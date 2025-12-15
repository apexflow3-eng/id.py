# -*- coding: utf-8 -*-
from telethon import types
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import get_display_name

class Userbot:
    """
    .pfp <reply/username>
    Foydalanuvchining oxirgi profil rasmini chiqaradi
    """

    def __init__(self, client):
        self.client = client

    async def pfp(self, message):
        try:
            args = message.text.split(maxsplit=1)
            reply = await message.get_reply_message()

            await message.edit("🖼 <b>Profil rasmi olinmoqda...</b>", parse_mode='html')

            # 1. Target user aniqlash
            if reply:
                user = await reply.get_sender()
            elif len(args) > 1:
                try:
                    user = await self.client.get_entity(args[1])
                except:
                    return await message.edit("❌ <b>Foydalanuvchi topilmadi.</b>", parse_mode='html')
            else:
                user = await message.get_sender()

            if not user:
                return await message.edit("❌ <b>User aniqlanmadi.</b>", parse_mode='html')

            # 2. Profil rasmi bor-yo‘qligini tekshirish
            if not user.photo:
                return await message.edit("❌ <b>Bu foydalanuvchida profil rasmi yo‘q.</b>", parse_mode='html')

            # 3. Full user info (bio uchun)
            full = await self.client(GetFullUserRequest(user.id))
            bio = full.full_user.about or "Mavjud emas"

            # 4. Eng oxirgi profil rasmini olish
            photo = await self.client.download_profile_photo(
                user,
                file=bytes
            )

            # 5. Yuborish
            caption = (
                f"🖼 <b>Profil rasmi</b>\n\n"
                f"👤 <b>Foydalanuvchi:</b> {get_display_name(user)}\n"
                f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
                f"📝 <b>Bio:</b>\n<code>{bio}</code>"
            )

            await message.delete()
            await self.client.send_file(
                message.chat_id,
                photo,
                caption=caption,
                parse_mode='html'
            )

        except Exception as e:
            await message.edit(f"❌ <b>Xatolik:</b> {e}", parse_mode='html')
