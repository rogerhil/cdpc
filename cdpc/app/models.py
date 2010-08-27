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
    Unicode, DateTime, ManyToOne, OneToMany, ManyToMany, Boolean, Integer
from ..config import DATABASE_URI

class Telefone(Entity):
    """Wrapper para a entidade telefone no banco de dados
    """
    numero = Field(Unicode(32))
    cadastrado = ManyToMany('Cadastrado')
    tel_proj = ManyToMany('Projeto')
    tel_ent = ManyToMany('Telefone')

class RedeSocial(Entity):
    """Wrapper para a entidade redesocial no banco de dados
    """
    nome = Field(Unicode(128))
    link = Field(Unicode(128))
    cadastrado = ManyToMany('Cadastrado')

class Feed(Entity):
    """Wrapper para a entidade feed no banco de dados
    """
    nome = Field(Unicode(128))
    link = Field(Unicode(128))
    cadastrado = ManyToMany('Cadastrado')

class Convenio(Entity):
    """Wrapper para a entidade convenio no banco de dados
    """
    nome = Field(Unicode(128))
    outro_convenio = ManyToMany('Projeto')

class Documentacao(Entity):
    """Wrapper para a entidade documentacao no banco de dados
    """
    doc = Field(Unicode(128)) # Caminho para o arquivo
    documentacoes = ManyToMany('Projeto')

class Parceiro(Entity):
    """Wrapper para a entidade parceiro no banco de dados
    """
    nome = Field(Unicode(128))
    parc_nome = ManyToMany('Projeto')

class Endereco(Entity):
    """Wrapper para a entidade endereco no banco de dados
    """
    nome = Field(Unicode(128))
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
    pessoas = ManyToOne('Pessoa')
    end_proj = ManyToOne('Projeto')
    end_outros = ManyToMany('Projeto')
    end_ent = ManyToOne('Projeto')

class Cadastrado(Entity):
    """Classe base para Pessoa e Projeto
    """
    using_options(inheritance='multi')

    # -- Meta informação
    data_cadastro = Field(DateTime, default=datetime.now)
    ip_addr = Field(Unicode(16))

    # -- Contatos e espaços na rede
    telefones = ManyToMany(Telefone, inverse='cadastrado')
    email = Field(Unicode(256), unique=True)
    website = Field(Unicode(256))
    redes_sociais = ManyToMany(RedeSocial, inverse='cadastrado')
    feeds = ManyToMany(Feed, inverse='cadastrado')

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

    # -- Geolocalização
    endereco = OneToMany('Endereco')

    # -- Dados de acesso
    usuario = Field(Unicode(64))
    senha = Field(Unicode(256))

