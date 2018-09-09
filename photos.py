from flask import Flask, render_template
from os import listdir, remove, makedirs
from os.path import isfile, join, isdir, basename, dirname, exists, getmtime
from PIL import Image

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('gallery.html', body = 'Hello World.')

@app.route("/update")
def update_photos():
	media = './static/media/'
	albums = [join(media, a) for a in listdir(media) if isdir(join(media, a))]
	albums = [{'album_title': x[8:], 'album_directory': x} for x in albums]

	return render_template('album.html', body = albums)
