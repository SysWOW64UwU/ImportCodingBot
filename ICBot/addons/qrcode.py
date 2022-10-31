from pyrogram import Client, filters
import os
import requests
import json


'''===========EDITABLES==========='''

preFix = "/"
cmds = ["qr", F"qr{os.getenv('BOT_UNAME')}"]
HELP = F"""Provide comma separated URLs as the argument to this command
{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} url1, [url2, ...] - converts the given URLs to rebrandly QR code links

You may remove the '.qr' from the end of the resulting links to use them as shortened rebrandly links"""

'''-------------------------------'''


requestHeaders = {
  "Content-type": "application/json",
  "apikey": os.getenv('REBRANDLY_KEY')
}
command = lambda cmd: filters.command(cmd, prefixes = preFix if preFix else os.getenv('MASTER_PREFIX', '/'))

def rebrandly(url):
  linkRequest = {
    "destination": f"{url}", 
    "domain": { "fullName": "rebrand.ly" }
  }
  r = requests.post("https://api.rebrandly.com/v1/links", 
    data = json.dumps(linkRequest),
    headers=requestHeaders)
  if (r.status_code == requests.codes.ok):
    link = r.json()
    return link["shortUrl"]
  return 0

@Client.on_message(command(cmds))
async def qrcode(_, message):
  msg = message.text
  tinied = ""
  if len(msg.split())>1:
    rep = await message.reply("Generating...", quote = 1)
    arguments = [x.strip() for x in msg.partition(msg.split()[0])[-1].strip().split(',')]
    for count, argument in enumerate(arguments, 1):
      url = rebrandly(argument)
      if not url: endl = "\n"
      else: endl = ".qr\n"
      tinied += F"{count}. `{url}{endl}`"
    await rep.delete()
    await message.reply(tinied)
  else: return await message.reply(F"Usage:\n`{HELP}`", quote = 1)
