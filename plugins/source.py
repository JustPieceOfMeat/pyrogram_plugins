from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command('source', list('!.')) & filters.me)
def on_source(client: Client, message: Message):
    message.edit_text('https://github.com/JustPieceOfMeat/pyrogram_plugins')
