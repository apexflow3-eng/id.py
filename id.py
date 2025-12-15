# -*- coding: utf-8 -*-
"""
================================================================================
Modul: AccountInfo
Funksiya: Akkaunt yoki user haqida keng qamrovli ma'lumot berish (.info)
================================================================================
"""
import time
from telethon import types
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_display_name

# Userbot ishlashi uchun kerakli kutubxonalar
from .. import loader, utils

@loader.tds
class AccountInfoMod(loader.Module):
    """Akkaunt va foydalanuvchi ma'lumotlarini chiqarish moduli."""
    
    # Modul nomi (Userbot shu nom bilan taniydi)
    strings = {"name": "AccountInfo"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def infocmd(self, message):
        """
        .info <reply/username> - Akkaunt haqida to'liq ma'lumot olish.
        """
        # Argumentlarni olish (FT usuli)
        args = utils.get_args_raw(message)

        reply = await message.get_reply_message()
        
        user_entity = None
        
        # 1. Userni aniqlash
        if reply:
            user_entity = await reply.get_sender()
        elif args:
            try:
                # Username yoki ID orqali qidirish
                user_entity = await self.client.get_entity(args)
            except Exception:
                return await message.edit("❌ <b>Akkaunt (username/ID) topilmadi.</b>")
        else:
            # Argument va reply bo'lmasa, o'zimizning ma'lumotimizni olamiz
            user_entity = await message.get_sender()
            
        if not user_entity: 
            return await message.edit("❌ <b>Ma'lumot olinmadi.</b>")
        
        await message.edit("🔄 <b>Akkaunt ma'lumotlari yig'ilmoqda...</b>")
        
        try:
            # 2. To'liq ma'lumot olish
            full_info = await self.client(GetFullUserRequest(user_entity.id))
            user = full_info.users[0]
            full_user = full_info.full_user
            
            # 3. Ma'lumotlarni tahlil qilish
            
            # User turi
            user_type = "Bot 🤖" if user.bot else "User 🧑‍💻"
            if user.premium: 
                user_type += " (Premium 🌟)"
            if user.scam:
                user_type += " (Scam ⚠️)"
            if user.fake:
                user_type += " (Fake 🚫)"
            
            # Status (Online/Offline)
            status = "Noma'lum"
            if isinstance(user.status, types.UserStatusOnline):
                status = "🟢 Online"
            elif isinstance(user.status, types.UserStatusOffline):
                last_seen_ts = user.status.was_online.timestamp()
                now_ts = time.time()
                diff_ms = (now_ts - last_seen_ts) * 1000
                
                # Vaqtni formatlash
                seconds = int(diff_ms / 1000)
                minutes, seconds = divmod(seconds, 60)
                hours, minutes = divmod(hours, 60)
                days, hours = divmod(hours, 24)
                
                if days > 0: last_seen_str = f"{days} kun"
                elif hours > 0: last_seen_str = f"{hours} soat"
                elif minutes > 0: last_seen_str = f"{minutes} daqiqa"
                else: last_seen_str = "bir oz"

                status = f"🔴 Offline ({last_seen_str} avval)"
            elif isinstance(user.status, types.UserStatusRecently):
                status = "🟡 Yaqinda kirgan"
            elif isinstance(user.status, types.UserStatusLastWeek):
                status = "🟡 O'tgan hafta kirgan"
            elif isinstance(user.status, types.UserStatusLastMonth):
                status = "🟡 O'tgan oy kirgan"
            else:
                status = "⚫️ Status yashirin"
            
            # DC ID
            dc_id = "Noma'lum"
            if user.photo:
                dc_id = getattr(user.photo, 'dc_id', 'Noma\'lum')

            # Bio
            bio = full_user.about if full_user.about else "Bio bo'sh."

            # Ism
            full_name = get_display_name(user)

            # Natijani chiqarish
            caption = f"👤 <b>AKKAUNT MA'LUMOTI</b>\n"
            caption += f"➖➖➖➖➖➖➖➖➖➖\n"
            caption += f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
            caption += f"👤 <b>Ism:</b> {full_name}\n"
            caption += f"🔗 <b>Username:</b> @{user.username or 'Mavjud emas'}\n"
            caption += f"🎭 <b>Turi:</b> {user_type}\n"
            caption += f"📡 <b>Status:</b> {status}\n"
            caption += f"🌐 <b>DC ID:</b> <code>{dc_id}</code>\n"
            caption += f"📝 <b>Bio:</b>\n<code>{bio}</code>\n"
            
            await message.edit(caption)
            
        except Exception as e:
            await message.edit(f"❌ <b>Xatolik:</b> {e}")
