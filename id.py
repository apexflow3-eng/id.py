# -*- coding: utf-8 -*-
from .. import loader, utils
from telethon import types
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_display_name
import time

@loader.tds
class AccountInfoMod(loader.Module):
    """Akkaunt haqida ma'lumot (.info)"""
    
    # Modul nomi aniq ko'rsatilgan
    strings = {"name": "AccountInfo"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def infocmd(self, message):
        """<reply yoki username> - User haqida to'liq ma'lumot"""
        
        # Argumentlarni olish
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        
        user = None
        
        try:
            if reply:
                user = await reply.get_sender()
            elif args:
                user = await self.client.get_entity(args)
            else:
                user = await message.get_sender()
        except Exception:
            await message.edit("<b>❌ Bunday foydalanuvchi topilmadi!</b>")
            return

        if not user:
            await message.edit("<b>❌ Ma'lumot olishning iloji bo'lmadi.</b>")
            return

        await message.edit("<b>🔄 Ma'lumotlar yuklanmoqda...</b>")

        try:
            # To'liq ma'lumotni tortib olish
            full_user = await self.client(GetFullUserRequest(user.id))
            user_info = full_user.full_user
            
            # Asosiy user obyekti
            u = full_user.users[0]

            # Tahlil
            user_type = "Bot 🤖" if u.bot else "Odam 👤"
            if u.premium: user_type += " (Premium ✨)"
            if u.scam: user_type += " (Scam ⚠️)"
            
            # Status
            status = "Noma'lum"
            if isinstance(u.status, types.UserStatusOnline):
                status = "🟢 Online"
            elif isinstance(u.status, types.UserStatusOffline):
                was_online = u.status.was_online.timestamp()
                diff = time.time() - was_online
                
                # Vaqtni hisoblash
                minutes = int(diff / 60)
                hours = int(minutes / 60)
                days = int(hours / 24)
                
                if days > 0: vaqt = f"{days} kun"
                elif hours > 0: vaqt = f"{hours} soat"
                elif minutes > 0: vaqt = f"{minutes} daqiqa"
                else: vaqt = "bir oz"
                
                status = f"🔴 Offline ({vaqt} oldin)"
            
            # Bio
            bio = user_info.about if user_info.about else "Mavjud emas"
            
            # DC ID (Suratdan olish)
            dc_id = u.photo.dc_id if u.photo else "Yo'q"

            # Natija
            text = (
                f"👤 <b>Foydalanuvchi:</b> {get_display_name(u)}\n"
                f"🆔 <b>ID:</b> <code>{u.id}</code>\n"
                f"🔗 <b>Username:</b> @{u.username if u.username else 'Yoq'}\n"
                f"🎭 <b>Turi:</b> {user_type}\n"
                f"📡 <b>Status:</b> {status}\n"
                f"🌐 <b>DC:</b> {dc_id}\n\n"
                f"📝 <b>Bio:</b>\n<code>{bio}</code>"
            )
            
            await message.edit(text)

        except Exception as e:
            await message.edit(f"<b>❌ Xatolik yuz berdi:</b> {str(e)}")
