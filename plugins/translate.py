from os import environ
from typing import List

from pyrogram import Client, filters
from pyrogram.types import Message

from googletrans import Translator
from pycountry import languages


@Client.on_message(filters.command(['transl', 'translate', 'trans'], ['.', '!']))
def translate_cmd(client: Client, message: Message):
    def translate_text(text_to_translate: str, dest_lang: str = environ.get('LANGUAGE'), src_lang: str = 'DETECT'):
        translator = Translator()
        result: str = ''
        for i in range(20):
            try:
                if src_lang != 'DETECT':
                    result = translator.translate(text_to_translate, src=src_lang, dest=dest_lang).text
                else:
                    result = translator.translate(text_to_translate, dest=dest_lang).text
                break
            except Exception:
                translator = Translator()
        return result

    words: List[str] = message.text.split(' ')
    if len(words) == 1:
        text = translate_text(message.reply_to_message.text)
        message.edit_text(text if text != '' else "1Couldn't translate...")
        return
    if ':' in words[1]:
        try:
            langs: List[str] = words[1].split(':')
            src: str = languages.lookup(langs[0]).name
            dest: str = languages.lookup(langs[1]).name
            text = ' '.join(words[2:]) if len(words) > 2 else message.reply_to_message.text
            text = translate_text(text, dest, src)
            message.edit_text(text if text != '' else "2Couldn't translate...")
        except LookupError:
            message.edit_text("Couldn't find language...")
        except Exception:
            message.edit_text("3Couldn't translate...")
        return
    try:
        text = ' '.join(words[2:]) if len(words) > 2 else message.reply_to_message.text
        text = translate_text(text, languages.lookup(words[1]).name)
        message.edit_text(text if text != '' else "4Couldn't translate...")
    except LookupError:
        text = translate_text(message.text)
        message.edit_text(text if text != '' else "5Couldn't translate...")
