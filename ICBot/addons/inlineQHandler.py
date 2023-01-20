from pyrogram import Client, enums
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from addons.gangsta import gangstafy # Star https://github.com/SouravJohar/gangsta
from addons.urlprev import urlformat, uri_validator
import PyBypass as bypasser # Star https://github.com/sanjit-sinha/PyBypass


'''===========EDITABLES==========='''

queries = ["gangsta", "uf", "urlprev", "bypass"]

'''-------------------------------'''


@Client.on_inline_query()
async def inlineQHandler(_, queryObj):
  query = queryObj.query
  if not query: return
  results=[]

  # gangsta
  if query.split()[0]==queries[0]:
    try: oText = query.split(maxsplit=1)[1]
    except: return
    gText = gangstafy(oText)
    results.append(
      InlineQueryResultArticle(
        title=gText,
        input_message_content=InputTextMessageContent(gText, parse_mode=enums.ParseMode.DISABLED)
      )
    )

  # uf
  if query.split()[0]==queries[1]:
    try: text = query.split(maxsplit=1)[1]
    except: return
    disablePrev=text.endswith("~")
    if disablePrev:text=text[:-1]
    results.append(
      InlineQueryResultArticle(
        title="Send unformatted text",
        input_message_content=InputTextMessageContent(text, parse_mode=enums.ParseMode.DISABLED, disable_web_page_preview=disablePrev)
      )
    )

  # urlprev
  if query.split()[0]==queries[2]:
    try: query = query.split(maxsplit=1)[1]
    except: return
    if len(query.split('|||'))==2:
      elements = [x.strip() for x in query.split('|||')]
      txt = elements[0]
      uri = elements[1]
      if uri_validator(uri):
        results.append(
          InlineQueryResultArticle(
            title="Send this preview!",
            input_message_content=InputTextMessageContent(urlformat.format(uri, txt))
          )
        )
      else:
        results.append(
          InlineQueryResultArticle(
            title="INVALID URL! Don't send this.",
            input_message_content=InputTextMessageContent('`Invalid URL Passed!`')
          )
        )

  # bypass
  if query.split()[0]==queries[3]:
    try: link = query.split(maxsplit=1)[1]
    except: return
    disablePrev=link.endswith("~")
    if disablePrev:link=link[:-1]
    try: url = bypasser.bypass(link)
    except: url = 0
    results.append(
      InlineQueryResultArticle(
        title="Send bypassed link" if url else "Unable to bypass this link :/",
        input_message_content=InputTextMessageContent(url if url else ":/", disable_web_page_preview=disablePrev)
      )
    )

  # new_query
  # if query.split()[0]==queries[Index_Of_Your_Query]:
  #   results.append(Results_of_the_query)
  
  await queryObj.answer(results, cache_time=1)
