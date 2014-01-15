# -*- coding: utf-8; Mode: Python -*-
#
# Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
# Copyright (C) 2010  Marco Túlio Gontijo e Silva <marcot@marcot.eti.br>
# Copyright (C) 2010  Rogério Hilbert Lima <rogerhil@gmail.com>
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

"""Contém os modelos das tabelas que serão usadas nos projetos e usuários
"""

from datetime import datetime
from elixir import using_options, Entity, Field, Unicode, DateTime, ManyToOne, \
    OneToMany, ManyToMany

class Telefone(Entity):
    """Wrapper para a entidade telefone no banco de dados
    """
    using_options(shortnames=True)
    numero = Field(Unicode(32))
    tipo = Field(Unicode(32))
    cadastrado = ManyToMany('Cadastrado')
    entidades = ManyToMany('Entidade')

class RedeSocial(Entity):
    """Wrapper para a entidade redesocial no banco de dados
    """
    using_options(shortnames=True)
    nome = Field(Unicode(128))
    link = Field(Unicode(128))
    cadastrado = ManyToMany('Cadastrado')

class Feed(Entity):
    """Wrapper para a entidade feed no banco de dados
    """
    using_options(shortnames=True)
    nome = Field(Unicode(128))
    link = Field(Unicode(128))
    cadastrado = ManyToMany('Cadastrado')

class Endereco(Entity):
    """Wrapper para a entidade endereco no banco de dados
    """
    using_options(shortnames=True)
    nome = Field(Unicode(128), default=u"")
    cep = Field(Unicode(8))
    numero = Field(Unicode(16))
    logradouro = Field(Unicode(128))
    complemento = Field(Unicode(128))
    uf = Field(Unicode(2))
    cidade = Field(Unicode(128))
    bairro = Field(Unicode(128))
    latitude = Field(Unicode(16))
    longitude = Field(Unicode(16))

    # -- relacionamentos
    pessoas = OneToMany('Pessoa')
    projetos = ManyToMany('Projeto')
    projeto = OneToMany('Projeto')
    entidades = OneToMany('Entidade')

class Cadastrado(Entity):
    """Classe base para Pessoa e Projeto
    """
    using_options(inheritance='multi', shortnames=True)

    # -- Meta informação
    data_cadastro = Field(DateTime, default=datetime.now)
    ip_addr = Field(Unicode(16))

    # -- Contatos e espaços na rede
    telefones = ManyToMany(Telefone, inverse='cadastrado')
    email = Field(Unicode(256))
    website = Field(Unicode(256))
    redes_sociais = ManyToMany(RedeSocial, inverse='cadastrado')
    feeds = ManyToMany(Feed, inverse='cadastrado')

