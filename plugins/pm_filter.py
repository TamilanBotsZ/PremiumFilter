# Codeded By @Tamilan_BotsZ
import asyncio
import re
import ast
import math
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from tamilanbotsz import short_url
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import ADMINS, AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTI_SHOW_OFF, IMDB, FILE_REQ_CHANNEL, HOW_TO_DOWNLOAD, PICS, AUTO_DELETE, AUTO_DELETE_SECONDS, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_shortlink, get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
file_req_channel = FILE_REQ_CHANNEL

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}
FILTER_MODE = {}

@Client.on_message(filters.command('autofilter'))
async def fil_mod(client, message): 
      mode_on = ["yes", "on", "true"]
      mode_of = ["no", "off", "false"]

      try: 
         args = message.text.split(None, 1)[1].lower() 
      except: 
         return await message.reply("**Iɴᴄᴏᴍᴩʟᴇᴛᴇ Cᴏᴍᴍᴀɴᴅ...**")
      
      m = await message.reply("**Sᴇᴛᴛɪɴɢs.../**")

      if args in mode_on:
          FILTER_MODE[str(message.chat.id)] = "True" 
          await m.edit("**Aᴜᴛᴏ-Fɪʟᴛᴇʀ Eɴᴀʙʟᴇᴅ**")
      
      elif args in mode_of:
          FILTER_MODE[str(message.chat.id)] = "False"
          await m.edit("**Aᴜᴛᴏ-Fɪʟᴛᴇʀ Dɪsᴀʙʟᴇᴅ**")
      else:
          await m.edit("Usᴇ :- /autofilter on Oʀ /autofilter off")

@Client.on_message((filters.group | filters.private) & filters.text & filters.incoming)
async def give_filter(client, message):
    k = await manual_filters(client, message)
    if k == False:
        await auto_filter(client, message)


@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer("oKda", show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.", show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await get_settings(query.message.chat.id)
    if settings['button']:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}", callback_data=f'files#{file.file_id}'
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'files_#{file.file_id}',
                ),
            ]
            for file in files
        ]
    
    if 0 < offset <= 6:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 6
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("‹‹‹ Bᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"),
             InlineKeyboardButton(f"📃 Pᴀɢᴇs {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}",
                                  callback_data="pages")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
             InlineKeyboardButton("Nᴇxᴛ ›››", callback_data=f"next_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("‹‹‹ Bᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
                InlineKeyboardButton("Nᴇxᴛ ›››", callback_data=f"next_{req}_{key}_{n_offset}")
            ],
        )
    btn.insert(0, [
        InlineKeyboardButton("😌 Cʜᴇᴄᴋ Bᴏᴛ PM 😌", url=f"https://t.me/{temp.U_NAME}")
    ])
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()


