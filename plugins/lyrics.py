import os
from config import GENIUS_API
from pyrogram import Client as Medusa,filters
from pyrogram.types import Message
from lyricsgenius import genius
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong


api = genius.Genius(GENIUS_API,verbose=False)


@Medusa.on_message(filters.command(['lyrics','lyric'],prefixes=['/','!']) 
    & (filters.group | filters.private) 
    & ~ filters.edited)
async def lyrics(medusa:Medusa,msg: Message):

    if len(msg.command) == 1:
        return await msg.reply(
            text='__Harap tentukan kueri...__', 
        )

    r_text = await msg.reply('__Mencari...__')
    song_name = msg.text.split(None, 1)[1]

    lyric = api.search_song(song_name)

    if lyric is None:return await r_text.edit('__Tidak ada lirik yang ditemukan untuk kueri Anda...__')

    lyric_title = lyric.title
    lyric_artist = lyric.artist
    lyrics_text = lyric.lyrics

    try:
        await r_text.edit_text(f'__--**{lyric_title}**--__\n__{lyric_artist}\n__\n\n__{lyrics_text}__\n__Diekstraksi oleh @xamusicdownloaderbot')

    except MessageTooLong:
        with open(f'downloads/{lyric_title}.txt','w') as f:
            f.write(f'{lyric_title}\n{lyric_artist}\n\n\n{lyrics_text}')

        await r_text.edit_text('__Lirik terlalu panjang. Mengirim sebagai file teks...__')
        await msg.reply_chat_action(
            action='upload_document'
        )
        await msg.reply_document(
            document=f'downloads/{lyric_title}.txt',
            thumb='src/Medusa320px.png',
            caption=f'\n__--{lyric_title}--__\n__{lyric_artist}__\n\n__Diekstraksi oleh @xamusicdownloaderbot__'
        )

        await r_text.delete()
        
        
        os.remove(f'downloads/{lyric_title}.txt')
