class script(object):
    START_TXT = """<b>Hᴇʏ {} ɪᴍ 『 ᴍᴏᴠɪᴇs ғɪʟᴛᴇʀ ʙᴏᴛ 』 ᴀɴ Aᴡᴇsᴏᴍᴇ Aᴜᴛᴏ + Mᴀɴᴜᴀʟ Fɪʟᴛᴇʀ + Fɪʟᴇ Sʜᴀʀᴇ Bᴏᴛ.
Aᴅᴅ Mᴇ Tᴏ Yᴏᴜʀ Gʀᴏᴜᴩ Nᴏᴡ 👇</b>"""

    HELP_TXT = """<b>Hᴇʏ {} Fʀɪᴇɴᴅ Hᴇʀᴇ Yᴏᴜʀ Bᴜᴛᴛᴏɴs 👇.</b>"""

    PRIVATEBOT_TXT = """<b>Tʜᴀɴᴋs Fᴏʀ Aᴅᴅɪɴɢ Mᴇ

- ›› Mᴜsᴛ Aᴅᴅ Mᴇ Aᴅᴍɪɴ Tᴏ Wᴏʀᴋ Oɴ Tʜɪs Gʀᴏᴜᴘ

- ›› Cʜᴀɴɢᴇ Sᴇᴛᴛɪɴɢ Fᴏʀ Uʀ Gʀᴏᴜᴘ Cʟɪᴄᴋ 👉 /connect

- ›› I Wɪʟʟ Pʀᴏᴠɪᴅᴇ Mᴏᴠɪᴇs/Sᴇʀɪᴇs Dᴏɴ'ᴛ Wᴏʀʀʏ

- ›› Eɴᴊᴏʏ !! Mᴏʀᴇ Iɴғᴏ Usᴇ Uɴᴅᴇʀ Bᴜᴛᴛᴏɴs</b>
"""

    METHOD_TXT ﹦ """﹤b﹥Pʀᴇss 👉 /movies Fᴏʀ Hᴏᴡ Tᴏ Rᴇǫᴜᴇsᴛ Mᴏᴠɪᴇs Iɴ A Pʀᴏᴩᴇʀ Wᴀʏ 📃.\nPʀᴇss 👉 /series Fᴏʀ Hᴏᴡ Tᴏ Rᴇǫᴜᴇsᴛ Sᴇʀɪᴇs Iɴ A Pʀᴏᴩᴇʀ Wᴀʏ 📃.\nPʀᴇss 👉 /tutorial Fᴏʀ Tᴜᴛᴏʀɪᴀʟ Aʙᴏᴜᴛ Hᴏᴡ Tᴏ Gᴇᴛ Dɪʀᴇᴄᴛ Fɪʟᴇs Fʀᴏᴍ Mᴇ 🤗 @Tamilan_BotsZ</b>"""

    MREQ_TXT ﹦ """﹤b﹥⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nᴍᴏᴠɪᴇ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n\nɢᴏ ᴛᴏ ɢᴏᴏɢʟᴇ ➠ ᴛʏᴘᴇ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ➠ ᴄᴏᴘʏ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ ➠ ᴘᴀꜱᴛᴇ ᴛʜɪꜱ ɢʀᴏᴜᴘ\n\nᴇxᴀᴍᴘʟᴇ : ᴀᴠᴀᴛᴀʀ: ᴛʜᴇ ᴡᴀʏ ᴏғ ᴡᴀᴛᴇʀ\n\n🚯 ᴅᴏɴᴛ ᴜꜱᴇ ➠ ':(!,./)\n\nᴄᴏᴅᴇᴅ ʙʏ ᴛᴀᴍɪʟᴀɴʙᴏᴛsᴢ</b>"""

    SREQ_TXT = """﹤b﹥⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nꜱᴇʀɪᴇꜱ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n\nɢᴏ ᴛᴏ ɢᴏᴏɢʟᴇ ➠ ᴛʏᴘᴇ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ➠ ᴄᴏᴘʏ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ ➠ ᴘᴀꜱᴛᴇ ᴛʜɪꜱ ɢʀᴏᴜᴘ\n\nᴇxᴀᴍᴘʟᴇ : ᴍᴏɴᴇʏ ʜᴇɪsᴛ S01E01\n\n🚯 ᴅᴏɴᴛ ᴜꜱᴇ ➠ ':(!,./)\n\nᴄᴏᴅᴇᴅ ʙʏ ᴛᴀᴍɪʟᴀɴʙᴏᴛsᴢ</b>"""
   
    MODS_TXT = """<b>I Hᴀᴠᴇ Mᴀɴʏ Fᴇᴀᴛᴜʀᴇs 🙌👇.﹤/b>"""

    PONG_TXT = """<b>Cʜᴇᴄᴋ Mʏ Pɪɴɢ Bʏ Cʟɪᴄᴋɪɴɢ 👉 /ping </b>"""

    ABOUT_TXT = """<b>🤖 ᴍʏ ɴᴀᴍᴇ : <a href=https://t.me/Tamilanz_Auto_Filter_Bot>ᴍᴏᴠɪᴇs ғɪʟᴛᴇʀ ʙᴏᴛ</a>
👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href=https://t.me/Sharathitsisme>sʜᴀʀᴀᴛʜ</a>
📝 ʟᴀɴɢᴜᴀɢᴇ : ᴘʏʀᴏɢʀᴀᴍ
📚 ꜰʀᴀᴍᴇᴡᴏʀᴋ : ᴘʏᴛʜᴏɴ 3
📡 ʜᴏsᴛᴇᴅ ᴏɴ : ﹤a href=https://t.me/Sharath_Links/31>24/7 ғʀᴇᴇ ʜᴏsᴛɪɴɢ</a>
📢 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ : <a href=https://t.me/TamilanMoviesChat>ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>
🌟 Sᴏᴜʀᴄᴇ Cᴏᴅᴇ : Pʀɪᴠᴀᴛᴇ °ᴩᴀɪᴅ° </b>"""

    SOURCE_TXT = """<b> Tʜɪs Is Aɴ Oᴩᴇɴ-Sᴏᴜʀᴄᴇ Pʀᴏᴊᴇᴄᴛ Bʏ @Tamilan_BotsZ</b>
<b>100﹪ Cᴏᴅᴇᴅ Bʏ <a href=https://t.me/SharathItsIsme>sʜᴀʀᴀᴛʜ</a></b>
<b>Rᴇᴩᴏ Lɪɴᴋ 👏🙌👇.﹤/b﹥"""

    FONT_TXT = """<b>I Cᴀɴ Gᴇɴᴇʀᴀᴛᴇ Aᴛᴛʀᴀᴄᴛɪᴠᴇ Fᴏɴᴛs Fᴏʀ Yᴏᴜʀ Tᴇxᴛ Sᴇɴᴅ Lɪᴋᴇ Tʜɪs 👇
- ᴇɢ :- /font hi da﹤/b﹥"""

    CARBON_TXT = """<b /carbon ﹛ ʏᴏᴜʀ ᴛᴇxᴛ ﹜
ᴇɢ :- /carbon hi ﹤/b﹥"""

    SHARE_TXT = """<b>/share ﹛ ʏᴏᴜʀ ᴛᴇxᴛ ﹜
ᴇɢ :- /share hi da﹤/b﹥"""

    VIDEO_TXT ="""Dᴏᴡɴʟᴏᴀᴅ Aɴʏ Yᴏᴜᴛᴜʙᴇ Vɪᴅᴇᴏ Fʀᴏᴍ Tʜᴇ Vɪᴅᴇᴏ Lɪɴᴋ

• Hᴏᴡ Tᴏ Usᴇ
• • Tʏᴘᴇ /video 𝘈𝘯𝘥 (YᴏᴜTᴜʙᴇ Vɪᴅᴇᴏ Lɪɴᴋ)
• Exᴀᴍᴘʟᴇ:
• <code>/video https://youtu.be/kB9TkCscX0</code>"""

    TELE_TXT = """<b>▫️Hᴇʟᴘ: ▪️ Tᴇʟᴇɢʀᴀᴘʜ ▪️</b>
     Tᴇʟᴇɢʀᴀᴘʜ Lɪɴᴋ Gᴇɴᴇʀᴀᴛᴏʀ
    </b>Usᴀɢᴇ</b>
    🤧 /telegraph - Sᴇɴᴅ Mᴇ Pʜᴏᴛᴏ Oʀ Vɪᴅᴇᴏ Uɴᴅᴇʀ (5ᴍʙ)"""

    MANUELFILTER_TXT = """<b> Hᴏᴡ Tᴏ Dᴏᴡɴʟᴏᴀᴅ Mᴏᴠɪᴇs / Sᴇʀɪᴇs Usɪɴɢ Tʜɪs Bᴏᴛ 😌 🔋</b>

<b>Fɪʀsᴛ Jᴏɪɴ Tʜɪs Gʀᴏᴜᴩ » @TamilanMoviesChat</b>

<b>Sᴇɴᴅ Yᴏᴜ Wᴀɴᴛ Mᴏᴠɪᴇs Oʀ Sᴇʀɪᴇs Nᴀᴍᴇ Wɪᴛʜ Cᴏʀʀᴇᴄᴛ Sᴩᴇʟʟɪɴɢ</b>

<b>Aɴᴅ Bᴏᴛ Wɪʟʟ Sᴇɴᴅ Yᴏᴜ Asᴋᴇᴅ Fɪʟᴇ</b>

<b>Hᴏᴡ Tᴏ Oᴩᴇɴ Bᴏᴛ Sᴇɴᴅᴇᴅ Fɪʟᴇ Lɪɴᴋ. » https://t.me/Sharath_Links/13 .﹤/b>
"""

    CONTACT_TXT = """<b> 
<b>»» ° Oɴʟʏ Cᴏɴᴛᴀᴄᴛ Fᴏʀ Pᴀɪᴅ Wᴏʀᴋs / Pʀᴏʙʟᴇᴍ / Dᴏᴜʙᴛ / Cᴏʟʟᴀʙ / Hᴇʟᴩ °</b>

<b>»» Iғ U Cᴏɴᴛᴀᴄᴛ Mᴇ Sᴇᴇ Bᴇʟᴏᴡ Bᴜᴛᴛᴏɴs 😙</b>
"""

    STATUS_TXT = """<b><u>Cᴜʀʀᴇɴᴛ Dᴀᴛᴀʙᴀsᴇ Sᴛᴀᴛᴜs</b></u>
    
<b>📑 ғɪʟᴇs sᴀᴠᴇᴅ: <code>{}</code>
👩🏻‍💻 ᴜsᴇʀs: <code>{}</code>
👥 ɢʀᴏᴜᴘs: <code>{}</code>
🗂️ ᴏᴄᴄᴜᴘɪᴇᴅ: <code>{}</code></b>
"""
    LOG_TEXT_G = """<b> #NewGroup
👥 ɢʀᴏᴜᴘ 👥 = {}(<code>{}</code>)
😇 ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs 😇 = <code>{}</code>
💌 ᴀᴅᴅᴇᴅ ʙʏ 💌 - {} </b>
"""
    LOG_TEXT_P = """<b> #NewUser
ɪᴅ ♥️- <code>{}</code>
ɴᴀᴍᴇ 💥- {} </b>
"""
