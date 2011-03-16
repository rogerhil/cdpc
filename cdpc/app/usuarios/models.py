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

"""Contém os modelos das tabelas que serão usadas nos usuários
"""

from elixir import metadata, setup_all, using_options, Entity, Field, Unicode, \
    DateTime, ManyToOne, ManyToMany

from ...config import DATABASE_URI
from ..common.models import Cadastrado

class Pessoa(Cadastrado):
    """Wrapper para a entidade pessoa no banco de dados
    """
    using_options(inheritance='multi', shortnames=True)

    responsavel_por = ManyToMany('Projeto', inverse='responsavel')
    projetos = ManyToMany('Projeto')

    # -- Sobre sua participação
    participacao = Field(Unicode(20))
    papel = Field(Unicode(26))
    nome_iniciativa = Field(Unicode(128))

    # -- Dados pessoais
    nome = Field(Unicode(256))
    cpf = Field(Unicode(11), unique=True)
    data_nascimento = Field(DateTime)
    sexo = Field(Unicode(16))
    avatar = Field(Unicode(256))

    # -- Geolocalização
    endereco = ManyToOne('Endereco')

    # -- Dados de acesso
    # O email será usado como login.
    email = Field(Unicode(256), unique=True)
    senha = Field(Unicode(256))

