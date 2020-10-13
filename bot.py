from pyrogram import Client, filters
from pytube import YouTube, exceptions
import os
import requests


api_id = int(os.environ["API_ID"])
api_hash = os.environ["API_HASH"]
bot_token = os.environ["BOT_TOKEN"]

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


@app.on_message(filters.command("start", prefixes="/") & ~filters.edited)
def start(client, message):
    text = f"Hello {str(message.from_user.first_name)}, I am a YouTube downloader bot made by @infinitEplus." + \
        "Please see /help if you want to know how to use me."
    app.send_message(chat_id=message.from_user.id, text=text)


@app.on_message(filters.command("help", prefixes="/") & ~filters.edited)
def help(client, message):
    text = 'Download YT videos and audios by:\n' + \
        '/video link\n' + \
        '/audio link'
    message.reply_text(text)


@app.on_message(filters.command("video", prefixes="/") & ~filters.edited)
def video_dl(client, message):
    chat_id = message.from_user.id
    link = message.text.split('video', maxsplit=1)[1]
    try:
        yt = YouTube(link)
        video = yt.streams.get_highest_resolution().download('res')
        caption = yt.title
        with open('a.jpg', 'wb') as t:
            t.write(requests.get(yt.thumbnail_url).content)
        thumb = open('a.jpg', 'rb')
        app.send_chat_action(chat_id, "upload_video")
        client.send_video(chat_id=chat_id, video=video, caption=caption,
                          thumb=thumb, duration=yt.length)
        if os.path.exists(video):
            os.remove(video)
        if os.path.exists('a.jpg'):
            os.remove('a.jpg')

    except exceptions.RegexMatchError:
        message.reply_text("Invalid URL.")
    except exceptions.LiveStreamError:
        message.reply_text("Live Stream links not supported.")
    except exceptions.VideoUnavailable:
        message.reply_text("Video is unavailable.")
    except exceptions.HTMLParseError:
        message.reply_text("Given URL couldn't be parsed.")


@app.on_message(filters.command("audio", prefixes="/") & ~filters.edited)
def audio_dl(client, message):
    chat_id = message.from_user.id
    link = message.text.split('audio', maxsplit=1)[1]
    try:
        yt = YouTube(link)
        audio = yt.streams.get_audio_only().download('res')
        title = yt.title
        app.send_chat_action(chat_id, "upload_audio")
        with open('a.jpg', 'wb') as t:
            t.write(requests.get(yt.thumbnail_url).content)
        thumb = open('a.jpg', 'rb')
        client.send_audio(chat_id=chat_id, audio=audio, title=title,
                          thumb=thumb, performer=yt.author, duration=yt.length)
        if os.path.exists(audio):
            os.remove(audio)
        if os.path.exists('a.jpg'):
            os.remove('a.jpg')

    except exceptions.RegexMatchError:
        message.reply_text("Invalid URL.")
    except exceptions.LiveStreamError:
        message.reply_text("Live Stream links not supported.")
    except exceptions.VideoUnavailable:
        message.reply_text("Video is unavailable.")
    except exceptions.HTMLParseError:
        message.reply_text("Given URL couldn't be parsed.")


app.run()
