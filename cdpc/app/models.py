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

"""Contém os modelos das tabelas que serão usadas no projeto
"""

from datetime import datetime
from elixir import metadata, setup_all, using_options, Entity, Field, \
    Unicode, DateTime, ManyToOne, OneToMany, ManyToMany
from ..config import DATABASE_URI

class Telefone(Entity):
    """Wrapper para a entidade telefone no banco de dados
    """
    numero = Field(Unicode(32))
    pessoas = ManyToMany('Pessoa')

class RedeSocial(Entity):
    """Wrapper para a entidade redesocial no banco de dados
    """
    nome = Field(Unicode(128))
    link = Field(Unicode(128))
    pessoas = ManyToMany('Pessoa')

class Feed(Entity):
    """Wrapper para a entidade feed no banco de dados
    """
    nome = Field(Unicode(128))
    link = Field(Unicode(128))
    pessoas = ManyToMany('Pessoa')

class Endereco(Entity):
    """Wrapper para a entidade endereco no banco de dados
    """
    cep = Field(Unicode(8))
    numero = Field(Unicode(16))
    logradouro = Field(Unicode(128))
    complemento = Field(Unicode(128))
    uf = Field(Unicode(2))
    cidade = Field(Unicode(128))
    bairro = Field(Unicode(128))
    latitude = Field(Unicode(16))
    longitude = Field(Unicode(16))

    cadastrado = ManyToOne('Cadastrado')

class Cadastrado(Entity):
    """Classe base para Pessoa e Projeto
    """
    using_options(inheritance='multi')

    # -- Meta informação
    data_cadastro = Field(DateTime, default=datetime.now)
    ip_addr = Field(Unicode(16))

    # -- Geolocalização
    endereco = OneToMany('Endereco')

    # -- Contatos e espaços na rede
    telefones = ManyToMany(Telefone, inverse='pessoas')
    email = Field(Unicode(256), unique=True)
    website = Field(Unicode(256))
    redes_sociais = ManyToMany(RedeSocial, inverse='pessoas')
    feeds = ManyToMany(Feed, inverse='pessoas')

class Pessoa(Cadastrado):
    """Wrapper para a entidade pessoa no banco de dados
    """
    using_options(inheritance='multi')

    # -- Dados pessoais
    nome = Field(Unicode(256))
    cpf = Field(Unicode(11))
    data_nascimento = Field(DateTime)
    sexo = Field(Unicode(16))
    avatar = Field(Unicode(128))

    # -- Dados de acesso
    usuario = Field(Unicode(64))
    senha = Field(Unicode(256))

class Projeto(Entity):
    """Wrapper para a entidade projeto no banco de dados
    """
    using_options(inheritance='multi')

    # -- Dados do projeto
    numero = Field(Unicode(12))
    nome = Field(Unicode(256))


metadata.bind = DATABASE_URI
metadata.bind.echo = True
setup_all()
