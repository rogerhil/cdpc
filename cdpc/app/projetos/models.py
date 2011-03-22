# -*- coding: utf-8; Mode: Python -*-
#
# Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
# Copyright (C) 2010  Marco Túlio Gontijo e Silva <marcot@marcot.eti.br>
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

from elixir import using_options, Entity, Field, Unicode, DateTime, ManyToOne, \
    OneToMany, ManyToMany, Boolean, Integer

from ..common.models import Cadastrado

class Convenio(Entity):
    """Wrapper para a entidade convenio no banco de dados
    """
    using_options(shortnames=True)
    nome = Field(Unicode(128))
    outro_convenio = ManyToMany('Projeto')

class Documentacao(Entity):
    """Wrapper para a entidade documentacao no banco de dados
    """
    using_options(shortnames=True)
    doc = Field(Unicode(128)) # Caminho para o arquivo
    documentacoes = ManyToMany('Projeto')

class Parceiro(Entity):
    """Wrapper para a entidade parceiro no banco de dados
    """
    using_options(shortnames=True)
    nome = Field(Unicode(128))
    projeto = ManyToMany('Projeto')

class Entidade(Entity):
    using_options(shortnames=True)
    nome = Field(Unicode(256))
    convenios = ManyToMany('Convenio')
    endereco = ManyToOne('Endereco')
    telefones = ManyToMany('Telefone')
    email = Field(Unicode(256))
    website = Field(Unicode(256))
    projetos = OneToMany('Projeto')

class Atividade(Entity):
    using_options(shortnames=True)
    nome = Field(Unicode(256))
    projetos = ManyToMany('Projeto')

class PublicoAlvo(Entity):
    using_options(shortnames=True)
    nome = Field(Unicode(256))
    projetos = ManyToMany('Projeto')

class CulturaTradicional(Entity):
    using_options(shortnames=True)
    nome = Field(Unicode(256))
    projetos = ManyToMany('Projeto')

class OcupacaoDoMeio(Entity):
    using_options(shortnames=True)
    nome = Field(Unicode(256))
    projetos = ManyToMany('Projeto')

class Genero(Entity):
    using_options(shortnames=True)
    nome = Field(Unicode(256))
    projetos = ManyToMany('Projeto')

class ManifestacaoLinguagem(Entity):
    using_options(shortnames=True)
    nome = Field(Unicode(256))
    projetos = ManyToMany('Projeto')

class AcaoCulturaViva(Entity):
    using_options(shortnames=True)
    nome = Field(Unicode(256))
    projetos = ManyToMany('Projeto')

class Projeto(Cadastrado):
    """Wrapper para a entidade projeto no banco de dados
    """
    using_options(inheritance='multi', shortnames=True)

    # -- Responsável pelo projeto
    responsavel = ManyToOne('Pessoa', inverse='responsavel_por')
    participantes = ManyToMany('Pessoa')

    # -- Dados do projeto
    nome = Field(Unicode(256))
    tipo = Field(Unicode(32))
    tipo_convenio = Field(Unicode(64))
    numero_convenio = Field(Unicode(32))

    # -- Geolocalização
    endereco_sede = ManyToOne('Endereco')
    enderecos = ManyToMany('Endereco')
    local = Field(Unicode(16))

    # -- Comunicação e Cultura Digital
    email = Field(Unicode(256), unique=True)
    sede_possui_tel = Field(Boolean)
    pq_sem_tel = Field(Unicode(256))
    sede_possui_net = Field(Boolean)
    tipo_internet = Field(Unicode(16))
    pq_sem_internet = Field(Unicode(256))

    # -- Entidade Proponente
    entidade = ManyToOne('Entidade')

    # -- Atividades exercidas pelo projeto
    # --- Qual a área de atuação das atividades do Projeto?
    atividades = ManyToMany('Atividade')

    # ---  Com qual Público Alvo o Projeto é desenvolvido?
    # ---- Sob aspectos de Faixa Etária
    publico_alvo = ManyToMany('PublicoAlvo')

    # ---- Sob aspectos das Culturas Tradicionais
    culturas_tradicionais = ManyToMany('CulturaTradicional')

    # ---- Sob aspectos de Ocupação do Meio
    ocupacao_do_meio = ManyToMany('OcupacaoDoMeio')

    # ---- Sob aspectos de Gênero
    genero = ManyToMany('Genero')

    # --- Quais são as Manifestações e Linguagens que o Projeto utiliza
    # em suas atividades?
    manifestacoes_linguagens = ManyToMany('ManifestacaoLinguagem')

    # --- O Projeto participa de alguma Ação do Programa Cultura Viva?
    acao_cultura_viva = ManyToMany('AcaoCulturaViva')

    descricao = Field(Unicode(1024))
    documentacoes = ManyToMany('Documentacao')

    # -- Parcerias do Projeto
    parcerias = ManyToMany('Parceiro')

    # -- Índice de acesso à cultura
    ind_oficinas = Field(Integer)
    ind_expectadores = Field(Integer)
    ind_populacao = Field(Integer)

    # -- Avatar
    avatar = Field(Unicode(256)) # Caminho para o arquivo

    def cadastrado_por(self):
        return getattr(self.responsavel, 'nome', '')

