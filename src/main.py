# -*- Coding: utf-8; Mode: Python -*-
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
aplicação pode ser usada pelo executável `cdcp', que chama o método
`.run()' da aplicação ou pelo mod_wsgi no apache.
"""

from flask import Flask

def create_app():
    """Constroi a aplicação flask e registra outros modulos nela.
    """
    app = Flask(__name__)
    return app
