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

"""Integra todos os modulos flask declarados noutros lugares.

Esses `outros' modulos são registrados numa aplicação flask. Essa nova
aplicação pode ser usada pelo executável `cdpc', que chama o método
`.run()' da aplicação ou pelo mod_wsgi no apache.
"""

import os
from string import printable
from random import choice
from flask import Flask, send_from_directory
from jinja2 import FileSystemLoader
from .config import STATIC_DIR, TEMPLATE_DIR
from .app.index import is_logged_in
from .app.usuarios import module as usuarios
from .app.projetos import module as projetos
from .app.cadastro import module as cadastro
from .app.index import module as index

class WebApp(Flask):
    """Flask extention to retrieve static files from a configurable
    place
    """

    def __init__(self, import_name, static_path=None, media_path=None):
        self.media_path = media_path
        super(WebApp, self).__init__(import_name, static_path)

    @property
    def has_static_folder(self):
        """This is `True` if self.media_path var exists or if the
        package bound object's container has a folder named
        ``'static'``.
        """
        return os.path.isdir(self.media_path) or \
            os.path.isdir(os.path.join(self.root_path, 'static'))

    def send_static_file(self, filename):
        """Function used internally to send static files from the static
        folder to the browser.

        This method is overriden to be able to customize the
        filesystem path exposed.
        """
        path = os.path.join(self.root_path, 'static')
        if self.media_path:
            path = os.path.abspath(self.media_path)
        return send_from_directory(path, filename)

def create_app():
    """Constroi a aplicação flask e registra outros modulos nela.
    """
    app = WebApp(__name__, media_path=STATIC_DIR)
    app.jinja_env.loader = FileSystemLoader(TEMPLATE_DIR)
    app.register_module(index, url_prefix="/")
    app.register_module(usuarios, url_prefix="/usuarios/")
    app.register_module(projetos, url_prefix="/projetos/")
    app.register_module(cadastro, url_prefix="/cadastro/")

    app.jinja_env.globals['is_logged_in'] = is_logged_in
    app.secret_key = ''.join(choice(printable) for x in range(50))
    return app