@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("sᴇᴀʀᴄʜ ʏᴏᴜʀsᴇʟғ", show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Iᴀᴍ Cʜᴇᴄᴋɪɴɢ U Asᴋᴇᴅ Fɪʟᴇ Iɴ Mʏ Dʙ...')
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:
             k = await query.message.edit('Sᴏʀʀʏ Pʟᴇᴀsᴇ Cʜᴇᴄᴋ Yᴏᴜʀ Sᴩᴇʟʟɪɴɢ Iɴ Gᴏᴏɢʟᴇ Fɪʀsᴛ ﹦ Iғ Yᴏᴜʀ Sᴩᴇʟʟɪɴɢ Cᴏʀʀᴇᴄᴛ Mᴇᴀɴs Tʜᴀᴛ Fɪʟᴇ Nᴏᴛ Fᴏᴜʙᴅ Iɴ Mʏ Dᴀᴛᴀʙᴀsᴇ 💌')
             await asyncio.sleep(30)
             await k.delete()



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Tʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴀᴄᴛɪᴠᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴꜱ!! Cᴏɴɴᴇᴄᴛ ᴛᴏ ꜱᴏᴍᴇ ɢʀᴏᴜᴘꜱ ғɪʀꜱᴛ.", quote=True)
                    return await query.answer(' ˆ°• Tᴀᴍɪʟᴀɴ BᴏᴛsZ •°ˆ ')
            else:
                await query.message.edit_text(
                    "Iᴀᴍ Nᴏᴛ Cᴏɴɴᴇᴄᴛᴇᴅ Tᴏ Aɴʏ Gʀᴏᴜᴩ \nCʜᴇᴄᴋ /connections Oʀ Cᴏɴɴᴇᴄᴛ Tᴏ Aɴʏ Gʀᴏᴜᴩ",
                    quote=True
                )
                return await query.answer(' ˆ°• Tᴀᴍɪʟᴀɴ BᴏᴛsZ •°ˆ ')

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return await query.answer(' ˆ°• Tᴀᴍɪʟᴀɴ BᴏᴛsZ •°ˆ ')

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("Tʜᴀᴛ´s Nᴏᴛ Fᴏʀ Yᴏᴜ !!", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("🚫 Dᴇʟᴇᴛᴇ 🚫", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("‹‹‹ Bᴀᴄᴋ", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return await query.answer(' ˆ°• Tᴀᴍɪʟᴀɴ BᴏᴛsZ •°ˆ ')
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text('Some error occurred!!', parse_mode=enums.ParseMode.MARKDOWN)
        return await query.answer(' ˆ°• Tᴀᴍɪʟᴀɴ BᴏᴛsZ •°ˆ ')
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Dɪsᴄᴏɴɴᴇᴄᴛᴇᴅ Fʀᴏᴍ **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"Sᴏᴍᴇ Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer(' ˆ°• Tᴀᴍɪʟᴀɴ BᴏᴛsZ •°ˆ ')
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Sᴜᴄᴄᴇssғᴜʟʟʏ Cᴏɴɴᴇᴄᴛɪᴏɴ Dᴇʟᴇᴛᴇᴅ"
            )
        else:
            await query.message.edit_text(
                f"Sᴏᴍᴇ Eʀʀᴏʀ Oᴄᴄᴜʀᴇᴅ!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer(' ˆ°• Tᴀᴍɪʟᴀɴ BᴏᴛsZ •°ˆ ')
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return await query.answer(' ˆ°• Tᴀᴍɪʟᴀɴ BᴏᴛsZ •°ˆ ')
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    if query.data.startswith("file"):
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"

        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            elif settings['botpm']:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            else:
                g = short_url(f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                await client.send_photo(chat_id=query.from_user.id, photo='https://graph.org/file/f7f173057c2b76940c79c.jpg', caption = f"<b>📕Nᴀᴍᴇ ➠ : <code>{files.file_name}</code> \n\n🔗Sɪᴢᴇ ➠ : {get_size(files.file_size)}</b>", 
                                          reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('⁉️ Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ ⁉️', url=HOW_TO_DOWNLOAD)
                ],
                [
                    InlineKeyboardButton('📂 Dᴏᴡɴʟᴏᴀᴅ Nᴏᴡ 📂', url=g)
                ]]))
                await query.answer('Cʟɪᴄᴋ °Cʜᴇᴄᴋ Bᴏᴛ Pᴍ° Bᴜᴛᴛᴏɴ\n\nI Sᴇɴᴛᴇᴅ U ASᴋᴇᴅ Fɪʟᴇs', show_alert=True)
        except UserIsBlocked:
            await query.answer('Fɪʀsᴛ Sᴛᴀʀᴛ Mᴇ Tʜᴇɴ I Wɪʟʟ Sᴇɴᴅ Fɪʟᴇs !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("Fɪʀsᴛ Jᴏɪɴ Tʜᴇ Cʜᴀɴɴᴇʟ Aɴᴅ Cʟɪᴄᴋ Tʜɪs 😒", show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('Nᴏ Sᴜᴄʜ Fɪʟᴇ Exsɪsᴛ.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        await query.answer()
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            protect_content=True if ident == 'checksubp' else False
        )
    elif query.data == "pages":
        await query.answer()

    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('➕ Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴘ ➕', url=f"https://t.me/{temp.U_NAME}?startgroup=true")
            ],[
            InlineKeyboardButton('💥 Mᴏᴠɪᴇ Uᴘᴅᴀᴛᴇs 💥', url='https://t.me/+5aoApavIMVo1YzQ1'),
            InlineKeyboardButton('🔎 Sᴇᴀʀᴄʜ Gʀᴏᴜᴘ 🔍', url='https://t.me/TamilanMoviesChat')
            ],[
            InlineKeyboardButton('😅 Sᴏᴜʀᴄᴇ Cᴏᴅᴇ 😊', callback_data='sources')
            ],[
            InlineKeyboardButton('💌 Aʙᴏᴜᴛ Aɴᴅ Iɴғᴏ 💌', callback_data= 'about')
            ],[
            InlineKeyboardButton('❌ Cʟᴏꜱᴇ ❌', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
         )
    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('🤖 Uᴩᴅᴀᴛᴇs 😜', url='https://t.me/Tamilan_BotsZ'),
            InlineKeyboardButton('♥️ Sʜᴀʀᴇ Mᴇ 💫', url=f"https://t.me/share/url?url=t.me/{temp.U_NAME}")
        ], [
            InlineKeyboardButton('🔭 Sᴛᴀᴛs 📊', callback_data='stats'),
            InlineKeyboardButton('📞 Cᴏɴᴛᴀᴄᴛ 📟', callback_data='contact')
        ], [
            InlineKeyboardButton('😅 Sᴏᴜʀᴄᴇ Cᴏᴅᴇ 😊', callback_data='source')
        ], [
            InlineKeyboardButton('😜 Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ Fɪʟᴇs Fʀᴏᴍ Mᴇ 😜', callback_data='info')
        ], [
            InlineKeyboardButton('👋 Exᴛʀᴀ Fᴇᴀᴛᴜʀᴇs 👋', callback_data='mods')
        ], [
            InlineKeyboardButton('📦 Cʜᴇᴄᴋ Pɪɴɢ 📡', callback_data='pongd')
        ], [
            InlineKeyboardButton('‹‹‹ Bᴀᴄᴋ', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
       )
    elif query.data == "mods":
        buttons = [[
            InlineKeyboardButton('🖼️ Tᴇʟᴇɢʀᴀᴘʜ 🔭', callback_data='tele')
        ],[
            InlineKeyboardButton('🗿 Cʜᴇᴄᴋ Pɪɴɢ ✏️', callback_data='pong')
        ],[
            InlineKeyboardButton('🤙 Sʜᴀʀᴇ Tᴇxᴛ 🤙', callback_data='share')
        ],[
            InlineKeyboardButton('🧑‍💻 Cᴀʀʙᴏɴ Gᴇɴᴇʀᴀᴛᴏʀ ✴️', callback_data='carbon')
        ],[ 
            InlineKeyboardButton('🙌 Fᴏɴᴛ Gᴇɴᴇʀᴀᴛᴏʀ 📝', callback_data='font')
        ],[  
            InlineKeyboardButton("▶️ Yᴛ Vɪᴅᴇᴏ Dᴏᴡɴʟᴀᴅᴇʀ 🎦", callback_data='video')
        ],[
            InlineKeyboardButton('🔭 Sᴛᴀᴛs 📊', callback_data='stats')
        ],[
            InlineKeyboardButton('😊 Sᴏᴜʀᴄᴇ Cᴏᴅᴇ ☺', url='https://Github.com/TamilanBotsZ/PremiumFilter')
        ],[
            InlineKeyboardButton('‹‹‹ Bᴀᴄᴋ', callback_data='about')
        ]]       
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MODS_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
       )
    elif query.data == "tele":
        buttons = [[
            InlineKeyboardButton('‹‹‹ Bᴀᴄᴋ', callback_data='mods')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.TELE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
       )
    elif query.data == "share":
        buttons = [[
            InlineKeyboardButton('‹‹‹ Bᴀᴄᴋ', callback_data='mods')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SHARE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "carbon":
        buttons = [[
            InlineKeyboardButton('‹‹‹ Bᴀᴄᴋ', callback_data='mods')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CARBON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "font":
        buttons = [[
            InlineKeyboardButton('‹‹‹ Bᴀᴄᴋ', callback_data='mods')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.FONT_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
       )
    elif query.data == "video":
        buttons = [[
            InlineKeyboardButton('‹‹‹ Bᴀᴄᴋ', callback_data='mods')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.VIDEO_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "pongd":
        buttons = [[
            InlineKeyboardButton('‹‹‹ Bᴀᴄᴋ', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.PONGD_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "pong":
        buttons = [[
            InlineKeyboardButton('‹‹‹ Bᴀᴄᴋ', callback_data='mods')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.PONG_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "sources":
        buttons = [[

            InlineKeyboardButton('😊 Rᴇᴩᴏ 😊', url='https://Github.com/TamilanBotsZ/PremiumFilter')
        ], [
            InlineKeyboardButton('‹‹‹ Bᴀᴄᴋ', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SOURCES_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "source":
        buttons = [[

            InlineKeyboardButton('😊 Rᴇᴩᴏ 😊', url='https://Github.com/TamilanBotsZ/PremiumFilter')
        ], [
            InlineKeyboardButton('‹‹‹ Bᴀᴄᴋ', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "info":
        buttons = [[
            InlineKeyboardButton('😪 Hᴏᴡ Tᴏ Oᴩᴇɴ Mʏ Lɪɴᴋs 💢', url='https://t.me/Sharath_Links/13')
        ], [
            InlineKeyboardButton('📞 Cᴏɴᴛᴀᴄᴛ 📟', callback_data='contact')
        ], [
            InlineKeyboardButton('‹‹‹ Bᴀᴄᴋ', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MANUELFILTER_TXT,       
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "contact":
        buttons = [[
            InlineKeyboardButton('😳 Cʀᴇᴀᴛᴏʀ 😳', url='https://t.me/SharathItsIsMe')
        ], [     
            InlineKeyboardButton('📞 Cᴏɴᴛᴀᴄᴛ 📟', url='https://t.me/TamilanBotsZ_Support')
        ], [  
            InlineKeyboardButton('‹‹‹ Bᴀᴄᴋ', callback_data='about')
        ], [
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONTACT_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('♻️ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ], [
            InlineKeyboardButton('‹‹‹ Bᴀᴄᴋ', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('♻️ Rᴇғʀᴇsʜ', callback_data='rfrsh')
        ], [
            InlineKeyboardButton('‹‹‹ Bᴀᴄᴋ', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Your Active Connection Has Been Changed. Go To /settings.")
            return await query.answer('Piracy Is Crime')

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Fɪʟᴛᴇʀ Bᴜᴛᴛᴏɴ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                ],
                [
                    InlineKeyboardButton('Sɪɴɢʟᴇ' if settings["button"] else 'Dᴏᴜʙʟᴇ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Fᴏʀᴡᴀʀᴅ Rᴇsᴛʀɪᴄᴛ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yᴇs' if settings["file_secure"] else '❌ Nᴏ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Iᴍᴅʙ', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yᴇs' if settings["imdb"] else '❌ Nᴏ',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Sᴩᴇʟʟ Cʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yᴇs' if settings["spell_check"] else '❌ Nᴏ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Wᴇʟᴄᴏᴍᴇ', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yᴇs' if settings["welcome"] else '❌ Nᴏ',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)
    await query.answer(' ˆ°• Tᴀᴍɪʟᴀɴ BᴏᴛsZ •°ˆ ')


async def auto_filter(client, msg, spoll=False):
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:
            search = message.text
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:
                await client.send_message(file_req_channel,f"-🦋 #REQUESTED_FILE 🦋-\n\n📝Fɪʟᴇ Nᴀᴍᴇ :{search}\n\nRᴇǫᴜᴇsᴛᴇᴅ Bʏ: {message.from_user.first_name}\n\n Usᴇʀ Iᴅ :{message.from_user.id}\n\n🗃Cᴏᴅᴇᴅᴇᴅ Bʏ  @Tamilan_BotsZ",
                                                                                                       reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔺 Fɪʟᴇ Uᴩʟᴏᴀᴅᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ 🔺", callback_data="close_data")]]))
                l = await message.reply_text(text=f"△ Hᴇʏ Fʀɪᴇɴᴅ {message.from_user.first_name} 😎,\n\nʏᴏᴜʀ ʀᴇQᴜᴇꜱᴛ ʜᴀꜱ ʙᴇᴇɴ ꜱᴇɴᴛ ᴛᴏ ᴏᴜʀ ᴀᴅᴍɪɴ'ꜱ ᴅᴀꜱʜʙᴏᴀʀᴅ !\n\nᴘʟᴇᴀꜱᴇ ᴋᴇᴇᴘ ꜱᴏᴍᴇ ᴘᴀᴛɪᴇɴᴄᴇ !\nᴛʜᴇʏ ᴡɪʟʟ ᴜᴘʟᴏᴀᴅ ɪᴛ ᴀꜱ ꜱᴏᴏɴ ᴀꜱ ᴘᴏꜱꜱɪʙʟᴇ.\n\n➟ 📝Cᴏɴᴛᴇɴᴛ Nᴀᴍᴇ : {search}\n\n➟ 👮 Rᴇǫᴜᴇsᴛᴇᴅ Bʏ Yᴏᴜ : {message.from_user.first_name}\n\n༺ @TamilanBotsZSupport༻\n\n🦋・‥☆Sᴜᴩᴩᴏʀᴛ Oᴜʀ Cʜᴀɴɴᴇʟ ☆‥・🦋\n╰┈➤・☆ @SharathItsIsMe ☆",
                                                                                                       reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("━ • │▌║  Aᴅᴅ Mᴇ Tᴏ Uʀ Gʀᴏᴜᴩ  ║▌│ • ━", url=f'http://t.me/{temp.U_NAME}?startgroup=true')],[InlineKeyboardButton("✪ Tᴀᴍɪʟᴀɴ Bᴏᴛs ✪", url="https://t.me/Tamilan_BotsZ"), InlineKeyboardButton("✪ Sᴜᴩᴩᴏʀᴛ Gʀᴏᴜᴩ ✪", url="https://t.me/TamilanBotsZ_Support"), InlineKeyboardButton("✪ Rᴇᴩᴏ ✪", url="https://Github.com/TamilanBotsZ/PremiumFilter")],[InlineKeyboardButton("╚»♥️Dᴇʟᴇᴛᴇ Tʜɪs Mᴇssᴀɢᴇ ♥️«╝", callback_data="close_data")]]))
                await asyncio.sleep(12)
                await l.delete()
                if settings["spell_check"]:
                    return await advantage_spell_chok(msg)
                else:
                    return
        else:
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}",
                    callback_data=f'{pre}#{file.file_id}',
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'{pre}#{file.file_id}',
                ),
            ]
            for file in files
        ]      
    
    if offset != "":
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton(text=f"🗓 1/{math.ceil(int(total_results) / 10)}", callback_data="pages"),
             InlineKeyboardButton(text="Nᴇxᴛ ›››", callback_data=f"next_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="🗓 1/1", callback_data="pages")]
        )
    btn.insert(0, [
        InlineKeyboardButton("😌 Cʜᴇᴄᴋ Bᴏᴛ PM 😌", url=f"https://t.me/{temp.U_NAME}")
    ])
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        cap = f"<b>😙Rᴇǫᴜᴇsᴛᴇᴅ Bʏ : {message.from_user.mention} \n\n😊 Yᴏᴜʀ Qᴜᴇʀʏ : {search} \n\n📂Tᴏᴛᴀʟ Fɪʟᴇs Fᴏᴜɴᴅᴇᴅ : {str(total_results)}</b>"
    if imdb and imdb.get('poster'):
        try:
            hehe =  await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024],
                                      reply_markup=InlineKeyboardMarkup(btn))
            if AUTO_DELETE:
                await asyncio.sleep(AUTO_DELETE_SECONDS)
                await hehe.delete()

        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            hmm = await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
            if AUTO_DELETE:
                await asyncio.sleep(AUTO_DELETE_SECONDS)
                await hmm.delete()
        except Exception as e:
            logger.exception(e)
            fek = await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
            if AUTO_DELETE:
                await asyncio.sleep(AUTO_DELETE_SECONDS)
                await fek.delete()
    else:
        fuk = await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
        if AUTO_DELETE:
            await asyncio.sleep(AUTO_DELETE_SECONDS)
            await fuk.delete()


async def advantage_spell_chok(msg):
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    query = query.strip() + " movie"
    g_s = await search_gagala(query)
    g_s += await search_gagala(msg.text)
    gs_parsed = []
    if not g_s:
        k = await msg.reply("I couldn't find any movie in that name.")
        await asyncio.sleep(8)
        await k.delete()
        return
    regex = re.compile(r".*(imdb|wikipedia).*", re.IGNORECASE)  # look for imdb / wiki results
    gs = list(filter(regex.match, g_s))
    gs_parsed = [re.sub(
        r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)',
        '', i, flags=re.IGNORECASE) for i in gs]
    if not gs_parsed:
        reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*",
                         re.IGNORECASE)  # match something like Watch Niram | Amazon Prime
        for mv in g_s:
            match = reg.match(mv)
            if match:
                gs_parsed.append(match.group(1))
    user = msg.from_user.id if msg.from_user else 0
    movielist = []
    gs_parsed = list(dict.fromkeys(gs_parsed))  # removing duplicates https://stackoverflow.com/a/7961425
    if len(gs_parsed) > 3:
        gs_parsed = gs_parsed[:3]
    if gs_parsed:
        for mov in gs_parsed:
            imdb_s = await get_poster(mov.strip(), bulk=True)  # searching each keyword in imdb
            if imdb_s:
                movielist += [movie.get('title') for movie in imdb_s]
    movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
    movielist = list(dict.fromkeys(movielist))  # removing duplicates
    if not movielist:
        k = await msg.reply("I couldn't find anything related to that. Check your spelling")
        await asyncio.sleep(8)
        await k.delete()
        return
    SPELL_CHECK[msg.id] = movielist
    btn = [[
        InlineKeyboardButton(
            text=movie.strip(),
            callback_data=f"spolling#{user}#{k}",
        )
    ] for k, movie in enumerate(movielist)]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'spolling#{user}#close_spellcheck')])
    await msg.reply("I couldn't find anything related to that\nDid you mean any one of these?",
                    reply_markup=InlineKeyboardMarkup(btn))


async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await client.send_message(group_id, reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                    elif btn == "[]":
                        await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                    else:
                        button = eval(btn)
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False
