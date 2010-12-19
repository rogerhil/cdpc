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
from formencode import foreach

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


CONSULTA_CEP = 'http://viavirtual.com.br/webservicecep.php?cep=%s'
CONSULTA_GEO = 'http://ws.geonames.org/postalCodeLookupJSON?postalcode=%s&country=BR'

TIPO = [(u'ponto', u'Ponto'),
        (u'pontao', u'Pontão'),
        (u'iniciativa_premiada', u'Iniciativa Premiada')]

TIPO_CONVENIO = [(u'internacional', u'Internacional'),
                 (u'federal', u'Federal'),
                 (u'estadual', u'Estadual'),
                 (u'municipal', u'Municipal')]

ACAO_CULTURA_VIVA = [(u'Agente Cultura Viva', u'Agente Cultura Viva'),
                     (u'Cultura Digital', u'Cultura Digital'),
                     (u'Cultura e Saúde', u'Cultura e Saúde'),
                     (u'Economia Viva', u'Economia Viva'),
                     (u'Escola Viva', u'Escola Viva'),
                     (u'Grios', u'Grios'),
                     (u'Interações Estéticas', u'Interações Estéticas'),
                     (u'Mídias Livres', u'Mídias Livres'),
                     (u'Pontinho de Cultura', u'Pontinho de Cultura'),
                     (u'Pontos de memória', u'Pontos de memória'),
                     (u'Redes Indígenas', u'Redes Indígenas'),
                     (u'Tuxaua', u'Tuxaua')]

PARCERIAS = [(u'Biblioteca', u'Biblioteca'),
             (u'Empresa', u'Empresa'),
             (u'Equipamento de Saúde', u'Equipamento de Saúde'),
             (u'Escola', u'Escola'),
             (u'Igreja', u'Igreja'),
             (u'ONG', u'ONG'),
             (u'Poder público', u'Poder público'),
             (u'Pontos de Memória', u'Pontos de Memória'),
             (u'Redes Indígenas', u'Redes Indígenas'),
             (u'Sistemas S', u'Sistemas S (Sesc, Senai, etc)'),
             (u'Tuxaua', u'Tuxaua')]

LOCAL_PROJ = [(u'sede', u'Sede'),
              (u'itinerante', u'Itinerante'),
              (u'outros', u'Outros locais')]

PQ_SEM_TEL = [(u'opcao', u'Opção'),
              (u'fornecimento', u'Não há fornecimento de serviços na região'),
              (u'recursos', u'Falta de recursos'),
              (u'outros', u'Outros')]

PQ_SEM_INTERNET = PQ_SEM_TEL

TIPO_TEL_SEDE = [(u'fixo', u'Fixo'),
                 (u'celular', u'Celular'),
                 (u'radio', u'Rádio'),
                 (u'rural', u'Rural'),
                 (u'publico', u'Público')]

TIPO_INTERNET = [(u'discada', u'Discada'),
                 (u'3g', u'3G'),
                 (u'adsl', u'ADSL/Cabo (Banda Larga)'),
                 (u'radio', u'Rádio'),
                 (u'gesac', u'Gesac'),
                 (u'public', u'Internet Pública')]

ATIVIDADE = [(u'Agente cultura viva', u'Agente Cultura Viva'),
             (u'Cultura digital', u'Cultura Digital'),
             (u'Cultura e saúde', u'Cultura e Saúde'),
             (u'Economia viva', u'Economia Viva'),
             (u'Escola viva', u'Escola Viva'),
             (u'Grios', u'Grios'),
             (u'Interacoes estéticas', u'Interações Estéticas'),
             (u'Mídias livres', u'Mídias Livres'),
             (u'Pontinho de cultura', u'Pontinho de Cultura'),
             (u'Pontos de memoria', u'Pontos de memória'),
             (u'Redes indígenas', u'Redes Indígenas'),
             (u'Tuxaua', u'Tuxaua')]

PUBLICO_ALVO = [(u'Criancas', u'Crianças'),
                (u'Adolescentes', u'Adolescentes'),
                (u'Adultos', u'Adultos'),
                (u'Jovens', u'Jovens')]
                
CULTURAS_TRADICIONAIS = [(u'Quilombola', u'Quilombola'),
                         (u'Pomerano', u'Pomerano'),
                         (u'Caiçara', u'Caiçara'),
                         (u'Indígena', u'Indígena'),
                         (u'Cigana', u'Cigana'),
                         (u'Ribeirinhos', u'Ribeirinhos'),
                         (u'Povos da floresta', u'Povos da Floresta')]


OCUPACAO_DO_MEIO = [(u'Rural', u'Rural'),
                    (u'Urbano', u'Urbano')]

GENERO = [(u'Mulheres', u'Mulheres'),
          (u'Homens', u'Homens'),
          (u'LGBT', u'LGBT')]

MANIFESTACOES_LINGUAGENS = [(u'Artes digitais', u'Artes digitais'),
                            (u'Artes plásticas', u'Artes plásticas'),
                            (u'Audiovisual', u'Audiovisual'),
                            (u'Circo', u'Circo'),
                            (u'Culinária', u'Culinária'),
                            (u'Dança', u'Dança'),
                            (u'Fotografia', u'Fotografia'),
                            (u'Grafite', u'Grafite'),
                            (u'Internet', u'Internet'),
                            (u'Jornalismo', u'Jornalismo'),
                            (u'Literatura', u'Literatura'),
                            (u'Música', u'Música'),
                            (u'Rádio', u'Rádio'),
                            (u'Teatro', u'Teatro'),
                            (u'Tecnologias digitais', u'Tecnologias digitais'),
                            (u'Tradição oral', u'Tradição oral'),
                            (u'TV', u'TV')]

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
