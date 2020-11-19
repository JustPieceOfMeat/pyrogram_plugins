from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command('purge', ['.', '!']) & filters.me & filters.reply)
def purge(client: Client, message: Message):
    messages = client.iter_history(message.chat.id, offset_id=message.reply_to_message.message_id, reverse=True)
    for message in messages:
        client.delete_messages(message.chat.id, message.message_id)
