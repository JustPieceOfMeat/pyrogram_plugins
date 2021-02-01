from time import sleep

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, RPCError


@Client.on_message(filters.command('purge', ['.', '!']) & filters.me & filters.reply)
def purge(client: Client, message: Message):
    messages = client.iter_history(message.chat.id, offset_id=message.reply_to_message.message_id, reverse=True)
    for msg in messages:
        try:
            message.delete()
        except FloodWait as e:
            sleep(e.x)
        except RPCError as e:
            continue
