from os import environ, path, remove
import re
from typing import List, Union
import urllib.request

from pyrogram import Client, filters
from pyrogram.types import Message, InputMediaPhoto, InputMediaVideo, InputMediaAnimation, InputMediaDocument
from pixivpy3 import AppPixivAPI


api = AppPixivAPI()
api.login(environ.get('PIXIV_LOGIN'), environ.get('PIXIV_PASSWORD'))
url_pattern = re.compile(r'pixiv.net\/..\/artworks\/\d+')
download_path = environ.get('DOWNLOAD_PATH') or '/tmp'

opener = urllib.request.build_opener()
opener.addheaders = [('referer', 'https://www.pixiv.net/')]
urllib.request.install_opener(opener)


@Client.on_message(filters.command('pixiv', list('!.')) & filters.regex(url_pattern) & (filters.me | filters.channel))
def on_pixiv(client: Client, message: Message):
    if message.chat.type == 'channel':
        if not client.get_chat_member(message.chat.id, 'me').can_post_messages:
            return
    m = url_pattern.search(message.text.markdown or message.caption.markdown)
    caption = m.string[m.end():]
    m = re.search(r'\d+', m.string[m.start():m.end()])
    artwork_id = int(m.string[m.start():m.end()])
    illust = api.illust_detail(artwork_id)
    message.delete()
    if illust['illust']['meta_pages']:
        urls: List[str] = [meta_page['image_urls']['original'] for meta_page in illust['illust']['meta_pages']]
        filenames: List[str] = [url.split('/')[-1] for url in urls]
        media: List[Union[InputMediaPhoto, InputMediaVideo, InputMediaAnimation, InputMediaDocument]] = []
        for url in urls:
            file_path = path.join(download_path, filenames[urls.index(url)])
            urllib.request.urlretrieve(url, file_path)
            if 'file' in message.text:
                if len(media) == 0:
                    media.append(InputMediaDocument(file_path, caption=caption))
                else:
                    media.append(InputMediaDocument(file_path))
            else:
                if filenames[urls.index(url)][-3:] in ('png', 'jpg', 'jpeg'):
                    if len(media) == 0:
                        media.append(InputMediaPhoto(file_path, caption=caption))
                    else:
                        media.append(InputMediaPhoto(file_path))
                elif filenames[urls.index(url)][-3:] == 'gif':
                    if len(media) == 0:
                        media.append(InputMediaAnimation(file_path, caption=caption))
                    else:
                        media.append(InputMediaAnimation(file_path))
                elif filenames[urls.index(url)][-3:] == 'mp4':
                    if len(media) == 0:
                        media.append(InputMediaVideo(file_path, caption=caption))
                    else:
                        media.append(InputMediaVideo(file_path))
                else:
                    if len(media) == 0:
                        media.append(InputMediaDocument(file_path, caption=caption))
                    else:
                        media.append(InputMediaDocument(file_path))
        client.send_media_group(message.chat.id, media)
        try:
            [remove(path.join(download_path, filename)) for filename in filenames]
        except OSError as e:
            print(e)
    elif illust['illust']['meta_single_page']:
        url = illust['illust']['meta_single_page']['original_image_url']
        filename = url.split('/')[-1]
        urllib.request.urlretrieve(url, path.join(download_path, filename))
        if 'file' in message.text:
            client.send_document(message.chat.id, path.join(download_path, filename), caption=caption)
        else:
            if filename[-3:] in ('png', 'jpg', 'jpeg'):
                client.send_photo(message.chat.id, path.join(download_path, filename), caption=caption)
            elif filename[-3:] == 'gif':
                client.send_animation(message.chat.id, path.join(download_path, filename), caption=caption)
            elif filename[-3:] == 'mp4':
                client.send_video(message.chat.id, path.join(download_path, filename), caption=caption)
            else:
                client.send_document(message.chat.id, path.join(download_path, filename), caption=caption)
        try:
            remove(path.join(download_path, filename))
        except OSError as e:
            print(e)
