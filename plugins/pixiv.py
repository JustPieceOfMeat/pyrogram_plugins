from os import environ, path, remove
import re
from typing import List, Dict, Union
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


@Client.on_message(
    filters.command('pixiv', list('!.')) &
    filters.regex(url_pattern) &
    (filters.me | filters.channel) &
    ~filters.scheduled
)
def on_pixiv(client: Client, message: Message):
    if message.chat.type == 'channel':
        if not client.get_chat_member(message.chat.id, 'me').can_post_messages:
            return

    m = url_pattern.search(message.text.html or message.caption.html)   # URL
    caption = m.string[m.end():]    # Caption
    m = re.search(r'\d+', m.string[m.start():m.end()])  # Artwork ID from URL
    artwork_id = int(m.string[m.start():m.end()])
    m = re.search(r'\[((\d+,)+ )?\d+]', caption)    # Indexes
    indexes: Union[List[int], None] = None
    if m is not None:
        indexes = eval(m.string[m.start():m.end()])
        caption = m.string[:m.start()] + m.string[m.end():]

    illust = api.illust_detail(artwork_id)
    caption = caption.replace('$TITLE', illust['illust']['title'])
    message.delete()
    if illust['illust']['meta_pages']:
        urls: List[str] = [meta_page['image_urls']['original'] for meta_page in illust['illust']['meta_pages']]
        filenames: List[str] = [url.split('/')[-1] for url in urls]
        media: Dict[str, List[Union[InputMediaPhoto, InputMediaVideo, InputMediaAnimation, InputMediaDocument]]] = {}
        for url in urls:
            if indexes is not None and urls.index(url) not in indexes:
                continue
            file_path = path.join(download_path, filenames[urls.index(url)])
            urllib.request.urlretrieve(url, file_path)
            if 'file' in message.text:
                if 'documents' not in media:
                    media['documents'] = []
                if len(media['documents']) == 0 or 'EACH' in str(message.text) + str(message.caption):
                    media['documents'].append(InputMediaDocument(file_path, caption=caption))
                else:
                    media['documents'].append(InputMediaDocument(file_path))
            else:
                if filenames[urls.index(url)][-3:] in ('png', 'jpg', 'jpeg'):
                    if 'photos' not in media:
                        media['photos'] = []
                    if len(media['photos']) == 0 or 'EACH' in str(message.text) + str(message.caption):
                        media['photos'].append(InputMediaPhoto(file_path, caption=caption))
                    else:
                        media['photos'].append(InputMediaPhoto(file_path))
                elif filenames[urls.index(url)][-3:] == 'gif':
                    if 'animations' not in media:
                        media['animations'] = []
                    if len(media['animations']) == 0 or 'EACH' in str(message.text) + str(message.caption):
                        media['animations'].append(InputMediaAnimation(file_path, caption=caption))
                    else:
                        media['animations'].append(InputMediaAnimation(file_path))
                elif filenames[urls.index(url)][-3:] == 'mp4':
                    if 'videos' not in media:
                        media['videos'] = []
                    if len(media['videos']) == 0 or 'EACH' in str(message.text) + str(message.caption):
                        media['videos'].append(InputMediaVideo(file_path, caption=caption))
                    else:
                        media['videos'].append(InputMediaVideo(file_path))
                else:
                    if 'documents' not in media:
                        media['documents'] = []
                    if len(media['documents']) == 0 or 'EACH' in str(message.text) + str(message.caption):
                        media['documents'].append(InputMediaDocument(file_path, caption=caption))
                    else:
                        media['documents'].append(InputMediaDocument(file_path))
        for media_type in media:
            for i in range(len(media[media_type]) // 10):
                client.send_media_group(message.chat.id, media[media_type][i*10:(i+1)*10])
            if len(media[media_type]) % 10 > 0:
                client.send_media_group(message.chat.id, media[media_type][-(len(media[media_type]) % 10):])
        for filename in filenames:
            try:
                remove(path.join(download_path, filename))
            except OSError:
                continue
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
