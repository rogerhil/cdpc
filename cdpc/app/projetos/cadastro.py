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

from urllib import urlopen
from simplejson import dumps, loads
from flask import Module, request
from formencode import foreach
from ..common.cadastro import *

TIPO = format(
    [u'Ponto',
     u'Pontão',
     u'Iniciativa Premiada'])

TIPO_CONVENIO = format(
    [u'Internacional',
     u'Federal',
     u'Estadual',
     u'Municipal'])

ACAO_CULTURA_VIVA = format(
                    [u'Agente Cultura Viva',
                     u'Cultura Digital',
                     u'Cultura e Saúde',
                     u'Economia Viva',
                     u'Escola Viva',
                     u'Grios',
                     u'Interações Estéticas',
                     u'Mídias Livres',
                     u'Pontinho de Cultura',
                     u'Pontos de memória',
                     u'Redes Indígenas',
                     u'Tuxaua'])

PARCERIAS = format(
    [u'Biblioteca',
     u'Empresa',
     u'Equipamento de Saúde',
     u'Escola',
     u'Igreja',
     u'ONG',
     u'Poder público',
     u'Pontos de Memória',
     u'Redes Indígenas',
     u'Sistemas S (Sesc, Senai, etc)',
     u'Tuxaua',
     u'Outros'])

LOCAL_PROJ = format(
    [u'Sede',
     u'Itinerante',
     u'Outros locais'])

PQ_SEM_TEL = format(
    [u'Opção',
     u'Não há fornecimento de serviços na região',
     u'Falta de recursos',
     u'Outros'])

PQ_SEM_INTERNET = PQ_SEM_TEL

TIPO_INTERNET = format(
    [u'Discada',
     u'3G',
     u'ADSL/Cabo (Banda Larga)',
     u'Rádio',
     u'Gesac',
     u'Internet Pública'])

ATIVIDADE = format(
    [u'Cultura Popular',
     u'Direitos Humanos',
     u'Economia Solidária',
     u'Educação',
     u'Esportes e Lazer',
     u'Etnia',
     u'Gênero',
     u'Habitação',
     u'Meio ambiente',
     u'Memória',
     u'Patrimônio Histórico Imaterial',
     u'Patrimônio Histórico Material',
     u'Pesquisa e Extensão',
     u'Povos e comunidades tradicionais',
     u'Recreação',
     u'Religião',
     u'Saúde',
     u'Sexualidade',
     u'Tecnologia',
     u'Trabalho'])

PUBLICO_ALVO = format(
    [u'Crianças',
     u'Adolescentes',
     u'Adultos',
     u'Jovens'])
                
CULTURAS_TRADICIONAIS = format(
    [u'Quilombola',
     u'Pomerano',
     u'Caiçara',
     u'Indígena',
     u'Cigana',
     u'Ribeirinhos',
     u'Povos da Floresta'])


OCUPACAO_DO_MEIO = format(
    [u'Rural',
     u'Urbano'])

GENERO = format(
    [u'Mulheres',
     u'Homens',
     u'LGBT'])

MANIFESTACOES_LINGUAGENS = format(
    [u'Artes digitais',
     u'Artes plásticas',
     u'Audiovisual',
     u'Circo',
     u'Culinária',
     u'Dança',
     u'Fotografia',
     u'Grafite',
     u'Internet',
     u'Jornalismo',
     u'Literatura',
     u'Música',
     u'Rádio',
     u'Teatro',
     u'Tecnologias digitais',
     u'Tradição oral',
     u'TV',
     u'Outras'])

