# pyrogram_plugins
Just my pyrogram plugins

## Plugins description
 - mention_admins.py. Something like /report in bots. It'll delete your message, that starts with `@admin` or `@admins` and send new same messages with ivisible admin mentions
 - message_json.py. Comamnds `json`,  `src` and `message` with `.` or `!` prefix (e.g. `!json`), that'll upload replied messsage JSON object to geany and paste link
 - pixiv.py. Helps you send images from pixiv. Format `!pixiv ARGUMENTS ARTWORK_LINK CAPTION` (or `.pixiv`). Arguments are:
  - file/files. if `file` in message text, that will send pictures as documents
  - EACH if `EACH` in message text, that'll add caption to each media/document
  - List of indexes for sending (starts at 0) e.g. if you pass [0, 1, 3] it'll send only 1st, 2nd and 4th pictures from post
  - You can use `$TITLE` in caption, it will be replaced with post title
  - You should pass your pixiv login and password as `PIXIV_LOGIN` and `PIXIV_PASSWORD` environment variables to make it works.
 - purge.py. On `!purge` or `.purge.` will delete all messages from replied to the latest in the chat.
 - read_only.py. Helps you mute other people in chat. Usage: `ro term` or `mute term` to mute person, whose message you replied. Term format must be like `1w7d24h60m` where `w` is weeks, `d` is days, `h` is hours, `m` is minutes. Not all letters are required (e.g. `mute 1d12h` will mute person for 1 day and 12 hours. Also you can do it with terms `1.5d` and `36h`)
 - source.py. Just send this repo on '!source' or `.source`
 - translate.py. Translate messages into other language. Commands: `trans`, `transl`, `translate` with `.` or `!` prefixes. Usage:
  - `!translate TEXT` will translate `TRANSLATE` into default language (you can set it via `LANGUAGE` environment variable).
  - `!translate LANG TEXT` will translate into `LANG`. E.g. `!translate English hello world`, `!translate en hello world`
  - `!translate SOURCE:DEST TEXT` will translate `TEXT` from `SOURCE` language into `DEST` language. Example: `!translate Ukrainian:en Я з'їм все твоє сало`
  - If you replied other message, it'll translate text from replied message, not from your.
  
## Installation
[Pyrogram docs](https://docs.pyrogram.org/topics/smart-plugins) or [with docker](https://t.me/pyrogramchat/263809)