class Projeto(Entity):
    """Wrapper para a entidade projeto no banco de dados
    """
    using_options(inheritance='multi')

    # -- Dados do projeto
    voce_eh = Field(Unicode(19))
    tipo_convenio = Field(Unicode(13))
    numero_convenio = Field(Unicode(12))
    nome_proj = Field(Unicode(256))

    # -- Geolocalização
    end_proj = OneToMany('Endereco', inverse='end_proj')
    local_proj = Field(Unicode(10))
    end_outros = ManyToMany('Endereco')

    # -- Comunicação e Cultura Digital
    sede_possui_tel = Field(Boolean)
    tipo_tel_sede = Field(Unicode(7))
    pq_sem_tel = Field(Unicode(12))
    pq_sem_tel_outro = Field(Unicode(256))
    sede_possui_net = Field(Boolean)
    tipo_internet = Field(Unicode(7))
    pq_sem_internet = Field(Unicode(12))
    pq_sem_internet_outro = Field(Unicode(256))

    # -- Entidade Proponente
    nome_ent = Field(Unicode(256))
    endereco_ent_proj = Field(Boolean)
    end_ent = OneToMany('Endereco', inverse='end_ent')
    tel_ent = ManyToMany('Telefone')
    email_ent = Field(Unicode(256), unique=True)
    website_ent = Field(Unicode(256))
    convenio_ent = Field(Boolean)
    outro_convenio = ManyToMany('Convenio')

    # -- Atividades exercidas pelo projeto
    # --- Qual a área de atuação das atividades do Projeto?
    cultura_popular = Field(Boolean)
    direitos_humanos = Field(Boolean)
    economia_solidaria = Field(Boolean)
    educacao = Field(Boolean)
    esportes_e_lazer = Field(Boolean)
    etnia = Field(Boolean)
    genero = Field(Boolean)
    habitacao = Field(Boolean)
    meio_ambiente = Field(Boolean)
    memoria = Field(Boolean)
    patrimonio_historico_imaterial = Field(Boolean)
    patrimonio_historico_material = Field(Boolean)
    pesquisa_e_extensao = Field(Boolean)
    povos_tradicionais = Field(Boolean)
    recreacao = Field(Boolean)
    religiao = Field(Boolean)
    saude = Field(Boolean)
    sexualidade = Field(Boolean)
    tecnologia = Field(Boolean)
    trabalho = Field(Boolean)
    outras_atividades = Field(Boolean)
    quais_outras_atividades = Field(Unicode(128))

    # ---  Com qual Público Alvo o Projeto é desenvolvido?
    # ---- Sob aspectos de Faixa Etária
    criancas = Field(Boolean)
    adolescentes = Field(Boolean)
    adultos = Field(Boolean)
    jovens = Field(Boolean)

    # ---- Sob aspectos das Culturas Tradicionais
    quilombola = Field(Boolean)
    pomerano = Field(Boolean)
    caicara = Field(Boolean)
    indigena = Field(Boolean)
    cigana = Field(Boolean)
    povos_da_floresta = Field(Boolean)
    ribeirinhos = Field(Boolean)
    outras_culturas = Field(Boolean)
    quais_outras_culturas = Field(Unicode(128))

    # ---- Sob aspectos de Ocupação do Meio
    rural = Field(Boolean)
    urbano = Field(Boolean)
    outro = Field(Boolean)
    outra_ocupacao = Field(Boolean)
    qual_outra_ocupacao = Field(Unicode(128))

    # ---- Sob aspectos de Gênero
    mulheres = Field(Boolean)
    homens = Field(Boolean)
    lgbt = Field(Boolean)

    # --- Quais são as Manifestações e Linguagens que o Projeto utiliza em suas
    # atividades?
    artes_digitais = Field(Boolean)
    artes_plasticas = Field(Boolean)
    audiovisual = Field(Boolean)
    circo = Field(Boolean)
    culinaria = Field(Boolean)
    danca = Field(Boolean)
    fotografia = Field(Boolean)
    grafite = Field(Boolean)
    internet = Field(Boolean)
    jornalismo = Field(Boolean)
    literatura = Field(Boolean)
    musica = Field(Boolean)
    radio = Field(Boolean)
    teatro = Field(Boolean)
    tecnologias_digitais = Field(Boolean)
    tradicao_oral = Field(Boolean)
    tv = Field(Boolean)
    outras_manifestacoes = Field(Boolean)
    quais_outras_manifestacoes = Field(Unicode(128))

    # --- O Projeto participa de alguma Ação do Programa Cultura Viva?
    participa_cultura_viva = Field(Boolean)
    agente_cultura_viva = Field(Boolean)
    cultura_digital = Field(Boolean)
    cultura_e_saude = Field(Boolean)
    economia_viva = Field(Boolean)
    escola_viva = Field(Boolean)
    grios = Field(Boolean)
    interacoes_esteticas = Field(Boolean)
    midias_livres = Field(Boolean)
    pontinho_de_cultura = Field(Boolean)
    pontos_de_memoria = Field(Boolean)
    redes_indigenas = Field(Boolean)
    tuxaua = Field(Boolean)

    descricao = Field(Unicode(1024))
    documentacoes = ManyToMany('Documentacao')

    # -- Parcerias do Projeto
    parcerias = Field(Boolean)
    parc_biblioteca = Field(Boolean)
    parc_empresa = Field(Boolean)
    parc_equipamento_de_saude = Field(Boolean)
    parc_escola = Field(Boolean)
    parc_igreja = Field(Boolean)
    parc_ong = Field(Boolean)
    parc_poder_publico = Field(Boolean)
    parc_pontos_de_memoria = Field(Boolean)
    parc_redes_indigenas = Field(Boolean)
    parc_sistema_s = Field(Boolean)
    parc_tuxaua = Field(Boolean)
    outros_parceiros = Field(Boolean)
    quais_outros_parceiros = Field(Unicode(128))
    parc_nome = ManyToMany('Parceiro')

    # -- Índice de acesso à cultura
    ind_oficinas = Field(Integer)
    ind_expectadores = Field(Integer)
    ind_populacao = Field(Integer)

    # -- Avatar
    avatar = Field(Unicode(128)) # Caminho para o arquivo

metadata.bind = DATABASE_URI
metadata.bind.echo = True
setup_all()
