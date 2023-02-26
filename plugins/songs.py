import os
from funcs.download import Descargar
from pyrogram import Client as Medusa, filters
from pyrogram.types import Message
from pyrogram.errors.exceptions import MessageNotModified
from youtubesearchpython import VideosSearch


text = (
    '__Saya tidak bisa menebak lagu yang ada di pikiran Anda.'
    ' Jadi harap untuk menentukan nama lagu.__'
    '\n\nPerintah: ```/song <nama lagu>```'
)

descargar = Descargar('downloads/')

@Medusa.on_message(
    filters.command(['song'],prefixes=['/', '!'])
    & (filters.group | filters.private)
    & ~ filters.edited)
async def song_dl(_, msg: Message):

    if len(msg.command) == 1:
        return await msg.reply(text=text, parse_mode='md')

    r_text = await msg.reply('Processing...')
    url = msg.text.split(None, 1)[1]
    url = extract_the_url(url=url)
    
    if url == 0:return await r_text.edit('Saya tidak dapat menemukan lagu itu. Coba dengan kata kunci lain...')

    await r_text.edit('Downloading...')

    ytinfo = descargar.get_song(url)

    if ytinfo == 0:
        await r_text.edit(f'Sesuatu yang salah\n\n☕️Ambil Kopi dan datang lagi... :(')
        return

    try:
        await r_text.edit_text('Mengunggah...')
    except MessageNotModified:
        pass

    await msg.reply_audio(
            audio=f'downloads/{ytinfo.title.replace("/","|")}-{ytinfo.video_id}.mp3', 
            thumb='src/rexaplaylist.png',
            duration=int(ytinfo.length),
            performer=str(ytinfo.author),
            title=f'{str(ytinfo.title)}',
            caption=f"<a href='{url}'>__{ytinfo.title}__</a>\n\n__Downloaded by @xamusicdownloaderbot__"
        )

    await r_text.delete()
    os.remove(f'downloads/{ytinfo.title.replace("/","|")}-{ytinfo.video_id}.mp3')



def extract_the_url(url: str):
    '''Extracting the youtube URL'''

    v = VideosSearch(url, limit=1)
    v_result = v.result()

    if not v_result['result']:
        return 0
    url = v_result['result'][0]['link']
    return url
