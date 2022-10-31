from pyrogram import Client, filters
import os
from urllib.parse import urlencode
import requests


'''===========EDITABLES==========='''

preFix = "/"
cmds = ["tiny", F"tiny{os.getenv('BOT_UNAME')}"]
HELP = F"""Provide comma separated URL(s) as an argument to this command
{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} url1, [url2, ...] - converts the given URL(s) to tinyurl link(s)"""

'''-------------------------------'''


command = lambda cmd: filters.command(cmd, prefixes = preFix if preFix else os.getenv('MASTER_PREFIX', '/'))

def make_tiny(url):
  request_url = F"http://tinyurl.com/api-create.php?{urlencode({'url': url})}"
  result = requests.get(request_url)
  return result.text

@Client.on_message(command(cmds))
async def tinyurl(_, message):
  msg = message.text
  tinied = ""
  if len(msg.split())>1:
    rep = await message.reply("Processing...")
    arguments = [x.strip() for x in msg.partition(msg.split()[0])[-1].strip().split(',')]
    for count, argument in enumerate(arguments, 1):
      url = make_tiny(argument)
      tinied += F"{count}. `{url}`\n"
    await rep.delete()
    await message.reply(tinied)
  else: return await message.reply(F"Usage:\n`{HELP}`", quote = 1)