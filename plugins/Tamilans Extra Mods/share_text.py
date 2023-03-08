import os
from pyrogram import Client, filters
from urllib.parse import quote
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command(["share_text", "share", "sharetext",]))
async def share_text(client, message):
    reply = message.reply_to_message
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    input_split = message.text.split(None, 1)
    if len(input_split) == 2:
        input_text = input_split[1]
    elif reply and (reply.text or reply.caption):
        input_text = reply.text or reply.caption
    else:
        await message.reply_text(
            text=f"**Nᴏᴛɪᴄᴇ:**\n\n1. Rᴇᴩʟʏ Tᴏ Aɴʏ Mᴇssᴀɢᴇ.\n2. Nᴏ Mᴇᴅɪᴀ Sᴜᴩᴩᴏʀᴛ ﹝ sᴜᴩᴩᴏʀᴛs ᴏɴʟʏ ᴛᴇxᴛ ﹞\n\n**Jᴏɪɴ Nᴏᴡ Oᴜʀ Uᴩᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ**",                
            reply_to_message_id=reply_id,               
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🙌 Uᴩᴅᴀᴛᴇs 💥", url=f"https://t.me/Tamilan_BotsZ")]])
            )                                                   
        return
    await message.reply_text(
        text=f"**Hᴇʀᴇ Is Yᴏᴜʀ Sʜᴀʀɪɴɢ Tᴇxᴛ 👇**\n\nhttps://t.me/share/url?url=" + quote(input_text),
        reply_to_message_id=reply_id,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("♂️ Sʜᴀʀᴇ ", url=f"https://t.me/share/url?url={quote(input_text)}")]])       
    )
