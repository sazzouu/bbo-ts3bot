import telnetlib
import time

class TClient:
    def __init__(self, ip, port):
        print("Initializing Telnet-Socket with {0} as remote and {1} as destination...".format(ip, port))
        self.__connection = None
        self.__result = []
        self.error = {
            'code': 0,
            'message': "Success!"
        }
        self.__error_msgs = {
            "0": "Success!",
            "256": "Command not found!",
            "512": "Invlalid Client-ID!",
            "513": "Nickname already in use!",
            "516": "Invalid client type... check your permissions!",
            "768": "Invalid Channel-ID!",
            "770": "No need to move!",
            "771": "Channelname already in use!",
            "772": "Channel not empty!",
            "1024": "Not logged into a virtual server!",
            "1538": "Inavlid parameter!",
            "1539": "Parameters not set!",
            "1540": "Invalid datatype for parameter!",
            "2817": "Slot limit reached!"
        }
        print("Done!\n")
        self.__connect(ip, port)
        time.sleep(5)

    def __connect(self, ip, port):
        if self.__connection == None:
            print("Connecting to {0} on port {1}...".format(ip, port))
            try:
                self.__connection = telnetlib.Telnet(ip, port)
            except:
                print("Connection could not be established!\nShutting down...")
            else:
                print("Success!\n")

    def __read_all(self):
        self.__result = self.__connection.read_very_eager().decode().split("\n\r")
        if(self.__result == ['']):
            time.sleep(0.1)
            self.__read_all()
        else:
            self.__result.pop()


    def __failed(self):
        self.__read_all()
        error = self.__result.pop().split(" ")
        err_code = int(error[1].split("=").pop())
        error_msg = self.__error_msgs[str(err_code)]

        self.error['code'] = err_code
        self.error['message'] = error_msg

        if err_code != 0:
            print(error_msg)
            self.__result = None
        else:
            if(len(self.__result) != 0):
                self.__result = self.__result[0]

    def write(self, command):
        self.__result = []
        self.__connection.write(str.encode(command + "\n"))
        self.__failed()
        return self.__result#