import m3u8
import requestes


#get m3u8 url
url = 'https://manifest.prod.boltdns.net/manifest/v1/hls/v4/aes128/5182475815001/9999009e-ad06-4103-a764-5078314fbf2f/10s/master.m3u8?fastly_token=NWViN2RiYTFfMzIwYWEyNGU3YmZjMDg3ZDU5N2U2YWI3M2ZlZmM1YWRmNzUxNjFiNDVmODM5MWYyMzZiOTY5YTUwNGJhNzRlOQ%3D%3D'

r = requests.get(url)

m3u8_master = m3u8.loads(r.text)

playlist_url = m3u8_master.data['playlists'][0]['uri']
print(playlist_url) #master playlist

r = requests.get(playlist_url)

playlist = m3u8.loads(r.text)
#print(playlist.segments)

for key in playlist.keys:
    if key:
       key_url = key.uri
       key_methond = key.method
       key_iv = key.iv


print(playlist.data['segments'][0]['uri'])


r = requests.get(playlist.data['segments'][2]['uri'])


# with open('v1.ts', 'wb') as f:
#     for segment in playlist.data['segments']:
#         url = segment['uri']
#         r = requests.get(url)
#         f.write(r.content)
