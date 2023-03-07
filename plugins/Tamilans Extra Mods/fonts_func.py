import os
import shutil
from pyrogram import Client, filters, enums
from telegraph import upload_file
from info import TMP_DOWNLOAD_DIRECTORY
from plugins.helper_functions.cust_p_filters import f_onw_fliter
from plugins.helper_functions.get_file_id import get_file_id


@Client.on_message(
    filters.command("telegraph") &
    f_onw_fliter
)
async def telegraph(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply_text("Sᴇɴᴅ Aɴʏ Pʜᴏᴛᴏ/Vɪᴅᴇᴏ Uɴᴅᴇʀ 5ᴍʙ Aɴᴅ Rᴇᴩʟʏ Wɪᴛʜ U Sᴇɴᴅᴇᴅ Fɪʟᴇ /telegraph .")
        return
    file_info = get_file_id(replied)
    if not file_info:
        await message.reply_text("Nᴏᴛ Sᴜᴩᴩᴏʀᴛᴇᴅ Mᴇᴅɪᴀ !")
        return
    _t = os.path.join(
        TMP_DOWNLOAD_DIRECTORY,
        str(replied.id)
    )
    if not os.path.isdir(_t):
        os.makedirs(_t)
    _t += "/"
    download_location = await replied.download(
        _t
    )
    try:
        response = upload_file(download_location)
    except Exception as document:
        await message.reply_text(message, text=document)
    else:
        await message.reply(
            f"Link :- <code>https://telegra.ph{response[0]}</code>",
            disable_web_page_preview=True
        )
    finally:
        shutil.rmtree(
            _t,
            ignore_errors=True
        )
