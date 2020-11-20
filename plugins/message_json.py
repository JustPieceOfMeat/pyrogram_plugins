import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
from os import getlogin
from pyrogram import Client, filters
from pyrogram.types import Message


def paste_code(content: str, author: str = getlogin()) -> str:  # from https://www.geany.org/p/help/api/
    fields = [('content', content), ('author', author), ('lexer', 'json')]
    encoded_data = urllib.parse.urlencode(fields).encode('utf-8')
    request = urllib.request.Request(
        'https://www.geany.org/p/api/',
        encoded_data,
    )
    response = urllib.request.urlopen(request)
    response_content = response.read()
    return response_content.decode()


@Client.on_message(filters.command(['json', 'message', 'src'], ['.', '!']) & filters.me)
def json_cmd(client: Client, message: Message):
    message.edit(paste_code(str(message.reply_to_message), client.get_me().username or client.get_me().first_name))
