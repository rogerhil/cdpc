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

from urllib import urlopen
from simplejson import dumps, loads
from flask import Module, request

VALORES_UF = (
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO',
)

CONSULTA_CEP = 'http://viavirtual.com.br/webservicecep.php?cep=%s'
CONSULTA_GEO = 'http://ws.geonames.org/postalCodeLookupJSON?postalcode=%s&country=BR'

module = Module(__name__)

@module.route("consulta_cep/")
def consulta_cep():
    """Usa um serviço na internet para baixar informações como rua,
    bairro, cidade e uf a partir do cep.

    Retorna um Json com as informações obtidas.
    """
    page = urlopen(CONSULTA_CEP % request.args.get('cep'))
    content = page.read().decode('iso-8859-1')
    rua, bairro, cidade, _, ufraw = content.split('||', 4)
    return dumps({
            'rua': rua, 'bairro': bairro, 'cidade': cidade,
            'uf': ufraw.replace('|', '')})

@module.route("consulta_geo/")
def consulta_geo():
    """Usa um serviço na internet para baixar latitude e longitude
    a partir do cep.

    Retorna um Json com a latitude e a longitude obtidas.
    """
    page = urlopen(CONSULTA_GEO % request.args.get('cep')[:5])
    content = loads(page.read())
    pcs = content['postalcodes'];
    if pcs:
        return dumps({
                'lat': content['postalcodes'][0]['lat'],
                'lng': content['postalcodes'][0]['lng']})
    return dumps({'lat':'', 'lng':''})
