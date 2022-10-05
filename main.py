from flask import Response
from flask import Flask
import asyncio
from pyrogram import Client

api_id = 0
api_hash = ""

tg = Client("ud", api_id, api_hash)
app = Flask(__name__)

@app.route('/')
async def welcome():
    return "<h1><u><b>Heyy, hi</b></u></h1>"


@app.route("/<string:chat_id>/<string:msg_id>")
async def get_msg(chat_id = "", msg_id = 1):
    msg_id = int(msg_id)
    msg = await tg.get_messages(chat_id, msg_id)

    mime = ""
    if bool(msg.document):
        mime = msg.document.mime_type
    elif bool(msg.video):
        mime = msg.video.mime_type
    elif bool(msg.audio):
        mime = msg.audio.mime_type
    elif bool(msg.photo):
        mime = "image/png"
    elif bool(msg.sticker):
        mime = msg.sticker.mime_type
    elif bool(msg.animation):
        mime = msg.animation.mime_type
    elif bool(msg.voice):
        mime = msg.voice.mime_type
    elif bool(msg.video_note):
        mime = msg.video_note.mime_type
    elif bool(msg.contact):
        mime = msg.contact.mime_type
    elif bool(msg.location):
        mime = msg.location.mime_type
    elif bool(msg.venue):
        mime = msg.venue.mime_type
    elif bool(msg.game):
        mime = msg.game.mime_type
    elif bool(msg.poll):
        mime = msg.poll.mime_type
    elif bool(msg.dice):
        mime = msg.dice.mime_type
    else:
        if msg.text.startswith(".web"):
            msg.text = msg.text[4:]
            msg.text = msg.text.strip()
            msg.text = msg.text.replace("\n", "<br>")
            return f"""
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
</head>
<body>
    {msg.text}
</body>
"""

    return Response(bytes((await tg.download_media(msg, in_memory=True)).getbuffer()), mimetype=mime)

import threading
import os
import subprocess

if __name__ == '__main__':
 
    #os.system('sudo kill -9 $(lsof -t -i:"1234")')
    threading.Thread(target=app.run, kwargs = {"host":"0.0.0.0", "port":1234}, daemon=True).start() #
    
    
    for i in range(3): #, wpp
        print(f"Starting UD engine...")
        while 1:
            try:
                tg.run()
                break
            except Exception as e:
                if "locked" in str(e):
                    print(f"Restarting for locked problem... ({e})")
                    session = "ud.session"
                    t = subprocess.Popen((f"sudo fuser {session}").split(), stdout=subprocess.PIPE)
                    process_id = str(t.communicate()[0]).split(" ")[1]
                    subprocess.Popen((f"sudo kill {process_id}").split(), stdout=subprocess.PIPE)
                    continue

                print(e)
                break
    
