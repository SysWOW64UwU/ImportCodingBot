from pyrogram import Client, filters
import os
import PyBypass as bypasser # Star https://github.com/sanjit-sinha/PyBypass


'''===========EDITABLES==========='''

preFix = "/"
cmds = ["bypass", F"bypass{os.getenv('BOT_UNAME')}"]
HELP = F"""Provide comma separated shortened URLs as the argument to this command
{preFix if preFix else os.getenv('MASTER_PREFIX', '/')}{cmds[0]} url1, [url2, ...] - retrieves the original URL

Inline Usage:
Provide only 1 URL in inline mode
{os.getenv('BOT_UNAME')} {cmds[0]} URL"""

'''-------------------------------'''


command = lambda cmd: filters.command(cmd, prefixes = preFix if preFix else os.getenv('MASTER_PREFIX', '/'))

@Client.on_message(command(cmds))
async def bypass(_, message):
  msg = message.text
  bypassed = ""
  if len(msg.split())>1:
    rep = await message.reply("Processing...")
    arguments = [x.strip() for x in msg.partition(msg.split()[0])[-1].strip().split(',')]
    for count, argument in enumerate(arguments, 1):
      try: url = bypasser.bypass(argument)
      except: url = "Error"
      bypassed += F"{count}. `{url}`\n"
    await rep.delete()
    await message.reply(bypassed)
  else: return await message.reply(F"Usage:\n`{HELP}`", quote = 1)

# Inline method defined in inlineQHandler.py