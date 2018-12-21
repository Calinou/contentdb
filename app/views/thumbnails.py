# Content DB
# Copyright (C) 2018  rubenwardy
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from flask import *
from app import app

import os
from PIL import Image

ALLOWED_RESOLUTIONS=[(100,67), (200,133), (350,233)]

def mkdir(path):
	if not os.path.isdir(path):
		os.mkdir(path)

mkdir("app/public/thumbnails/")

def resize_and_crop(img_path, modified_path, size):
	img = Image.open(img_path)

	# Get current and desired ratio for the images
	img_ratio = img.size[0] / float(img.size[1])
	ratio = size[0] / float(size[1])

	# Is more portrait than target, scale and crop
	if ratio > img_ratio:
		img = img.resize((int(size[0]), int(size[0] * img.size[1] / img.size[0])),
				Image.BICUBIC)
		box = (0, (img.size[1] - size[1]) / 2, img.size[0], (img.size[1] + size[1]) / 2)
		img = img.crop(box)

	# Is more landscape than target, scale and crop
	elif ratio < img_ratio:
		img = img.resize((int(size[1] * img.size[0] / img.size[1]), int(size[1])),
				Image.BICUBIC)
		box = ((img.size[0] - size[0]) / 2, 0, (img.size[0] + size[0]) / 2, img.size[1])
		img = img.crop(box)

	# Is exactly the same ratio as target
	else:
		img = img.resize(size, Image.BICUBIC)

	img.save(modified_path)


@app.route("/thumbnails/<int:level>/<img>")
def make_thumbnail(img, level):
	if level > len(ALLOWED_RESOLUTIONS) or level <= 0:
		abort(403)

	w, h = ALLOWED_RESOLUTIONS[level - 1]

	mkdir("app/public/thumbnails/{:d}/".format(level))

	cache_filepath  = "public/thumbnails/{:d}/{}".format(level, img)
	source_filepath = "public/uploads/" + img

	resize_and_crop("app/" + source_filepath, "app/" + cache_filepath, (w, h))
	return send_file(cache_filepath)
