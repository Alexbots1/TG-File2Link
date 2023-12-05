
import os
import sys
import glob
import asyncio
import logging
import importlib
from pathlib import Path
from pyrogram import idle
from .bot import StreamBot
from .vars import Var
from aiohttp import web
from .server import web_server
from .utils.keepalive import ping_server

ppath = "WebStreamer/bot/plugins/*.py"
files = glob.glob(ppath)

loop = asyncio.get_event_loop()


async def start_services():
    print()
    if Var.SECONDARY:
        print("------------------ Starting as Secondary Server ------------------")
    else:
        print("------------------- Starting as Primary Server -------------------")
    print()
    print("-------------------- Initializing Telegram Bot --------------------")
    await StreamBot.start()
    bot_info = await StreamBot.get_me()
    StreamBot.id = bot_info.id
    StreamBot.username = bot_info.username
    StreamBot.fname=bot_info.first_name
    print("------------------------------ DONE ------------------------------")
    print()
    print("---------------------- Initializing Clients ----------------------")
    await initialize_clients()
    print("------------------------------ DONE ------------------------------")
    if Var.KEEP_ALIVE:
        print("------------------ Starting Keep Alive Service ------------------")
        print()
        asyncio.create_task(ping_server())
    print()
    print("--------------------- Initializing Web Server ---------------------")
    await server.setup()
    await web.TCPSite(server, Var.BIND_ADDRESS, Var.PORT).start()
    print("------------------------------ DONE ------------------------------")
    print()
    print("------------------------- Service Started -------------------------")
    print("                        bot =>> {}".format(bot_info.first_name))
    if bot_info.dc_id:
        print("                        DC ID =>> {}".format(str(bot_info.dc_id)))
    print(" URL =>> {}".format(Var.URL))
    print("------------------------------------------------------------------")
    await idle()

async def cleanup():
    await server.cleanup()
    await StreamBot.stop()

if __name__ == "__main__":
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        pass
    except Exception as err:
        logging.error(traceback.format_exc())
    finally:
        loop.run_until_complete(cleanup())
        loop.stop()
        print("------------------------ Stopped Services ------------------------")
