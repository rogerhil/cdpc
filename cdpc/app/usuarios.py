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
from elixir import session

from . import validators
from . import models
from .cadastro import VALORES_UF

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
            clean_list = lambda x: [i for i in x if i.strip()];

            rs_nomes = clean_list(request.form.getlist('rs_nome'))
            rs_links = clean_list(request.form.getlist('rs_link'))
            assert len(rs_nomes) == len(rs_links)

            feed_nomes = clean_list(request.form.getlist('feed_nome'))
            feed_links = clean_list(request.form.getlist('feed_link'))
            assert len(feed_nomes) == len(feed_links)

        except Invalid, e:
            # Dar um feedback pro usuário usando a instância da
            # exceção "e".
            pass
        except AssertionError, e:
            # Feedback sobre erros nos campos de lista
            pass
        else:
            # Instanciando o modelo e associando os campos validados e
            # transformados em valores python à instância que será
            # salva no db.

            usuario = models.Pessoa()
            usuario.ip_addr = request.remote_addr

            # -- Dados pessoais
            usuario.nome = validado['nome']
            usuario.cpf = validado['cpf']
            usuario.data_nascimento = validado['data_nascimento']
            usuario.sexo = validado['sexo']

            # -- Sobre a sua localização geográfica
            endereco = models.Endereco()
            endereco.cep = validado['end_cep']
            endereco.uf = validado['end_uf']
            endereco.cidade = validado['end_cidade']
            endereco.bairro = validado['end_bairro']
            endereco.logradouro = validado['end_logradouro']
            endereco.numero = validado['end_numero']
            endereco.complemento = validado['end_complemento']
            endereco.latitude = validado['end_latitude']
            endereco.longitude = validado['end_longitude']
            usuario.endereco.append(endereco)

            # -- Contatos e espaços na rede
            usuario.email = validado['email']
            usuario.website = validado['website']
            for i in request.form.getlist('telefone'):
                tel = models.Telefone()
                tel.numero = i
                usuario.telefones.append(tel)

            for i in range(len(rs_nomes)):
                rsocial = models.RedeSocial()
                rsocial.nome = rs_nomes[i]
                rsocial.link = rs_links[i]
                usuario.redes_sociais.append(rsocial)

            for i in range(len(feed_nomes)):
                feed = models.Feed()
                feed.nome = feed_nomes[i]
                feed.link = feed_links[i]
                usuario.feeds.append(feed)

            try:
                session.commit()
            except Exception, e:
                session.rollback()
                raise e

            # FIXME: Avisar ao usuário que tudo deu certo.

    return render_template(
        'usuarios/novo.html',
        vals_uf=VALORES_UF)
