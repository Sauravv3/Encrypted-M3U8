import requests
import m3u8
import subprocess
from Crypto.Cipher import AES



url = 'https://manifest.prod.boltdns.net/manifest/v1/hls/v4/aes128/5182475815001/9999009e-ad06-4103-a764-5078314fbf2f/10s/master.m3u8?fastly_token=NWViYWE3ZjJfMzk1YmJkMWZjOGYxNTJjZWE2ZDZiMzNjMjA4MjcwYTNlMjMxNmY5YTQ2YWU5NzhjNzA0ZmRiYjBhMGMyYjRhYw%3D%3D'

r = requests.get(url)

m3u8_master_playlist = m3u8.loads(r.text)


m3u8_master_playlist_video = m3u8_master_playlist.data['playlists']
m3u8_master_playlist_audio = m3u8_master_playlist.data['media']


#master video playlist formatted output
for video in m3u8_master_playlist_video:
        resolution = video['stream_info']['resolution']
        playlist_url = video['uri']
        print(resolution, playlist_url)
        #print(str("URL-1 ") + "  " +url['uri'])
        #print(str("Resolution: ") + "  " + url['stream_info']['resolution'])
#---------------------------------------------------------------------------------

final_playlist = m3u8_master_playlist_video[3]['uri'] #select video quality
r = requests.get(final_playlist)
playlist = m3u8.loads(r.text)



for key in playlist.keys:
    if key:
        video_key_url = key.uri
        video_iv = key.iv
        vieo_key_method = key.method


#master audio playlist formatted output
for audio in m3u8_master_playlist_audio:
    audio_language = audio['language']
    audio_url = audio['uri']
    print(str('audio language:'),audio_language, audio_url)
#----------------------------------------------------------------------------------

audio_final = m3u8_master_playlist_audio[0]['uri'] #select audio quality

r = requests.get(audio_final)
audio = m3u8.loads(r.text)
print(audio.data)


for key in audio.keys:
    if key:
        audio_key_url = key.uri
        audio_iv = key.iv
        aduio_key_methon = key.method


with open('fvid01.ts', 'wb') as f:
     for segment in playlist.data['segments']:
         url = segment['uri']
         r = requests.get(url)
         iv = video_iv[:AES.block_size]
         get_key = requests.get(video_key_url)
         get_key = get_key.content
         cipher = AES.new(get_key, AES.MODE_CBC, iv)
         decrypt_video = cipher.decrypt(r.content)
         f.write(decrypt_video)


with open('faud01.ts', 'wb') as f:
     for segment in audio.data['segments']:
         url = segment['uri']
         r = requests.get(url)
         iv = audio_iv[:AES.block_size]
         get_key = requests.get(audio_key_url)
         get_key = get_key.content
         cipher = AES.new(get_key, AES.MODE_CBC, iv)
         decrypt_audio = cipher.decrypt(r.content)
         f.write(decrypt_audio)


subprocess.run('ffmpeg', '-i', 'fvid01.ts', '-i', 'faud01.ts' '-c' 'copy', 'final.ts')


print(""""

Audio + Video Download complete...

""")












