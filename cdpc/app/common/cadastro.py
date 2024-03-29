# -*- coding: utf-8; Mode: Python -*-
#
# Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
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

from simplejson import dumps, loads
from formencode import foreach

PREFIX = 'OPCAO_SISTEMA'
#item_format = lambda x: ("%s: %s" % (PREFIX, x))
item_format = lambda x: x
format = lambda items: [(item_format(i), i) for i in items]

EMPTY_HACK = '____________________'

VALORES_UF = (
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO',
)

VALORES_UF = [(u'AC', u'Acre'),
              (u'AL', u'Alagoas'),
              (u'AP', u'Amapá'),
              (u'AM', u'Amazonas'),
              (u'BA', u'Bahia'),
              (u'CE', u'Ceará'),
              (u'DF', u'Distrito Federal'),
              (u'ES', u'Espírito Santo'),
              (u'GO', u'Goiás'),
              (u'MA', u'Maranhão'),
              (u'MT', u'Mato Grosso'),
              (u'MS', u'Mato Grosso do Sul'),
              (u'MG', u'Minas Gerais'),
              (u'PB', u'Paraiba'),
              (u'PR', u'Paraná'),
              (u'PA', u'Pará'),
              (u'PE', u'Pernambuco'),
              (u'PI', u'Piauí'),
              (u'RN', u'Rio Grande do Norte'),
              (u'RS', u'Rio Grande do Sul'),
              (u'RJ', u'Rio de Janeiro'),
              (u'RO', u'Rondônia'),
              (u'RR', u'Roraima'),
              (u'SC', u'Santa Catarina'),
              (u'SE', u'Sergipe'),
              (u'SP', u'São Paulo'),
              (u'TO', u'Tocantins')]

TIPO_TEL_SEDE = format(
    [u'Fixo',
     u'Celular',
     u'Rádio',
     u'Rural',
     u'Público'])
        
def prepare_data(lists, fields):
    data = {}
    for key, valid in fields.items():
        value = lists.get(key)
        if value != None and len(value) > 1:
            value = [i for i in value if i]
            data[key] = value
        else:
            if isinstance(valid, foreach.ForEach):
                if value == None:
                    value = []
                value = [i for i in value if i]
                data[key] = value
                continue
            sch = getattr(valid, 'schema', None)
            for i in xrange(5):
                if sch == None:
                    if value == None:
                        continue
                    data[key] = value[0]
                    continue
                if isinstance(sch, foreach.ForEach):
                    if value == None:
                        value = []
                    value = [i for i in value if i]                    
                    data[key] = value 
                    continue
                sch = getattr(sch, 'schema', None)
    return data

