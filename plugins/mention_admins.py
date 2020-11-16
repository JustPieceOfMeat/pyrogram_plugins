from time import sleep

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors.exceptions.flood_420 import SlowmodeWait


@Client.on_message(filters.command(['admin', 'admins'], '@') & filters.me)
def mention_admins(client: Client, message: Message):
    message.delete()
    message_text = message.text
    for admin in client.iter_chat_members(message.chat.id, 0, '', 'administrators'):
        message_text += f'<a href="tg://user?id={admin.user.id}">&#8203;</a>'   # add invisible mention to message text
    try:
        client.send_message(message.chat.id, message_text)
    except SlowmodeWait as e:   # if slow mode enabled
        sleep(e.x)
        client.send_message(message.chat.id, message_text)
