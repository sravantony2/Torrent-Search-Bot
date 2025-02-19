# (c) @AbirHasan2005 & Jigar Varma & Hemanta Pokharel & The Anon Cat

import py1337x
import aiohttp
from pyrogram import Client, filters
from pyrogram.errors import QueryIdInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent
from tpblite import TPB

from configs import Config
from torrentx_handler import queryMessageContent

TorrentBot = Client(session_name=Config.SESSION_NAME, api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)


@TorrentBot.on_message(filters.command("start"))
async def start_handler(_, message: Message):
    await message.reply_text(
        text="Hello, I am Torrent Search Bot!\nI can search Torrent Magnetic Link from Inline.\n\nRe-Coded by @EdithSeedBox. Thanks to Abir Sir",
        disable_web_page_preview=True,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Search Torrents", switch_inline_query_current_chat="!s "),
                 InlineKeyboardButton("Go Inline", switch_inline_query="!s ")],
                [InlineKeyboardButton("Search ThePirateBay", switch_inline_query_current_chat="!pts "),
                 InlineKeyboardButton("Go Inline", switch_inline_query="!pts ")],
                [InlineKeyboardButton("Search 1337x", switch_inline_query_current_chat=""),
                 InlineKeyboardButton("Go Inline", switch_inline_query="")],
                [InlineKeyboardButton("Developer: Edith SeedBox", url="https://t.me/EdithSeedBox")]
            ]
        )
    )


@TorrentBot.on_inline_query()
async def inline_handlers(_, inline: InlineQuery):
    search_ts = inline.query
    answers = []
    if search_ts == "":
        answers.append(
            InlineQueryResultArticle(
                title="Search Something ...",
                description="Search For Torrents ...",
                input_message_content=InputTextMessageContent(
                    message_text="Search for Torrents from Inline!",
                    parse_mode="Markdown"
                ),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Search Torrents", switch_inline_query_current_chat="")]])
            )
        )
    elif search_ts.startswith("!pts"):
        # Coded by @AbirHasan2005 & Jigar Varma
        jv = search_ts.split(" ", 1)[-1]
        if jv == "":
            answers.append(
                InlineQueryResultArticle(
                    title="!pts [text]",
                    description="Search For Torrent in pirate bay ...",
                    input_message_content=InputTextMessageContent(
                        message_text="`!pts [text]`\n\nSearch Pirate Bay Torrents from Inline!",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!pts ")]])
                )
            )
        else:
            j_v = TPB()
            torrentList = j_v.search(jv)
            for torrent in torrentList:
                name_tor = torrent.title
                answers.append(
                    InlineQueryResultArticle(
                        title=f"{name_tor}",
                        description=f"Seeders: {torrent.seeds}, Leechers: {torrent.leeches}\nSize: {torrent.filesize}",
                        input_message_content=InputTextMessageContent(
                            message_text=f"/mirror {torrent.magnetlink}",
                            parse_mode="Markdown"
                        ),
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!pts ")]])
                    )
                )
                if name_tor == "":
                    answers.append(
                        InlineQueryResultArticle(
                            title="No Torrents Found in Pirate bay !",
                            description=f"Can't find torrents for {search_ts} in Pirate bay !!",
                            input_message_content=InputTextMessageContent(
                                message_text=f"No Torrents Found For `{search_ts}` in Pirate bay !!",
                                parse_mode="Markdown"
                            ),
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!pts ")]])
                        )
                    )
    elif search_ts.startswith("!s"):
        # Coded by @AbirHasan2005
        try:
            async with aiohttp.ClientSession() as ses:
                async with ses.get("https://api.sumanjay.cf/torrent/?query=" + search_ts.split(" ", 1)[-1]) as r:
                    try:
                        torrent = await r.json()
                        name_tor = ""
                        for i in range(Config.MAX_INLINE_RESULTS):
                            try:
                                name_tor = torrent[i]['name']
                                answers.append(
                                    InlineQueryResultArticle(
                                        title=f"{name_tor}",
                                        description=f"Seeders: {torrent[i]['seeder']}, Leechers: {torrent[i]['leecher']}\nSize: {torrent[i]['size']}",
                                        input_message_content=InputTextMessageContent(
                                            message_text=f"/mirror /{torrent[i]['magnet']}",
                                            parse_mode="Markdown"
                                        ),
                                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="!s ")]])
                                    )
                                )
                            except (IndexError, KeyError):
                                break
                        if name_tor == "":
                            answers.append(
                                InlineQueryResultArticle(
                                    title="No Torrents Found!",
                                    description=f"Can't find torrents for {search_ts} !!",
                                    input_message_content=InputTextMessageContent(
                                        message_text=f"No Torrents Found For `{search_ts}`",
                                        parse_mode="Markdown"
                                    ),
                                    reply_markup=InlineKeyboardMarkup(
                                        [[InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!s ")]])
                                )
                            )
                    except Exception as err:
                        print(f"Error: {err}")
                        answers.append(
                            InlineQueryResultArticle(
                                title="No Torrents Found!",
                                description=f"Can't find torrents for {search_ts} !!",
                                input_message_content=InputTextMessageContent(
                                    message_text=f"No Torrents Found For `{search_ts}`",
                                    parse_mode="Markdown"
                                ),
                                reply_markup=InlineKeyboardMarkup(
                                    [[InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!s ")]])
                            )
                        )
        except Exception as err:
            print(f"Error: {err}")
            answers.append(
                InlineQueryResultArticle(
                    title="No Torrents Found!",
                    description=f"Can't find torrents for {search_ts} !!",
                    input_message_content=InputTextMessageContent(
                        message_text=f"No Torrents Found For `{search_ts}`",
                        parse_mode="Markdown"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Try Again", switch_inline_query_current_chat="!s ")]])
                )
            )
    else:
        # Coded by Hemanta Pokharel, The Anon Cat
        # Re-Coded by @AbirHasan2005
        torrentX = py1337x.py1337x()
        offset = int(inline.offset.split(':')[0]) if inline.offset else 0
        page = int(inline.offset.split(':')[1]) if inline.offset else 1
        results = torrentX.search(inline.query, page)
        for count, item in enumerate(results['items'][offset:]):
            if count >= 5:
                break

            info = torrentX.info(link=item['link'])
            answers.append(
                InlineQueryResultArticle(
                    title=f"{item['name']}",
                    description=f"Seeders: {item['seeders']}, Leechers: {item['leechers']}\nSize: {item['size']}",
                    input_message_content=InputTextMessageContent(
                        message_text=queryMessageContent(torrentId=item['torrentId']),
                        parse_mode="HTML",
                        disable_web_page_preview=True
                    ),
                    thumb_url=info['image'],
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("Search Again", switch_inline_query_current_chat="")]
                        ]
                    )
                )
            )
    try:
        await inline.answer(
            results=answers,
            cache_time=0
        )
    except QueryIdInvalid:
        await inline.answer(
            results=answers,
            cache_time=0,
            switch_pm_text="Error: Search timed out!",
            switch_pm_parameter="start",
        )


TorrentBot.run()
