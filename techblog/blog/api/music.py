# coding:utf-8
import ncmbot


def readFile(fn, buf_size=262144):
    f = open(fn, "rb")
    while True:
        c = f.read(buf_size)
        if c:
            yield c
        else:
            break
    f.close()


def searchMusic(s=u'热门英文歌'):
	response = ncmbot.search(keyword=s, limit=50)
	if response.status_code != 200:
		yield False

	result = response.json()['result']
	songCount = result['songCount']
	songs = result['songs']
	for song in songs:
		id = song['id']
		name = song['name']
		# size = ncmbot.music_url(ids=[id]).json()['data'][0]['size']

		singers = ' '.join(singer['name'] for singer in song['artists']) # singer
		if len(singers) > 30 and ' ' in singers:
			singers = u'群星'

		album = song['album']['name']

		duration = song['duration']
		m, s = divmod(round(int(duration)/1000.0), 60)
		duration = "%02d:%02d" % (m, s)

		download_name = singers + ' - ' + name + '.mp3'
		yield {'id': id, 'name': name, 'singers': singers, 'album': album, 'duration': duration,
			   'download_name': download_name}


if __name__ == '__main__':
	# for i in searchMusic():
	# 	print i
	# 	print '-'*100
	print ncmbot.song_detail([186016]).json()['songs'][0]['m']['size']


	
