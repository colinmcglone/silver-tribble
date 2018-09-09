from flask import Flask, render_template
from os import listdir, remove, makedirs
from os.path import isfile, join, isdir, basename, dirname, exists, getmtime
from PIL import Image

app = Flask(__name__)

def get_albums():
	media = './static/media/'
	albums = [join(media, a) for a in listdir(media) if isdir(join(media, a))]
	albums.sort(key=lambda x: getmtime(x), reverse=True)
	albums = [{'album_title': x[15:], 'album_directory': x} for x in albums]

	for album in albums:
		album['photos'] = [x for x in listdir(album['album_directory']) if x[-3:].upper() == "JPG" ]

	return albums

@app.route("/")
def hello():
	albums = get_albums()
    return render_template('gallery.html', body = albums)

@app.route("/update")
def update_photos():
	albums = get_albums()
	for album in albums:
		if not exists(album['album_directory'] + '/thumbs/'):
			makedirs(album['album_directory'] + '/thumbs/')
		for photo in album['photos']:
			thumbname = "%s_thumbnail" % (photo[:-4])
			thumblocation = album['album_directory'] + '/thumbs/' + thumbname
			if not exists(thumblocation + '.jpeg'):
				img = Image.open(photo)
				try:
					img.load()
				except:
					break
				img.thumbnail([500, 500])
				img.save(thumblocation + '.jpeg', 'jpeg')
				img = Image.open(pic)
				img.load()
				img.thumbnail([1000, 1000])
				img.save(thumblocation + '-large.jpeg', 'jpeg')
				
	return render_template('album.html', body = albums)
