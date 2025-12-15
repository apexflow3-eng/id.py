# -*- coding: utf-8 -*-
import time
from telethon import types, events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_display_name

class Userbot:
    """
    Bu klass tizim tomonidan avtomatik o'qib olinadi.
    """
    def __init__(self, client):
        self.client = client

    # Buyruq nomi funksiya nomidan olinadi (info -> .info)
    async def info(self, message):
        """
        .info <reply/username> - Foydalanuvchi haqida to'liq ma'lumot
        """
        try:
            args = message.text.split(maxsplit=1)
            reply = await message.get_reply_message()
            
            user_entity = None
            
            await message.edit("🔄 <b>Ma'lumot olinmoqda...</b>", parse_mode='html')

            # 1. Kimning ma'lumotini olishni aniqlash
            if reply:
                user_entity = await reply.get_sender()
            elif len(args) > 1:
                try:
                    user_entity = await self.client.get_entity(args[1])
                except:
                    return await message.edit("❌ <b>Foydalanuvchi topilmadi.</b>", parse_mode='html')
            else:
                user_entity = await message.get_sender()
                
            if not user_entity:
                return await message.edit("❌ <b>Ma'lumot olish imkoni bo'lmadi.</b>", parse_mode='html')

            # 2. To'liq ma'lumotni API dan tortib olish
            full_info = await self.client(GetFullUserRequest(user_entity.id))
            user = full_info.users[0]
            full_user = full_info.full_user
            
            # 3. Tahlil
            user_type = "Bot 🤖" if user.bot else "User 🧑‍💻"
            if user.premium: user_type += " (Premium ✨)"
            if user.scam: user_type += " (Scam ⚠️)"
            
            # Status
            status = "Yashirin ⚫️"
            if isinstance(user.status, types.UserStatusOnline):
                status = "Online 🟢"
            elif isinstance(user.status, types.UserStatusOffline):
                was_online = user.status.was_online.timestamp()
                diff = time.time() - was_online
                m = int(diff / 60)
                h = int(m / 60)
                d = int(h / 24)
                if d > 0: vaqt = f"{d} kun"
                elif h > 0: vaqt = f"{h} soat"
                elif m > 0: vaqt = f"{m} daqiqa"
                else: vaqt = "bir oz"
                status = f"Offline ({vaqt} oldin) 🔴"
            
            # DC ID va Bio
            dc_id = getattr(user.photo, 'dc_id', 'Noma\'lum') if user.photo else "Yo'q"
            bio = full_user.about if full_user.about else "Mavjud emas"
            
            # 4. Javob
            text = (
                f"👤 <b>Foydalanuvchi:</b> {get_display_name(user)}\n"
                f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
                f"🔗 <b>Username:</b> @{user.username if user.username else 'Yoq'}\n"
                f"🎭 <b>Turi:</b> {user_type}\n"
                f"📡 <b>Status:</b> {status}\n"
                f"🌐 <b>DC ID:</b> {dc_id}\n\n"
                f"📝 <b>Bio:</b>\n<code>{bio}</code>"
            )
            
            await message.edit(text, parse_mode='html')

        except Exception as e:
            await message.edit(f"❌ <b>Xatolik:</b> {e}", parse_mode='html')
