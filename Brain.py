from Socket import Telnet

class Bot:
    def __init__(self, name, password, ip="localhost", port=10011):
        print("Setting up TS3-Bot...")
        self.client = Telnet(ip, port)
        self.client.connect()
        self.connected = False
        self.ccount = 0
        self.login(name, password)

    def login(self, user, password):
        result = self.client.write("login {0} {1}".format(user, password))
        if not self.client.error:
            print("Successfully logged in!")
            self.use(self.serverList()['virtualserver_id'])
        else:
            print("Failed to connect to server!")

    def use(self, sid):
        print("Loggin into virtual server...")
        response = self.client.write("use sid=" + str(sid))
        if response != None:
            self.connected = True
            print("Successfully logged into virtual server!\n")
        else:
            self.connected = False
            print("Connection to virtual server could not be established!")

    def throw_error(self):
        print(self.client.error_msg)
        self.client.error_msg = "Everything is fine!"

    def globalMessage(self, text="Hello World!"):
        print("Sending global message: " + text + "...")
        text = text.replace(" ", "\s")
        result = self.client.write("gm msg=" + text)
        if result == None:
            print("Failed!\n")
        else:
            print("Success!\n")

    def commandHelp(self, command):
        self.client.write("help " + command)
        print(self.client.result)

    def serverInfo(self):
        self.client.write("serverinfo")
        self.client.result = self.client.result.split(" ")
        json = {}
        for i in range(0,len(self.client.result)):
            self.client.result[i] = self.client.result[i].split("=", 1)
            if len(self.client.result[i]) == 2:
                json[self.client.result[i][0]] = self.client.result[i][1].replace("\\s", " ")
        self.client.result = json
        return self.client.result

    def serverList(self):
        list = self.client.write("serverlist").split(" ")
        if list != None:
            jsonList = {}
            for i in range(0, len(list) - 1):
                temp = list[i].split("=")
                jsonList[temp[0]] = temp[1]
            return jsonList

    def editServer(self, new_config):
        params = ""
        for key, value in new_config.items():
            params += key + "=" + str(value).replace(" ", "\s") + " "
        self.client.write("serveredit " + params)

    def afkClients(self):
        response = self.client.write("clientlist -times")
        if response != None:
            response = response.split("|")
            clients = []
            for clientstring in response:
                jsonList = {}
                client = clientstring.split(" ")
                for i in range(0,len(client)):
                    temp = client[i].split("=")
                    jsonList[temp[0]] = temp[1]
                clients.append(jsonList)
            return clients
        else:
            print("No clients found! Are you connected?")
            return None

    def clientMove(self, clid, cid, reason=None):
        print("Moving client with ID {0} to channel {1}...\nReason: {2}".format(clid, cid, reason))
        response = self.client.write("clientmove " + str(clid) + " cid=" + str(cid))
        if response != None:
            print("Done!")
            if(reason != None):
                clids = str(clid).split("|")
                if len(clids) > 1:
                    for clid in clids:
                        self.clientPoke(clid, reason)
                else:
                    self.clientPoke(clids.pop(), reason)


    def clientPoke(self, clid, message):
        print("Poking client {0}...\nMessage: {1}".format(clid, message))
        response = self.client.write("clientpoke " + str(clid) + " msg=" + str(message.replace(" ", "\s")))
        if response != None:
            print("Done!\n")
        else:
            self.throw_error()

    def complains(self):
        print("Requesting serverinfos...")
        print("[Nothing implemented yet]\n")

    def setName(self, name):
        print("Setting bot-name...")
        name = name.replace(" ", "\s")
        response = self.client.write("clientupdate client_nickname=" + str(name))
        if response != None:
            print("Done!")

    def editChannel(self, cid, new_config):
        params = " "
        for key, value in new_config.items():
            params += key + "=" + str(value).replace(" ", "\s") + " "
        self.client.write("channeledit cid=" + str(cid) + params)

    def clientCount(self):
        response = self.serverInfo()
        return int(response['virtualserver_clientsonline'])

    def clientCountChanged(self):
        cur_count = self.clientCount()

        if cur_count != self.ccount:
            self.ccount = cur_count
            return True
        else:
            return False