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
from cdpc.config import UPLOAD_PATH_AVATAR_PESSOA, UPLOAD_PATH_AVATAR_PROJETO, \
                        UPLOAD_PATH_DOCS
from ..projetos import cadastro

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
    
def file_list(objs, name):
    res = []
    for obj in objs:
        urlpath = "/static/upload/documentos/%s/%s" % (name, obj.doc)
        fspath = os.path.join(UPLOAD_PATH_DOCS, str(name), obj.doc)
        link = ' - <a href="%s" target="_blank">%s</a>'
        if not os.path.isfile(fspath):
            continue
        res.append(link % (urlpath, obj.doc))
    return "<br />".join(res)


def file_list_for_edit(objs, pid):
    res = []
    for obj in objs:
        urlpath = "/static/upload/documentos/%s/%s" % (pid, obj.doc)
        fspath = os.path.join(UPLOAD_PATH_DOCS, str(pid), obj.doc)
        link = '<div class="file-item"><a href="javascript:;">%s</a></div>' \
               '<a class="remove" onclick="removeDoc(this, %s);">Remover</a>'
        link = '<label>%s</label>' % link
        if not os.path.isfile(fspath):
            continue
        res.append(link % (obj.doc, obj.id))
    res = '<div>%s<div style="clear: both; margin-bottom: 10px;"></div></div>' \
          % "</div><div>".join(res)
    res += '<input type="hidden" name="files_to_remove" id="files_to_remove" />'
    return res

def to_dict(obj):
    return dict(obj)

def to_str(obj):
    return str(obj)

def get_choices(name):
    return dict(getattr(cadastro, name, {}))
    
def get_value(d, value):
    print "#"*100
    print value
    return dict(d).get(value, value)

