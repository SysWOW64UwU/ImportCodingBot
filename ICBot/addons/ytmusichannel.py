# All the imports on top, just for the sake of convention, not mandatory
from pyrogram import Client, filters
from pyrogram.types import *
import yt_dlp
import shutil
import requests
from dotenv import load_dotenv
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor


executor = ThreadPoolExecutor(10)
loop = asyncio.get_event_loop()
load_dotenv()
'''===========EDITABLES==========='''

preFix = ""
cmds = ["ytch", F"ytch{os.getenv('BOT_UNAME')}"]
HELP = F"{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} link - upload music from youtube to the specified channel"
# Youtube video thumbnail link format
YT_THUMB_LINK = 'https://i.ytimg.com/vi/{id}/mqdefault.jpg'
MUSIC_CHANNEL = -1001746607360
CAPTION = '''
<b>Title</b> - <code>{title}</code>
<b>Artist</b> - <code>{uploader}</code>
'''

'''-------------------------------'''


def command(cmd): return filters.command(
  cmd, prefixes=preFix if preFix else os.getenv('MASTER_PREFIX', '/'))


def dl_thumbnail_image(link, msg):
  response = requests.get(link)
  if response.status_code == 200:
    try:
      os.remove(f"thumbnail_{msg.from_user.id}.jpg")
    except: pass

    with open(f"thumbnail_{msg.from_user.id}.jpg", "wb") as cover:
      cover.write(response.content)
    return True
  else:
    return None


@Client.on_message(command(cmds))
async def ytmusichannel(app, msg):
  args = msg.text.split(" ")
  if len(args) == 1:
    return await msg.reply(F"Usage:\n`{HELP}`", quote = 1)
  elif len(args) == 2:
    link = args[-1].strip()
  else:
    return await msg.reply(F"Usage:\n`{HELP}`", quote = 1)

  ydl_opts = {
    'format': 'bestaudio/best',
    'writethumbnail': 'True',
    'keepvideo': 'False',
    'postprocessors': [
      {
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '0',
      },
      {
        'key': 'FFmpegMetadata',
      },
      {
        'key': 'EmbedThumbnail',
      }
    ],
    'outtmpl': f"music_{msg.from_user.id}/%(title)s.%(ext)s"
  }

  song_path = os.path.join(os.getcwd(), f"music_{msg.from_user.id}")

  tag = F"[{msg.from_user.first_name}](tg://user?id={msg.from_user.id})"

  reply = await msg.reply_animation(
    animation="https://i.pinimg.com/originals/48/6a/a0/486aa0fa1658b7522ecd8918908ece40.gif",
    caption=f"<code>Downloading from YT...</code>",
  )
  try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(link)
  except:
    shutil.rmtree(song_path)
    return await reply.edit_media(
      InputMediaPhoto(
        media="https://c4.wallpaperflare.com/wallpaper/976/117/318/anime-girls-404-not-found-glowing-eyes-girls-frontline-wallpaper-preview.jpg",
        caption=f'<b>Link is invalid : </b><code>{link}</code>',
      )
    )
  try:
    await reply.edit_media(
      InputMediaAnimation(
        media="https://i.pinimg.com/originals/48/6a/a0/486aa0fa1658b7522ecd8918908ece40.gif",
        caption="<code>Download completed, Sending to telegram...</code>"
      )
    )
  except: pass

  if 'playlist' in link.lower():
    await playlist_upload(app, msg, reply, info, song_path, tag)
  else:
    await song_upload(app, msg, reply, info, song_path, tag)


async def song_upload(client, msg, reply, info, song_path, tag):
  thumb_status = await loop.run_in_executor(executor, lambda: dl_thumbnail_image(YT_THUMB_LINK.format(id=info['id']), msg))
  for song in os.listdir(song_path):
    fpath = os.path.join(song_path, song)
    if not song.endswith(".mp3"):
      os.remove(fpath)
    else:
      if thumb_status:
        song_uploaded = await client.send_audio(
          chat_id=MUSIC_CHANNEL,
          audio=fpath,
          thumb=f'thumbnail_{msg.from_user.id}.jpg',
          caption=CAPTION.format(
            title=info['title'],
            uploader=info['uploader']
          )
        )

      else:
        song_uploaded = await client.send_audio(
          chat_id=MUSIC_CHANNEL,
          audio=fpath,
          caption=CAPTION.format(
              title=info['title'],
              uploader=info['uploader']
          )
        )
      os.remove(fpath)

  buttons = [InlineKeyboardButton(
    text="Access Here",
    url=f'https://t.me/comding_music/{song_uploaded.id}'
  )]
  markup = InlineKeyboardMarkup([buttons])
  await reply.edit_media(
    media=InputMediaPhoto(
      media=f"thumbnail_{msg.from_user.id}.jpg",
      caption=f"<b>Your Song has been Uploaded -</b> {tag}"
    ),
    reply_markup=markup
  )
  try: os.remove(f'thumbnail_{msg.from_user.id}.jpg')
  except: pass


async def playlist_upload(client, msg, reply, info, song_path, tag):
  for song in info["entries"]:
    thumb_status = await loop.run_in_executor(executor, lambda: dl_thumbnail_image(YT_THUMB_LINK.format(id=song['id']), msg))
    fpath = os.path.join(song_path, f'{song["title"]}.mp3')
    if thumb_status:
      song_uploaded = await client.send_audio(
        chat_id=MUSIC_CHANNEL,
        audio=fpath,
        thumb=f'thumbnail_{msg.from_user.id}.jpg',
        caption=CAPTION.format(
          title=song['title'],
          uploader=song['uploader']
        )
      )
    else:
      song_uploaded = await client.send_audio(
        chat_id=msg.chat.id,
        audio=fpath,
        caption=CAPTION.format(
          title=song['title'],
          uploader=song['uploader']
          )
      )

  buttons = [InlineKeyboardButton(
    text="Access Here",
    url=f'https://t.me/comding_music/{song_uploaded.id}'
  )]
  markup = InlineKeyboardMarkup([buttons])
  shutil.rmtree(song_path)
  await reply.edit_media(
    media=InputMediaPhoto(
        media=f"thumbnail_{msg.from_user.id}.jpg",
        caption=f"<b>Your Playlist has been Uploaded</b> - {tag}"
    ),
    reply_markup=markup
  )
  try: os.remove(f'thumbnail_{msg.from_user.id}.jpg')
  except: pass