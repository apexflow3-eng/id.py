# -*- coding: utf-8 -*-
"""
================================================================================
Modul: AccountInfoModule
Funksiya: Akkaunt yoki user haqida keng qamrovli ma'lumot berish (.info)
================================================================================
"""
import time
from telethon.tl.functions.users import GetFullUserRequest

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
            except:
                return await message.edit("❌ Akkaunt (username/ID) topilmadi.")
        else:
            # Akkauntni o'zimiznikini olish
            user_entity = await message.get_sender()
            
        if not user_entity: 
            return await message.edit("❌ Ma'lumot olinmadi.")
        
        await message.edit("🔄 Akkaunt ma'lumotlari yig'ilmoqda...")
        
        try:
            # 2. To'liq ma'lumot olish (Bio, Status, va h.k.)
            full_info = await self.client(GetFullUserRequest(user_entity.id))
            user = full_info.users[0]
            full_user = full_info.full_user
            
            # 3. Ma'lumotlarni tahlil qilish
            
            # User turi
            user_type = "Bot 🤖" if user.bot else "User 🧑‍💻"
            if user.premium: user_type += " (Premium 🌟)"
            
            # Oxirgi ko'rgan vaqti (Status)
            if isinstance(full_user.status, types.UserStatusOnline):
                status = "🟢 Online"
            elif isinstance(full_user.status, types.UserStatusOffline):
                last_seen_ts = full_user.status.was_online.timestamp()
                now_ts = time.time()
                diff_ms = (now_ts - last_seen_ts) * 1000
                last_seen = self.utils.time_formatter(diff_ms)
                status = f"🔴 Offline (Oxirgi: {last_seen} avval)"
            else:
                 status = "⚫️ Status: Yashirin"
            
            # Katta matnni tuzish
            caption = f"👤 **AKKAUNT MA'LUMOTI**\n"
            caption += f"➖➖➖➖➖➖➖➖➖➖\n"
            caption += f"**ID:** `{user.id}`\n"
            caption += f"**Ism:** {user.first_name} {user.last_name or ''}\n"
            caption += f"**Username:** @{user.username or 'Mavjud emas'}\n"
            caption += f"**Turi:** {user_type}\n"
            caption += f"**Status:** {status}\n"
            caption += f"**DC ID:** `{getattr(user.photo, 'dc_id', 'Noma\'lum')}`\n"
            caption += f"**Bio:**\n`{full_user.about or 'Bio bo\'sh.'}`\n"
            
            await message.edit(caption)
            
        except Exception as e:
            # Xato (masalan, akkaunt o'chirilgan bo'lishi mumkin)
            await message.edit(f"❌ Akkaunt ma'lumotlarini olishda xato yuz berdi: {e}")