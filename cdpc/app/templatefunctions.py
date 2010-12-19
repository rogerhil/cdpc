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

import os
from cdpc.config import UPLOAD_PATH_AVATAR_PESSOA, UPLOAD_PATH_AVATAR_PROJETO

def avatar_pessoa(obj):
    urlpath = "/static/upload/avatar/pessoa/%s.jpg" % obj.id
    fspath = os.path.join(UPLOAD_PATH_AVATAR_PESSOA, "%s.jpg" % obj.id)
    img = '<img src="%s" width="175" />'
    if os.path.isfile(fspath):
        return img % urlpath
    if obj.sexo == 'masculino':
        return img % '/static/img/bg/blank_user_male_175.gif'
    else:
        return img % '/static/img/bg/blank_user_female_175.gif'

def avatar_projeto(obj):
    urlpath = "/static/upload/avatar/projeto/%s.jpg" % obj.id
    fspath = os.path.join(UPLOAD_PATH_AVATAR_PROJETO, "%s.jpg" % obj.id)
    img = '<img src="%s" width="175" />'
    if os.path.isfile(fspath):
        return img % urlpath
    return img % '/static/img/bg/project_icon.jpg'
