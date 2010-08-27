# -*- coding: utf-8; Mode: Python -*-
#
# Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
# Copyright (C) 2010  Marco Túlio Gontijo e Silva <marcot@marcot.eti.br>
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

from flask import Module, render_template

from . import validators
from . import models
from cadastrado import VALORES_UF

module = Module(__name__)

@module.route("novo/")
def novo():
    """
    """
    if request.method == 'POST':
        # instanciando o validador
        validator = validators.Projeto()
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
            projeto = models.Projeto()
            projeto.voce_eh = validado['voce_eh']
            projeto.tipo_convenio = validado['tipo_convenio']
            projeto.numero_convenio = validado['numero_convenio']
            projeto.nome_proj = validado['nome_proj']
            projeto.email = validado['email']
            projeto.nome_ent = validado['nome_ent']

            session.commit()

            # FIXME: Avisar ao usuário que tudo deu certo.

    return render_template(
        'projetos/novo.html',
        vals_uf=VALORES_UF)
