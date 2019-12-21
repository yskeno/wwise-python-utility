#! python3

""" WAAPI:Connect to Localhost.

    Find Extended description of function.

    Optional Args:
        -a,,--appName [str]: Application name that you want to connect to.
                             If not exist this arg, connect to 1st found application.
        -d, --disconnect: Turn off current connection.

    Returns:
        None
"""

import argparse
import sys
import waapi

parser = argparse.ArgumentParser(
    description="Connect to Remote Platform on Local host.")
parser.add_argument("-a", "--appName",
                    help="""The value in the Application Name column from the Remote Connection dialog in Wwise, or from "ak.wwise.core.remote.getAvailableConsoles".
                    If you are running more than one Sound Engine instance, you can specify the name of the application to connect to.""")
parser.add_argument("-d", "--disconnect", action="store_true",
                    help="""Disconnects the Wwise Authoring application from a connected Wwise Sound Engine running executable.""")

args = parser.parse_args()

try:
    # Connecting to Waapi using default URL
    with waapi.WaapiClient() as client:
        # NOTE: client will automatically disconnect at the end of the scope

        # Connect/Disconnect to Remote Platform on Local host
        if not args.disconnect:
            if client.call("ak.wwise.core.remote.getConnectionStatus")["isConnected"]:
                print(
                    "WAAPI/Connect to Local host:Already connected, please disconnect from current remote session first.")
                # Profiler Message is too verbose.
                # client.call("ak.soundengine.postMsgMonitor", {
                #             "message": "Connect to Local host:Already connected, please disconnect from current remote session first."})
                sys.exit()

            # Setup appName arg.
            # If more than one available consoles are found, use the 1st found appName to connect.
            if args.appName == None:
                appName = client.call(
                    "ak.wwise.core.remote.getAvailableConsoles")
                for i in range(len(appName["consoles"])):
                    if appName["consoles"][i]["host"] == "127.0.0.1":
                        appName = appName["consoles"][i]["appName"]
                        break
                    continue
            else:
                appName == args.appName

            # Connect to Localhost with appName
            remote_connect_args = {"host": "127.0.0.1",
                                   "appName": appName}
            client.call("ak.wwise.core.remote.connect", remote_connect_args)

        else:
            if not client.call("ak.wwise.core.remote.getConnectionStatus")["isConnected"]:
                print(
                    "WAAPI/Disconnect from Local host:Not Conneted to any remote sessions.")
                # Profiler Message is too verbose.
                # client.call("ak.soundengine.postMsgMonitor", {
                #             "message": "Disconnect from Local host:Not Conneted to any remote sessions."})
                sys.exit()
            client.call("ak.wwise.core.remote.disconnect")


except waapi.CannotConnectToWaapiException:
    print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")
