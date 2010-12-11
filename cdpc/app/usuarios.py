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
from hashlib import sha1
from math import ceil
from formencode import Invalid, htmlfill
from simplejson import dumps, loads
from flask import Module, request, render_template, flash, make_response, \
                  redirect
from elixir import session

from . import schemas
from . import models
from .cadastro import VALORES_UF

module = Module(__name__)

@module.route('/')
def listing():
    count = models.Pessoa.query.count()
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))

    pages = ceil(count / limit)
    index = limit*(page-1)

    query = models.Pessoa.query.slice(index, index+limit)
    lista = query.all()
    limit = min(limit, query.count())

    pagination = dict(count=count, limit=limit, pages=pages,
                      page=page)
    return render_template('usuarios/listing.html',
                           lista=lista,
                           pagination=pagination,
                           vals_uf=VALORES_UF)

@module.route("novo/", methods=('GET', 'POST'))
def novo():
    """Renderiza o formulário de cadastro de usuários
    """
    if request.method == 'POST':
        # instanciando o validador
        validator = schemas.Usuario()
        validado = {}
        try:
            validado = validator.to_python(request.form)
            clean_list = lambda x: [i for i in x if i.strip()];

        except Invalid, e:
            rendered = render_template(
                        'usuarios/novo.html',
                        vals_uf=VALORES_UF,
                        errors=dict([(i,j) for i,j in e.unpack_errors().items() if type(j) == list]),
                        values=[i for i  in request.form.lists() if len(i[1]) > 1])
            errors = e.error_dict
            error_tag = lambda x : '<label generated="true" class="error">%s</label>' % x
            filled = htmlfill.render(rendered, request.form.to_dict(), errors, prefix_error=False, auto_error_formatter=error_tag)
            return make_response(filled)

        else:
            # Instanciando o modelo e associando os campos validados e
            # transformados em valores python à instância que será
            # salva no db.

            usuario = models.Pessoa()
            usuario.ip_addr = request.remote_addr

            # -- Dados de acesso
            usuario.email = validado['email']
            usuario.senha = sha1(validado['senha']).hexdigest()

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
            usuario.website = validado['website']
            for i in validado['telefone']:
                tel = models.Telefone()
                tel.numero = i
                usuario.telefones.append(tel)
            
            if validado.has_key('rs_nome'):
                for i in range(len(validado['rs_nome'])):
                    rsocial = models.RedeSocial()
                    rsocial.nome = validado['rs_nome'][i]
                    rsocial.link = validado['rs_link'][i]
                    usuario.redes_sociais.append(rsocial)
            if validado.has_key('feed_nome'):
                for i in range(len(validado['feed_nome'])):
                    feed = models.Feed()
                    feed.nome = validado['feed_nome'][i]
                    feed.link = validado['feed_link'][i]
                    usuario.feeds.append(feed)

            try:
                session.commit()
            except Exception, e:
                session.rollback()
                raise e

            flash(u'Usuário cadastrado com sucesso!', 'success')
            return redirect("/usuarios/")

    return render_template('usuarios/novo.html', vals_uf=VALORES_UF)

