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

from datetime import datetime
from elixir import metadata, setup_all, using_options, Entity, Field, \
    Unicode, DateTime, ManyToOne, OneToMany, ManyToMany, Boolean, Integer, \
    session
from ..config import DATABASE_URI

def get_or_create(model, **kwargs):
    """Helper function to search for an object or create it otherwise,
    based on the Django's Model.get_or_create() method.
    """
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = {}
        for k, v in kwargs.iteritems():
            params[k] = v
        instance = model(**params)
        session.add(instance)
        return instance, True    

class Telefone(Entity):
    """Wrapper para a entidade telefone no banco de dados
    """
    using_options(shortnames=True)
    numero = Field(Unicode(32), unique=True)
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
    pessoas = ManyToMany('Pessoa')
    projetos = ManyToMany('Projeto')
    entidades = ManyToMany('Entidade')

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
    cpf = Field(Unicode(11))
    data_nascimento = Field(DateTime)
    sexo = Field(Unicode(16))
    avatar = Field(Unicode(128))
    email = Field(Unicode(256))
    site = Field(Unicode(256))

    # -- Geolocalização
    endereco = ManyToMany('Endereco')

    # -- Dados de acesso
    # O email será usado como login.
    senha = Field(Unicode(256))

class Entidade(Entity):
    using_options(shortnames=True)
    nome = Field(Unicode(256))
    convenios = ManyToMany('Convenio')
    enderecos = ManyToMany('Endereco')
    telefones = ManyToMany('Telefone')
    email = Field(Unicode(256))
    site = Field(Unicode(256))
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
    responsavel = ManyToMany('Pessoa', inverse='responsavel_por')
    participantes = ManyToMany('Pessoa')

    # -- Dados do projeto
    nome = Field(Unicode(256))
    tipo = Field(Unicode(32))
    tipo_convenio = Field(Unicode(64))
    numero_convenio = Field(Unicode(32))

    # -- Geolocalização
    enderecos = ManyToMany('Endereco')
    local = Field(Unicode(16))

    # -- Comunicação e Cultura Digital
    email = Field(Unicode(256))
    site = Field(Unicode(256))
    sede_possui_tel = Field(Boolean)
    tipo_tel_sede = Field(Unicode(7))
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
    avatar = Field(Unicode(128)) # Caminho para o arquivo

    def cadastrado_por(self):
        return " ".join([resp.nome for resp in self.responsavel])

class SiteMessage(Entity):
    text = Field(Unicode(1024))
    status =  Field(Unicode(64))
    data = Field(DateTime, default=datetime.now)
    usuario = ManyToOne('Pessoa')
    
    _possible_status = ['info', 'success', 'warning', 'error']
    
    @staticmethod
    def create(text, user, status='info'):
        if not status in SiteMessage._possible_status:
            raise Exception("%s is not a possible status. Expected: " \
                            % (status, ", ".join(SiteMessage._possible_status)))
        from elixir import session
        msg = SiteMessage(text=text, usuario=user, status=status)
        try:
            session.commit()
        except Exception, e:
            session.rollback()
            raise e
        return msg

    @staticmethod
    def get_list(user):
        dict_list = [msg.__dict__.copy() for msg in SiteMessage.query.filter_by(usuario=user)]
        SiteMessage.query.filter_by(usuario=user).delete()
        try:
            session.commit()
        except Exception, e:
            session.rollback()
            raise e
        return dict_list
    
metadata.bind = DATABASE_URI
metadata.bind.echo = True
setup_all()
