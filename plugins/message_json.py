from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command(['json', 'message'], ['.', '!']))
def json_cmd(client: Client, message: Message):
    if 'here' in message.text:
        message.reply_text(str(message.reply_to_message), parse_mode=None)
    else:
        client.send_message('me', str(message.reply_to_message), parse_mode=None)
