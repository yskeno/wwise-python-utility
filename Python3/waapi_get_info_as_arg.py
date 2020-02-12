#! python3
""" WAAPI:Get info and Execute application with arg.

    Get Wwise information and execute application with this wwise info as argument.
    For Example, "-a program.exe -t wprojname" returns "program.exe [Wwise Project Name]" on Command Prompt.

    Optional Args:
        -a,,--application [str]: Execute this program(or application) with Wwise info as arguments.
                                 If this arg is not exist, just show Wwise Info on cmd.
        -t, --type [wprojname, wprojpath, reaprojpath]:
                                 Select Wwise information type that you want.
                                    wprojname: Wwise project name
                                    wprojpath: .wproj directory
                                    reaprojpath: REAPROJ path in AudioFileSources' notes.
                                                 In use case, "-a reaper.exe -t reaprojpath" can open reaper project that import AudioFileSource to Wwise.

    Returns:
                subprocess.Popen(args.application + " " + exec_arg)
        else:
            for exec_arg in exec_args:
                subprocess.Popen("echo " + exec_arg, shell=True)
"""

import argparse
import os
import re
import subprocess
import sys
import waapi

parser = argparse.ArgumentParser(
    description="Pass Wwise Info to argument of Program.")
parser.add_argument("-a", "--application", type=str,
                    help="""Execute this program(or application) with Wwise info as arguments.
                    If this arg is not exist, just show Wwise Info on cmd.
                    For Example, "-a program.exe -t wprojname" returns "program.exe [Wwise Project Name]".""")
parser.add_argument("-t", "--type",
                    help="Type of Wwise info that you need.",
                    choices=["wprojname", "wprojpath", "reaprojpath"])

args = parser.parse_args()

try:
    # Connecting to Waapi using default URL
    with waapi.WaapiClient() as client:
        # NOTE: client will automatically disconnect at the end of the scope
        exec_args = set()

        # Get Project Name
        if args.type == "wprojname":
            get_project_name_args = {
                "from": {
                    "ofType": ["Project"]
                },
                "options": {
                    "return": ["name"]
                }
            }
            ret_info = client.call(
                "ak.wwise.core.object.get", get_project_name_args)
            exec_args.add(ret_info["return"][0]["name"])

        # Get wproj File Path
        elif args.type == "wprojpath":
            get_project_path_args = {
                "from": {
                    "ofType": ["Project"]
                },
                "options": {
                    "return": ["filePath"]
                }
            }
            ret_info = client.call(
                "ak.wwise.core.object.get", get_project_path_args)
            exec_args.add(ret_info["return"][0]["filePath"])

        # Get Reaper Project Path Written in AudioFileSource Notes
        elif args.type == "reaprojpath":
            selected_obj = client.call("ak.wwise.ui.getSelectedObjects")
            selected_id = []
            for i in range(len(selected_obj["objects"])):
                selected_id.append(selected_obj["objects"][i]["id"])
            get_reaper_recall_args = {
                "from": {
                    "id": selected_id
                },
                "transform": [
                    {"select": ["children"]},
                    {"where": [
                        "type:isIn", ["AudioFileSource"]
                    ]}
                ],
                "options": {
                    "return": ["notes"]
                }
            }
            ret_info = client.call(
                "ak.wwise.core.object.get", get_reaper_recall_args)
            # Find rpp path in objects' notes
            for i in range(len(ret_info["return"])):
                rpp_regex = re.search(
                    r"(?<=REAPROJ:\").+\.rpp", ret_info["return"][i]["notes"])
                exec_args.add(rpp_regex.group())
        else:
            pass

        # Execute program with arguments.
        exec_app = ""
        if args.application != None:
            exec_app = args.application
            if os.path.exists(args.application):
                for exec_arg in exec_args:
                    # subprocess.Popen("echo" + '"' + exec_arg + '"', shell=True)
                    subprocess.Popen([args.application, exec_arg])
        else:
            print("Not Found Application.")
            sys.exit()
            # for exec_arg in exec_args:
            #     subprocess.call(
            #         "echo" + '"' + exec_arg + '"', shell=True)


except waapi.CannotConnectToWaapiException:
    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")
