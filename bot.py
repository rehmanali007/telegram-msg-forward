#!/usr/bin/python

from telethon import TelegramClient, events, errors
# import logging
from configparser import


config = ConfigParser()
config.read('conf.ini')


# logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
# level=logging.WARNING)

api_id = config['TELEGRAM']['api_id']
api_hash = config['TELEGRAM']['api_hash']
target_group = config['TELEGRAM'].getint('telegram_destination_group_id')
session_file = 'telegramBot'


# ##############################################< Proxy >##############################################

try:
    proxy_enabled = config['PROXY'].getboolean('enable')
    proxy_server = config['PROXY']['server'].encode()
    proxy_port = config['PROXY'].getint('port')
except KeyError:
    proxy_enabled = True
    proxy_server = '159.89.49.60'
    proxy_port = 31264
    pass


# if config['proxy']['enable']:
#     sockProxy = {
#         "proxy_type": socks.SOCKS5,
#         "addr": conf.SOCKS5_SERVER,
#         "port": conf.SOCKS5_PORT,
#         "rdns": True,
#         "username": conf.USERNAME,
#         "password": conf.PASSWORD
#     }


if proxy_enabled:
    # print(f'Using proxy server {proxy_server}:{proxy_port}')
    telegramClient = TelegramClient(session_file, api_id, api_hash, proxy=(
        socks.SOCKS5, proxy_server, proxy_port))
else:
    telegramClient = TelegramClient(session_file, api_id, api_hash)


chats = conf['TELEGRAM'].['source_channels']
destination_channel = conf['TELEGRAM'].getint('dest_channel')


@client.on(events.NewMessage(chats, blacklist_chats=False))
async def newMessageHandler(msg):
    await client.send_message(dest_channel, msg.message)


try:
    client.start()
    print("-------------------------\nMessage Forward bot is up!\n-------------------------\n")
    print("[+] To run in the background type 'nohup python /path/to/app &' command. Thanks!\n")
    client.run_until_disconnected()
except KeyboardInterrupt:
    print("[+] Quiting bot!")
except errors.rpcerrorlist.ApiIdInvalidError:
    print("[+] Invalid API_ID/API_HASH")
