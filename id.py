# -*- coding: utf-8 -*-

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

            await message.edit("🖼 <b>Profil rasmi olinmoqda...</b>", parse_mode="html")

            # 1. Target user aniqlash
            if reply:
                user = await reply.get_sender()
            elif len(args) > 1:
                user = await self.client.get_entity(args[1])
            else:
                user = await message.get_sender()

            if not user:
                return await message.edit(
                    "❌ <b>Foydalanuvchi aniqlanmadi.</b>",
                    parse_mode="html"
                )

            # 2. Profil rasmi bor-yo‘qligini tekshirish
            if not getattr(user, "photo", None):
                return await message.edit(
                    "❌ <b>Bu foydalanuvchida profil rasmi yo‘q.</b>",
                    parse_mode="html"
                )

            # 3. Full user info (bio uchun)
            try:
                full = await self.client(GetFullUserRequest(user.id))
                bio = full.full_user.about or "Mavjud emas"
            except:
                bio = "Mavjud emas"

            # 4. Eng oxirgi profil rasmini olish (ENG STABIL USUL)
            photo = await self.client.download_profile_photo(
                user,
                file=bytes
            )

            if not photo:
                return await message.edit(
                    "❌ <b>Profil rasmini yuklab bo‘lmadi.</b>",
                    parse_mode="html"
                )

            # 5. Yuborish
            caption = (
                "🖼 <b>Profil rasmi</b>\n\n"
                f"👤 <b>Foydalanuvchi:</b> {get_display_name(user)}\n"
                f"🆔 <b>ID:</b> <code>{user.id}</code>\n"
                f"📝 <b>Bio:</b>\n<code>{bio}</code>"
            )

            await message.delete()
            await self.client.send_file(
                message.chat_id,
                photo,
                caption=caption,
                parse_mode="html"
            )

        except Exception as e:
            try:
                await message.edit(
                    f"❌ <b>Xatolik:</b> <code>{e}</code>",
                    parse_mode="html"
                )
            except:
                pass
