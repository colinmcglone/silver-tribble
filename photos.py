from flask import Flask, render_template
from os import listdir, remove, makedirs
from os.path import isfile, join, isdir, basename, dirname, exists, getmtime
from PIL import Image, ExifTags
from raven.contrib.flask import Sentry

app = Flask(__name__)
sentry = Sentry(app, dsn='https://605561e8608b41d88f625e54cb098f41:bbef88ee71834543815dbd4abcd2ffd8@sentry.io/1277428')

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
	return render_template('gallery.html', albums = albums)

@app.route("/<album>/")
def album_view(album):
	albums = get_albums()
	album = next((item for item in albums if item['album_title'] == album), None)

	return render_template('album.html', album = album)

@app.route("/update")
def update_photos():
	albums = get_albums()
	if not albums:
		return render_template('update.html', body = 'No Albums')

	for album in albums:
		if not exists(album['album_directory'] + '/thumbs/'):
			makedirs(album['album_directory'] + '/thumbs/')
		for photo in album['photos']:
			thumbname = "%s_thumbnail" % (photo[:-4])
			thumblocation = album['album_directory'] + '/thumbs/' + thumbname
#			if not exists(thumblocation + '.jpeg'):
#				img = Image.open(album['album_directory'] + '/' + photo)
#				try:
#					img.load()
#				except Exception as e:
#					return render_template('update.html', body = repr(e))
#				try:
#					for orientation in ExifTags.TAGS.keys():
#						if ExifTags.TAGS[orientation]=='Orientation':
#							break
#					exif=dict(img._getexif().items())
#
#					if exif[orientation] == 3:
#						img=img.rotate(180, expand=True)
#					elif exif[orientation] == 6:
#						img=img.rotate(270, expand=True)
#					elif exif[orientation] == 8:
#						img=img.rotate(90, expand=True)
#
#					img.thumbnail((1000, 1000), Image.ANTIALIAS)
#					img.save(thumblocation + '-large.jpeg', 'jpeg')
#
#					img.thumbnail((500, 500), Image.ANTIALIAS)
#					img.save(thumblocation + '.jpeg', 'jpeg')
#
#				except Exception as e:
#					return render_template('update.html', body = repr(e))

	return render_template('update.html', body = "success")
