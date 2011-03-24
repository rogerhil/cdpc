# -*- coding: utf-8; Mode: Python -*-
#
# Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
# Copyright (C) 2010  Rogerio Hilbert Lima <rogerhil@gmail.com>
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

# Campos:
#
# * nome
# * tipo
# * tipo_convenio
# * numero_convenio
#
# * entidade proponente
#   * nome
#   * telefones
#   * endereco
#   * contato
#
# * responsavel
#   * nome
#   * email
#   * telefones
#
# * endereco
#   * logradouro
#   * numero
#   * bairro
#   * cidade
#   * estado
#   * complemento
#   * cep
#
# * contato
#   * telefone(s)
#   * email
#   * blog

import csv
import sys
sys.path.insert(0, '..')
from datetime import datetime
from time import strptime

from elixir import session
from sqlalchemy.exc import IntegrityError

from cdpc.app.usuarios.models import Pessoa
from cdpc.app.projetos.models import Projeto, Entidade
from cdpc.app.common.models import Endereco, Telefone
from cdpc.app.utils.model import get_or_create
from cdpc.main import setup_models

setup_models()


TIPOSTEL = {'8': u'Celular',
            '9': u'Celular',
            '7': u'Rádio'}
            #'2': u'Rural',
            #'2': u'Público'}

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

def get_tipo(tel):
    p = tel[0]
    tipo = TIPOSTEL.get(p, u'Fixo')
    return format(tipo)

def add_tel(tel_list, ddd, tel):
    ddd = ddd.strip()
    tel = tel.strip()
    if ddd and tel:
        tel = '%s%s' % (ddd, tel)
        tipo = get_tipo(tel)
        inst, _ = get_or_create(Telefone, numero=tel, tipo=tipo)
        session.commit()
        if not inst in tel_list:
            tel_list.append(inst)
        session.commit()

def clean_name(name):
    name = unicode(name.decode('utf-8')).strip()
    cap = lambda x: x.lower() if len(x) <= 2 or (len(x) == 3 and \
                    x.lower().endswith('s')) else x.capitalize()
    splited = name.split(' ')
    if splited:
        name = ' '.join(filter(None, [splited[0].capitalize()] + map(cap, splited[1:])))
    return name

def main():
    # Iterando sobre as entradas no arquivo csv gerado à partir do dump
    # do banco de dados colhido durante a teia2010.
    #
    # Todos os campos que começam com "p_" são relativos ao projeto, já
    # os que começam com "r_", são relativos ao responsável e,
    # finalmente, os que começam com "e_" são relativos à entidade
    # proponente. Meio tosco, mas é um script utilitário que vai ser
    # usado apenas uma vez, então... let the hammer fall!
    
    for i in list(csv.reader(file('pontos_teia2010.csv')))[1:]:
        (_, _, _, _,
         p_tipo, p_tipo_convenio, p_nome,
         p_logradouro, p_num, p_complemento, p_bairro, p_cep, p_cidade, p_uf,
         p_ddd1, p_tel1, p_ddd2, p_tel2, p_email, p_blog,
         r_nome, r_email, r_ddd, r_tel,
         e_nome,
         e_logradouro, e_num, e_complemento, e_bairro, e_cep, e_cidade, e_uf,
         e_ddd1, e_tel1, e_ddd2, e_tel2, e_email, e_blog,
         data_cadastro, hora_cadastro, _
         ) = i

        # Criando a linha para a pessoa responsável pelo projeto e suas
        # relações
        responsavel, created = get_or_create(Pessoa, email=r_email)
        if created:
            responsavel.nome = clean_name(r_nome)
            add_tel(responsavel.telefones, r_ddd, r_tel)

        # Criando a linha para a entidade responsável pelo projeto e
        # suas relações
        entidade = get_or_create(Entidade, nome=e_nome, email=e_email,
                                 website=e_blog)[0]
        
        entidade.endereco = get_or_create(Endereco, 
            logradouro=e_logradouro,
            numero=e_num,
            complemento=e_complemento,
            bairro=e_bairro,
            cep=e_cep,
            cidade=e_cidade,
            uf=e_uf)[0]

        add_tel(entidade.telefones, e_ddd1, e_tel1)
        add_tel(entidade.telefones, e_ddd2, e_tel2)

        # Finalmente, criando o projeto
        projeto = Projeto(
            nome=clean_name(p_nome),
            tipo=p_tipo,
            tipo_convenio=p_tipo_convenio,
            email=p_email,
            site=p_blog,
            entidade=entidade)

        projeto.endereco_sede = get_or_create(Endereco, 
                logradouro=clean_name(p_logradouro),
                numero=p_num,
                complemento=p_complemento,
                bairro=clean_name(p_bairro),
                cep=p_cep,
                cidade=clean_name(p_cidade),
                uf=p_uf)[0]

        add_tel(projeto.telefones, p_ddd1, p_tel1)
        add_tel(projeto.telefones, p_ddd2, p_tel2)

        data_cadastro = data_cadastro.strip()
        hora_cadastro = hora_cadastro.strip()
        data = ''
        if data_cadastro:
            data = data_cadastro
            formato = '%Y-%m-%d'
        if data_cadastro and hora_cadastro:
            data += ' %s' % hora_cadastro
            formato += ' %H:%M:%S'
        if data:
            time_st = strptime(data, formato)
            projeto.data_cadastro = datetime(*tuple(time_st)[:6])

        session.commit()

if __name__ == '__main__':
    main()
