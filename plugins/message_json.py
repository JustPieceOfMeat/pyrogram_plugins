from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.regex(r'^(ro)|(mute) ((\d+|(\d+\.\d+))[mhdw])+$'))
def read_only(client: Client, message: Message):