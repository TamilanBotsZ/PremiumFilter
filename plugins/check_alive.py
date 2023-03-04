import time
import random
from pyrogram import Client, filters

CMD = ["/", "."]

@Client.on_message(filters.command("alive", CMD))
async def check_alive(_, message):
    await message.reply_text("Lᴜᴄᴋʟʏ I Aᴍ Aʟɪᴠᴇ :) Pʀᴇss 👉 /start \n\nPʀᴇss 👉 /help Fᴏʀ Hᴇʟᴩ ;)\n\n\nPʀᴇss 👉 /ping Tᴏ Cʜᴇᴄᴋ Mʏ Pɪɴɢ 😁")

@Client.on_message(filters.command("help", CMD))
async def help(_, message):
    await message.reply_text("Pʀᴇss 👉 /movie Fᴏʀ Hᴏᴡ Tᴏ Rᴇǫᴜᴇsᴛ Mᴏᴠɪᴇs Iɴ A Pʀᴏᴩᴇʀ Wᴀʏ 📃\n\nPʀᴇss 👉 /series Fᴏʀ Hᴏᴡ Tᴏ Rᴇǫᴜᴇsᴛ Sᴇʀɪᴇs Iɴ A Pʀᴏᴩᴇʀ Wᴀʏ 📃\n\n\nPʀᴇss 👉 /tutorial Fᴏʀ Tᴜᴛᴏʀɪᴀʟ Aʙᴏᴜᴛ Hᴏᴡ Tᴏ Gᴇᴛ Dɪʀᴇᴄᴛ Fɪʟᴇs Fʀᴏᴍ Mᴇ 🤗")


@Client.on_message(filters.command("movie", CMD))
async def movie(_, message):
    await message.reply_text("⚠️❗️ Mᴏᴠɪᴇ Rᴇǫᴜᴇsᴛ Fᴏʀᴍᴀᴛ❗️⚠️\n\n📝 ﹝ ᴏɴʟʏ sᴇɴᴅ ᴛʜᴇ ᴍᴏᴠɪᴇs ɴᴀᴍᴇ ᴡɪᴛʜ ᴄᴏʀʀᴇᴄᴛ ﹞ 📚\n\n🖇 Exᴀᴍᴩʟᴇ:\n\n• Robin Hood ✅\n• Ponniyan Selvan 250mb✅\n• Varisu 2023✅\n• Master Tam✅\n\n❌ DᴏɴˆT Usᴇ Aɴʏ Sʏᴍʙᴏʟs ﹝ ᴏɴʟʏ sᴇɴᴅ ᴛʜᴇ ᴍᴏᴠɪᴇs ɴᴀᴍᴇ ᴡɪᴛʜ ᴄᴏʀʀᴇᴄᴛ ﹞❌")

@Client.on_message(filters.command("series", CMD))
async def series(_, message):
    await message.reply_text("⚠️❗️ Sᴇʀɪᴇs Rᴇǫᴜᴇsᴛ Fᴏʀᴍᴀᴛ ❗️⚠️\n\n🗣﹝ ᴏɴʟʏ sᴇɴᴅ ᴛʜᴇ sᴇʀɪᴇs ɴᴀᴍᴇ ᴡɪᴛʜ ᴄᴏʀʀᴇᴄᴛ ﹞ 🧠\n\n🖇Exᴀᴍᴩʟᴇ: \n\n• Game Of Thrones Season Season 1✅\n• Sex Education episode 2✅ \n• Breaking Bad S01E05✅\n\n❌ DᴏɴˆT Usᴇ Aɴʏ Sʏᴍʙᴏʟs ﹝ ᴏɴʟʏ sᴇɴᴅ ᴛʜᴇ sᴇʀɪᴇs ɴᴀᴍᴇ ᴡɪᴛʜ ᴄᴏʀʀᴇᴄᴛ ﹞ ❌")

@Client.on_message(filters.command("download", CMD))
async def tutorial(_, message):
    await message.reply_text("Fɪʀsᴛ Sᴇᴇ Tʜɪʏᴜʏ")

@Client.on_message(filters.command("ping", CMD))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("...........")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"𝖯𝗂𝗇𝗀!\n{time_taken_s:.3f} ms")
