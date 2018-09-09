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

	pictures = []

	albums.sort(key=lambda x: getmtime(x), reverse=True)

	for album in albums:
		pictures.append([join(album, f) for f in listdir(album) if isfile(join(album, f))])

	for album in pictures:
		if not exists(dirname(album[0]) + '/thumbs/'):
			makedirs(dirname(album[0]) + '/thumbs/')

		album.sort(key=lambda x: basename(x)[4:-4])

		for pic in album:
			print(pic)
			name = basename(pic)[:-4]
			thumbname = "%s_thumbnail" % (basename(pic)[:-4])
			thumblocation = dirname(pic)+'/thumbs/'+thumbname
			if not exists(thumblocation + '.jpeg'):
				img = Image.open(pic)
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


			tag = '<a href="%s" class="js-mediaSwipe" data-rel="%s" style="background-image: %s;"></a>\n' % (pic , dirname(pic), 'url(\'' + thumblocation + '.jpeg' + '\')')
			with open('pictures.html', 'a') as the_file:
				the_file.write(tag)
			with open('%s.html' % (dirname(album[0])[8:]), 'a') as album_file:
				album_file.write(tag)
			if pic == album[-1]:
				with open('pictures.html', 'a') as the_file:
					the_file.write('</div>')
				with open('%s.html' % (dirname(album[0])[8:]), 'a') as album_file:
					album_file.write('</div><script src="mediaswipe.js"></script></body></html>')
