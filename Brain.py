from Socket import TClient

class Bot:
    def __init__(self, name, password, ip="localhost", port=10011):
        print("Setting up TS3-Bot...")
        self.__client = TClient(ip, port)
        self.__ccount = 0
        self.__login(name, password)

    def __login(self, user, password):
        result = self.__client.write("login {0} {1}".format(user, password))
        if self.__client.error['code'] == 0:
            print("Successfully logged in!")
            self.__use(self.serverList()['virtualserver_id'])
        else:
            print("Failed to connect to server!")

    def __use(self, sid):
        print("Loggin into virtual server...")
        response = self.__client.write("use sid=" + str(sid))
        if response != None:
            print("Successfully logged into virtual server!\n")
        else:
            print("Connection to virtual server could not be established!")

    def getError(self):
        return self.__client.error

    def getClientCount(self):
        return self.__ccount

    def globalMessage(self, text="Hello World!"):
        print("Sending global message: " + text + "...")
        text = text.replace(" ", "\s")
        result = self.__client.write("gm msg=" + text)
        if result == None:
            print("Failed!\n")
        else:
            print("Success!\n")

    def commandHelp(self, command):
        print(self.__client.write("help " + command))

    def serverInfo(self):
        result = self.__client.write("serverinfo")
        result = result.split(" ")
        json = {}
        for i in range(0,len(result)):
            result[i] = result[i].split("=", 1)
            if len(result[i]) == 2:
                json[result[i][0]] = result[i][1].replace("\\s", " ")
        result = json
        return result

    def serverList(self):
        list = self.__client.write("serverlist").split(" ")
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
        self.__client.write("serveredit " + params)

    def afkClients(self):
        response = self.__client.write("clientlist -times")
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
        response = self.__client.write("clientmove " + str(clid) + " cid=" + str(cid))
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
        response = self.__client.write("clientpoke " + str(clid) + " msg=" + str(message.replace(" ", "\s")))
        if response != None:
            print("Done!\n")

    def clientServerGroups(self, cdbid):
        response = self.__client.write("servergroupsbyclientid cldbid=" + str(cdbid))
        response = response.split("|")
        groups = []
        for i in range(0, len(response)):
            group = {}
            for item in response[i].split(" "):
                item = item.replace("\\s", " ").split("=")
                group[item[0]] = item[1]
            groups.append(group)
        print(groups)
        return groups

    def setName(self, name):
        print("Setting bot-name...")
        name = name.replace(" ", "\s")
        response = self.__client.write("clientupdate client_nickname=" + str(name))
        if response != None:
            print("Done!")

    def editChannel(self, cid, new_config):
        params = " "
        for key, value in new_config.items():
            params += key + "=" + str(value).replace(" ", "\s") + " "
        self.__client.write("channeledit cid=" + str(cid) + params)

    def clientCount(self):
        response = self.serverInfo()
        return int(response['virtualserver_clientsonline'])

    def clientCountChanged(self):
        cur_count = self.clientCount()

        if cur_count != self.__ccount:
            self.__ccount = cur_count
            return True
        else:
            return False