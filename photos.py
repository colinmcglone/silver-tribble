import shutil

from flask import Flask, render_template
from os import listdir, remove, makedirs
from os.path import isfile, join, isdir, basename, dirname, exists, getmtime
from PIL import Image, ExifTags, ImageFile, ImageOps
from raven.contrib.flask import Sentry

app = Flask(__name__)
sentry = Sentry(app, dsn='https://605561e8608b41d88f625e54cb098f41:bbef88ee71834543815dbd4abcd2ffd8@sentry.io/1277428')

ImageFile.LOAD_TRUNCATED_IMAGES = True

def get_albums():
	media = './static/media/'
	albums = [join(media, a) for a in listdir(media) if isdir(join(media, a))]
	albums.sort(key=lambda x: getmtime(x), reverse=True)
	albums = [{'album_title': x[15:], 'album_directory': x} for x in albums]

	for album in albums:
		album['photos'] = [x for x in listdir(album['album_directory']) if x[-3:].upper() == ("JPG" or "JPEG") ]

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

#	shutil.rmtree('./static/media/Bon_Echo/thumbs')

	for album in albums:
		if exists(album['album_directory'] + '/thumbs/'):
			shutil.rmtree(album['album_directory'] + '/thumbs/')
		if not exists(album['album_directory'] + '/thumbs/'):
			makedirs(album['album_directory'] + '/thumbs/')
		for photo in album['photos']:
			thumbname = "%s_thumbnail" % (photo[:-4])
			thumblocation = album['album_directory'] + '/thumbs/' + thumbname
			if not exists(thumblocation + '.jpeg'):
				img = Image.open(album['album_directory'] + '/' + photo)
				try:
					img.load()
				except Exception as e:
					return render_template('update.html', body = repr(e))
				try:
					line = 1
					for orientation in ExifTags.TAGS.keys():
						if ExifTags.TAGS[orientation]=='Orientation':
							break
					try:
						exif=dict(img._getexif().items())
						if exif[orientation] == 3:
							img=img.rotate(180, expand=True)
						elif exif[orientation] == 6:
							img=img.rotate(270, expand=True)
						elif exif[orientation] == 8:
							img=img.rotate(90, expand=True)
					except:
						pass

					thumb = ImageOps.fit(img, (1000, 1000), Image.ANTIALIAS, centering = (0.5, 0.5))
					thumb.save(thumblocation + '-large.jpeg', 'jpeg', quality=95)

					thumb = ImageOps.fit(img, (500, 599), Image.ANTIALIAS, centering = (0.5, 0.5))
					thumb.save(thumblocation + '.jpeg', 'jpeg', quality=95)

				except Exception as e:
					return render_template('update.html', body = repr(e) + thumblocation + str(line))

	return render_template('update.html', body = "success")
