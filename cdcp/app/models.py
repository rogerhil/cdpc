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
from elixir import metadata, setup_all, Entity, Field, Unicode, \
     DateTime, ManyToMany
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

class Pessoa(Entity):
    """Wrapper para a entidade pessoa no banco de dados
    """
    # -- Meta informação
    data_cadastro = Field(DateTime, default=datetime.now)
    ip_addr = Field(Unicode(16))

    # -- Dados pessoais
    nome = Field(Unicode(256))
    cpf = Field(Unicode(11))
    data_nascimento = Field(DateTime)
    sexo = Field(Unicode(16))
    avatar = Field(Unicode(128))

    # -- Geolocalização
    end_cep = Field(Unicode(8))
    end_numero = Field(Unicode(16))
    end_logradouro = Field(Unicode(128))
    end_uf = Field(Unicode(2))
    end_cidade = Field(Unicode(128))
    end_bairro = Field(Unicode(128))
    end_latitude = Field(Unicode(16))
    end_longitude = Field(Unicode(16))

    # -- Contatos e espaços na rede
    telefones = ManyToMany(Telefone, inverse='pessoas')
    email = Field(Unicode(256), unique=True)
    website = Field(Unicode(256))
    redes_sociais = ManyToMany(RedeSocial, inverse='pessoas')
    feeds = ManyToMany(Feed, inverse='pessoas')

    # -- Dados de acesso
    usuario = Field(Unicode(64))
    senha = Field(Unicode(256))

metadata.bind = DATABASE_URI
metadata.bind.echo = True
setup_all()
