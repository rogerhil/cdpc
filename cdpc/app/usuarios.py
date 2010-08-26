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

"""Contém as visualizações para a gestão de usuários
"""
from formencode import Invalid
from urllib import urlopen
from simplejson import dumps, loads
from flask import Module, request, render_template

from . import validators
from . import models
from cadastrado import VALORES_UF

module = Module(__name__)

@module.route("novo/", methods=('GET', 'POST'))
def novo():
    """Renderiza o formulário de cadastro de usuários
    """
    if request.method == 'POST':
        # instanciando o validador
        validator = validators.Usuario()
        validado = {}
        try:
            validado = validator.to_python(request.form)
        except Invalid, e:
            # Dar um feedback pro usuário usando a instância da
            # exceção "e".
            pass
        else:
            # Instanciando o modelo e associando os campos validados e
            # transformados em valores python à instância que será
            # salva no db.
            usuario = models.Usuario()
            usuario.nome = validado['nome']
            usuario.cpf = validado['cpf']
            session.commit()

            # FIXME: Avisar ao usuário que tudo deu certo.

    return render_template(
        'usuarios/novo.html',
        vals_uf=VALORES_UF)
