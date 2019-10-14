from Brain import Bot as Client
import json

with open("./config.json", "r") as file:
    config = json.load(file)

    bot = Client(config['query_name'], config['query_password'], config['query_address'], config['query_port'])
    bot.setName(config['bot_name'])
    if config['server_settings_override']:
        cur_info = bot.serverInfo()
        new_info = {}

        for key, value in config['server_settings'].items():
            if (cur_info[key] != value):
                new_info[key] = value

        bot.editServer(new_info)

    if config['use_auto_expands']:
        for auto in config['auto_expands']:
            start = 0
            end = None
            channels = bot.getChannels()
            for i in range(0, len(channels)):
                if channels[i]['cid'] == auto['start_cid']:
                    start = i
                elif channels[i]['cid'] == auto['end_cid']:
                    end = i

            if end == None:
                channels = channels[start + 1:]
            else:
                if start == end:
                    channels = channels[start]
                else:
                    channels = channels[start + 1:end]

            for channel in channels:
                bot.channelDelete(channel['cid'])

            bot.channelCreate(auto['label'].format(1), auto['start_cid'])



    while(True):
        if bot.getError()['code'] == 1024:
            print("Connection seems to be lost...")
            break
        else:
            if config['use_afk']:
                afks = bot.afkClients()
                afk_ids = ""
                for afk in afks:
                    if int(afk['client_database_id']) != 1:
                        if(int(afk['cid']) != config['afk_cid'] and not int(afk['cid']) in config['afk_immune_cids']):
                            if int(afk['client_idle_time']) > config['max_idle_time']:
                                temp = "clid=" + afk['clid'] + "|"

                                for group in bot.clientServerGroups(afk['client_database_id']):
                                    if int(group['sgid']) in config['afk_immune_gids']:
                                        temp = ""

                                afk_ids += temp

                if afk_ids != "":
                    afk_ids = afk_ids[:-1]
                    bot.clientMove(afk_ids, config['afk_cid'], config['afk_move_message'])

            if config['use_auto_expands']:
                for auto in config['auto_expands']:
                    start = 0
                    end = None
                    channels = bot.getChannels()
                    for i in range(0, len(channels)):
                        if channels[i]['cid'] == auto['start_cid']:
                            start = i
                        elif channels[i]['cid'] == auto['end_cid']:
                            end = i

                    if end == None:
                        channels = channels[start + 1:]
                    else:
                        if start == end:
                            channels = channels[start]
                        else:
                            channels = channels[start + 1:end]

                    temp = channels.pop()
                    if temp['total_clients'] != "0":
                        bot.channelCreate(auto['label'].format(len(channels) + 2), temp['cid'])

                    keeper = []
                    if(len(channels)) >= 1:
                        for channel in channels:
                            if channel['total_clients'] == "0":
                                bot.channelDelete(channel['cid'])
                            else:
                                keeper.append(channel)
                    keeper.append(temp)
                    channels = keeper

                    for i in range(0, len(channels)):
                        if channels[i]['channel_name'] != auto['label'].format(i + 1):
                            bot.editChannel(channels[i]['cid'], {
                                'channel_name': auto['label'].format(i + 1)
                            })

            if config['use_online_spacer']:
                if bot.clientCountChanged():
                    cfg = {
                        'channel_name': config['online_spacer_label'].format(bot.getClientCount()),
                    }
                    bot.editChannel(config['online_spacer_cid'], cfg)