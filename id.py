# -*- coding: utf-8 -*-
"""
================================================================================
Modul: AccountInfoModule
Funksiya: Akkaunt yoki user haqida keng qamrovli ma'lumot berish (.info)
================================================================================
"""
import time
import asyncio
from telethon import types  # UserStatus turlarini olish uchun muhim
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_display_name

class AccountInfoModule:
    """
    Akkaunt va foydalanuvchi ma'lumotlarini chiqarish moduli.
    Asosiy buyruq: .info
    """

    async def infocmd(self, message):
        """
        Akkaunt haqida to'liq ma'lumot chiqarish.
        Ishlatish: .info yoki Reply qiling (boshqa user uchun)
        """
        args = self.utils.get_args_list(message)
        reply = await message.get_reply_message()
        
        user_entity = None
        
        # 1. Userni aniqlash
        if reply:
            user_entity = await reply.get_sender()
        elif args:
            try:
                # Username yoki ID orqali qidirish
                user_entity = await self.client.get_entity(args[0])
            except Exception:
                return await message.edit("❌ Akkaunt (username/ID) topilmadi.")
        else:
            # Argument va reply bo'lmasa, o'zimizning ma'lumotimizni olamiz
            user_entity = await message.get_sender()
            
        if not user_entity: 
            return await message.edit("❌ Ma'lumot olinmadi.")
        
        await message.edit("🔄 Akkaunt ma'lumotlari yig'ilmoqda...")
        
        try:
            # 2. To'liq ma'lumot olish (Bio, Status, va h.k.)
            # GetFullUserRequest ko'p ma'lumot beradi
            full_info = await self.client(GetFullUserRequest(user_entity.id))
            user = full_info.users[0]
            full_user = full_info.full_user
            
            # 3. Ma'lumotlarni tahlil qilish
            
            # User turi (Botmi, User, Premium)
            user_type = "Bot 🤖" if user.bot else "User 🧑‍💻"
            if user.premium: 
                user_type += " (Premium 🌟)"
            if user.scam:
                user_type += " (Scam ⚠️)"
            if user.fake:
                user_type += " (Fake 🚫)"
            
            # Oxirgi ko'rgan vaqti (Status)
            status = "Noma'lum"
            if isinstance(user.status, types.UserStatusOnline):
                status = "🟢 Online"
            elif isinstance(user.status, types.UserStatusOffline):
                last_seen_ts = user.status.was_online.timestamp()
                now_ts = time.time()
                # Millisekund hisobi (self.utils funksiyasi uchun)
                diff_ms = (now_ts - last_seen_ts) * 1000
                last_seen_str = self.utils.time_formatter(diff_ms)
                status = f"🔴 Offline (Oxirgi: {last_seen_str} avval)"
            elif isinstance(user.status, types.UserStatusRecently):
                status = "🟡 Yaqinda kirgan"
            elif isinstance(user.status, types.UserStatusLastWeek):
                status = "🟡 O'tgan hafta kirgan"
            elif isinstance(user.status, types.UserStatusLastMonth):
                status = "🟡 O'tgan oy kirgan"
            else:
                status = "⚫️ Status yashirin"
            
            # DC ID (Data Center ID)
            dc_id = "Noma'lum"
            if user.photo:
                # Userning profil rasmidan DC ID ni olish
                dc_id = getattr(user.photo, 'dc_id', 'Noma\'lum')

            # Bio (About)
            bio = full_user.about if full_user.about else "Bio bo'sh."

            # Ism (Display Name)
            full_name = get_display_name(user)

            # Katta matnni tuzish
            caption = f"👤 **AKKAUNT MA'LUMOTI**\n"
            caption += f"➖➖➖➖➖➖➖➖➖➖\n"
            caption += f"🆔 **ID:** `{user.id}`\n"
            caption += f"👤 **Ism:** {full_name}\n"
            caption += f"🔗 **Username:** @{user.username or 'Mavjud emas'}\n"
            caption += f"🎭 **Turi:** {user_type}\n"
            caption += f"📡 **Status:** {status}\n"
            caption += f"🌐 **DC ID:** `{dc_id}`\n"
            caption += f"📝 **Bio:**\n`{bio}`\n"
            
            await message.edit(caption)
            
        except Exception as e:
            # Xato (masalan, akkaunt o'chirilgan yoki maxfiylik sozlamalari)
            await message.edit(f"❌ Akkaunt ma'lumotlarini olishda xato yuz berdi: {e}")
