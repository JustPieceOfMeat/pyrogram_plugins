from time import sleep

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait


@Client.on_message(filters.command('purge', ['.', '!']) & filters.me & filters.reply)
def purge(client: Client, message: Message):
    messages = client.iter_history(message.chat.id, offset_id=message.reply_to_message.message_id, reverse=True)
    for message in messages:
        try:
            if 'me' in message.command and not message.from_user.is_self:
                continue
            client.delete_messages(message.chat.id, message.message_id)
        except FloodWait as e:
            sleep(e.x)
        except Exception as e:
            message.edit("Unexpected error, can't continue...\n\n" + e)
            return
