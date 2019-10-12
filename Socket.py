import telnetlib

class Telnet:
    def __init__(self, ip, port):
        print("Initializing Telnet-Socket with {0} as remote and {1} as destination...".format(ip, port))
        self.host = ip
        self.port = port
        self.connection = None
        self.result = []
        self.error = []
        self.error_msg = "Everything is fine!"
        print("Done!\n")

    def connect(self):
        if self.connection == None:
            print("Connecting to {0} on port {1}...".format(self.host, self.port))
            try:
                self.connection = telnetlib.Telnet(self.host, self.port)
                self.read_all()
                print("Success!\n")
            except:
                print("Connection could not be established!\nShutting down...")

    def read_all(self):
        res = self.connection.read_until(b"\n\r", 1)
        if(res != b''):
            self.result.append(res.decode().split("\n\r")[0])
            self.read_all()

    def failed(self):
        self.read_all()
        self.error = self.result.pop().split(" ")
        err_code = int(self.error[1].split("=").pop())
        self.error = err_code != 0
        if self.error:
            swticher = {
                "0": "Success!",
                "256": "Command not found!",
                "512": "Invlalid Client-ID!",
                "516": "Invalid client type... check your permissions!",
                "768": "Invalid Channel-ID!",
                "771": "Channelname already in use!",
                "1024": "Not logged into a virtual server!",
                "1538": "Inavlid parameter!",
                "1539": "Parameters not set!",
                "1540": "Invalid datatype for parameter!",
                "2817": "Slot limit reached!"
            }
            self.error_msg = swticher[str(err_code)]
            print(self.error_msg)
            self.result = None
        else:
            if(len(self.result) != 0):
                self.result = self.result[0]

    def write(self, command):
        self.result = []
        self.connection.write(str.encode(command + "\n"))
        self.failed()
        return self.result

