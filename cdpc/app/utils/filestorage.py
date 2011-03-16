# -*- coding: utf-8; Mode: Python -*-
#
# Copyright (C) 2010  Rogerio Hilbert Lima <rogerhi@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, Image
from cdpc.config import UPLOAD_PATH_AVATAR_PESSOA, UPLOAD_PATH_AVATAR_PROJETO, \
                        UPLOAD_PATH_DOCS

IMAGE_SIZE = (256, 256)

MTYPE = {'pessoa': UPLOAD_PATH_AVATAR_PESSOA,
         'projeto': UPLOAD_PATH_AVATAR_PROJETO}

def save_image(stream, name, mtype):
    image = Image.open(stream)
    image.thumbnail(IMAGE_SIZE)
    path = os.path.join(MTYPE[mtype], '%s.jpg' % name)
    image.save(path)
    
def save_file(fieldstorage, name):
    path = os.path.join(UPLOAD_PATH_DOCS, str(name))
    if not os.path.isdir(path):
        os.makedirs(path)
    path = os.path.join(path, fieldstorage.filename)
    fieldstorage.save(path)
