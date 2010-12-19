# -*- coding: utf-8; Mode: Python -*-
#
# Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
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

"""Mantém todas as configurações para da aplicação de cadastro de
pontos de cultura.
"""
import os

def get_path(*extrapaths):
    """Retorna o caminho para alguma coisa que esteja "próxima" ao
    arquivo de configuração.
    """
    return os.path.join(os.path.dirname(__file__), '..', *extrapaths)

TEMPLATE_DIR = get_path('data', 'templates')

STATIC_DIR = get_path('data', 'media')

#DATABASE_URI = 'mysql://cdpc:cdpc@localhost/cdpc'
DATABASE_URI = 'mysql://root@localhost/cdpc'
    
UPLOAD_PATH = get_path('data', 'media', 'upload')
UPLOAD_PATH_AVATAR = os.path.join(UPLOAD_PATH, 'avatar/')
UPLOAD_PATH_AVATAR_PESSOA = os.path.join(UPLOAD_PATH_AVATAR, 'pessoa/')
UPLOAD_PATH_AVATAR_PROJETO = os.path.join(UPLOAD_PATH_AVATAR, 'projeto/')

if not os.path.exists(UPLOAD_PATH_AVATAR_PESSOA):
    os.makedirs(UPLOAD_PATH_AVATAR_PESSOA)
if not os.path.exists(UPLOAD_PATH_AVATAR_PROJETO):
    os.makedirs(UPLOAD_PATH_AVATAR_PROJETO)
