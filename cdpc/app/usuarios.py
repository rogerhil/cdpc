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
from urllib import urlopen
from simplejson import dumps
from flask import Module, request, render_template

VALORES_UF = (
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO',
)

CONSULTA_CEP = 'http://viavirtual.com.br/webservicecep.php?cep=%s'

module = Module(__name__)

@module.route("novo/")
def novo():
    """Renderiza o formulário de cadastro de usuários
    """
    return render_template(
        'usuarios/novo.html',
        vals_uf=VALORES_UF)

@module.route("consulta_cep/")
def consulta_cep():
    """Usa um serviço na internet para baixar informações como rua,
    bairro, cidade e uf a partir do cep.

    Retorna um Json com as informações obtidas.
    """
    page = urlopen(CONSULTA_CEP % request.args.get('cep'))
    content = page.read()
    rua, bairro, cidade, _, ufraw = content.split('||', 4)
    return dumps({
            'rua': rua, 'bairro': bairro, 'cidade': cidade,
            'uf': ufraw.replace('|', '')})