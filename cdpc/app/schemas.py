# -*- coding: utf-8; Mode: Python -*-
#
# Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
# Copyright (C) 2010  Ministério da Cultura <http://cultura.gov.br>
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

import formencode, re
from formencode import validators
from formencode.validators import _, Invalid

from formencode.interfaces import *
from formencode.api import *
from formencode.schema import format_compound_error
from validators import CpfValidator, Cep, BrazilPhoneNumber, Dependent, \
                       AtLeastOne


class CdpcSchema(formencode.Schema):
    """
    Customized schema to treat depending fields
    """
    def _to_python(self, value_dict, state):
        if value_dict:
            for name in self.fields.keys():
                validator = self.fields[name]                
                if hasattr(validator, 'depend_field') and \
                   validator.depend_field:
                    fname, fvalue = validator.depend_field
                    if value_dict.has_key(fname) and \
                       value_dict[fname] != fvalue or \
                       not value_dict.has_key(fname):
                        if value_dict.has_key(name):
                            del value_dict[name]
                        del self.fields[name]
        print "oioioi"
        print value_dict
        print "oioioi"
        return super(CdpcSchema, self)._to_python(value_dict, state)


################################################################################
# Usuario Validation


class Usuario(formencode.Schema):
    # -- Dados de acesso
    senha = validators.String(not_empty=True)
    confirmar_senha = validators.String(not_empty=True)
    email = validators.String(not_empty=True)
    # TODO: Comparar senha original e confimada

    # -- Dados pessoais
    nome = validators.String(not_empty=True)
    cpf = CpfValidator(not_empty=True)
    data_nascimento = validators.DateConverter(month_style='dd/mm/yyyy')
    sexo = validators.String(not_empty=True)
    telefone = validators.String(not_empty=True)
    avatar = validators.FieldStorageUploadConverter()

    # -- Sobre a sua geolocalização
    end_cep = validators.String(not_empty=True)
    end_numero = validators.String(not_empty=True)
    end_uf = validators.String(not_empty=True)
    end_cidade = validators.String(not_empty=True)
    end_bairro = validators.String(not_empty=True)
    end_logradouro = validators.String(not_empty=True)
    end_complemento = validators.String()
    end_longitude = validators.String()
    end_latitude = validators.String()

    # -- Contatos e Espaços na rede
    website = validators.URL()
    rs_nome = validators.String()
    rs_link = validators.String()
    feed_nome = validators.String()
    feed_link = validators.String()


################################################################################
# Classes for Projeto Validation Wizard:
# - DadosProjeto
# - LocalizacaoGeoProjeto
# - ContatosEspacoRede
# - ComunicacaoCulturaDigital
# - EntidadeProponente
# - AtividadesExercidasProjeto
# - ParceriasProjeto
# - IndiceAcessoCultura
# - Avatar
#


class Projeto:
    class DadosProjeto(formencode.Schema):
        nome = validators.String(not_empty=True)
        tipo = validators.String(not_empty=True)
        tipo_convenio = validators.String(not_empty=True)
        numero_convenio = validators.String(not_empty=True)


    class LocalizacaoGeoProjeto(CdpcSchema):
        end_proj_cep = Cep(not_empty=True)
        end_proj_numero = validators.String(not_empty=True)
        end_proj_logradouro = validators.String(not_empty=True)
        end_proj_complemento = validators.String()
        end_proj_uf = validators.String(not_empty=True)
        end_proj_cidade = validators.String(not_empty=True)
        end_proj_bairro = validators.String(not_empty=True)
        end_proj_latitude = validators.String()
        end_proj_longitude = validators.String()
        local_proj = validators.String(not_empty=True)
        end_outro_nome = Dependent(schema=formencode.ForEach(validators.String(not_empty=True)), depend_field=('local_proj', 'outros'))
        end_outro_cep = Dependent(schema=formencode.ForEach(validators.String(not_empty=True)), depend_field=('local_proj', 'outros'))
        end_outro_numero = Dependent(schema=formencode.ForEach(validators.String(not_empty=True)), depend_field=('local_proj', 'outros'))
        end_outro_logradouro = Dependent(schema=formencode.ForEach(validators.String(not_empty=True)), depend_field=('local_proj', 'outros'))
        end_outro_complemento = Dependent(schema=formencode.ForEach(validators.String()), depend_field=('local_proj', 'outros'))
        end_outro_uf = Dependent(schema=formencode.ForEach(validators.String(not_empty=True)), depend_field=('local_proj', 'outros'))
        end_outro_cidade = Dependent(schema=formencode.ForEach(validators.String(not_empty=True)), depend_field=('local_proj', 'outros'))
        end_outro_bairro = Dependent(schema=formencode.ForEach(validators.String(not_empty=True)), depend_field=('local_proj', 'outros'))
        end_outro_latitude = Dependent(schema=formencode.ForEach(validators.String()), depend_field=('local_proj', 'outros'))
        end_outro_longitude = Dependent(schema=formencode.ForEach(validators.String()), depend_field=('local_proj', 'outros'))


    class ContatosEspacoRede(CdpcSchema):
        proj_tel = formencode.ForEach(BrazilPhoneNumber(not_empty=True))
        email_proj = validators.Email(not_empty=True)
        website_proj = validators.URL()
        frequencia = validators.String()
        rs_nome = validators.String()
        rs_link = validators.String()
        feed_nome = validators.String()
        feed_link = validators.String()


    class ComunicacaoCulturaDigital(CdpcSchema):
        sede_possui_tel = validators.String(not_empty=True)
        tipo_tel_sede = Dependent(schema=validators.String(not_empty=True), depend_field=('sede_possui_tel', 'sim'))
        pq_sem_tel = Dependent(schema=validators.String(not_empty=True), depend_field=('sede_possui_tel', 'nao'))
        pq_sem_tel_outro = Dependent(schema=validators.String(not_empty=True), depend_field=('pq_sem_tel', 'outro'))
        sede_possui_net = validators.String(not_empty=True)
        tipo_internet =  Dependent(schema=validators.String(not_empty=True), depend_field=('sede_possui_net', 'sim'))
        pq_sem_internet =  Dependent(schema=validators.String(not_empty=True), depend_field=('sede_possui_net', 'nao'))
        pq_sem_internet_outro =  Dependent(schema=validators.String(not_empty=True), depend_field=('pq_sem_internet', 'outro'))



    class EntidadeProponente(CdpcSchema):
        nome_ent = validators.String(not_empty=True)
        endereco_ent_proj = validators.String(not_empty=True)

        end_ent_cep = Dependent(schema=validators.String(not_empty=True), depend_field=('endereco_ent_proj', 'nao'))
        end_ent_numero = Dependent(schema=validators.String(not_empty=True), depend_field=('endereco_ent_proj', 'nao'))
        end_ent_logradouro = Dependent(schema=validators.String(not_empty=True), depend_field=('endereco_ent_proj', 'nao'))
        end_ent_complemento = Dependent(schema=validators.String(), depend_field=('endereco_ent_proj', 'nao'))
        end_ent_uf = Dependent(schema=validators.String(not_empty=True), depend_field=('endereco_ent_proj', 'nao'))
        end_ent_cidade = Dependent(schema=validators.String(not_empty=True), depend_field=('endereco_ent_proj', 'nao'))
        end_ent_bairro = Dependent(schema=validators.String(not_empty=True), depend_field=('endereco_ent_proj', 'nao'))
        end_ent_latitude = Dependent(schema=validators.String(), depend_field=('endereco_ent_proj', 'nao'))
        end_ent_longitude = Dependent(schema=validators.String(), depend_field=('endereco_ent_proj', 'nao'))

        ent_tel = formencode.ForEach(BrazilPhoneNumber())
        email_ent = validators.String()
        website_ent = validators.URL()
        convenio_ent = validators.String(not_empty=True)
        outro_convenio = Dependent(schema=validators.String(not_empty=True), depend_field=('convenio_ent', 'sim'))


    class AtividadesExercidasProjeto(CdpcSchema):
        atividade = formencode.ForEach(validators.String(not_empty=True))

        # ---  Com qual Público Alvo o Projeto é desenvolvido?
        # ---- Sob aspectos de Faixa Etária
        publico_alvo = formencode.ForEach(validators.String(not_empty=True))

        # ---- Sob aspectos das Culturas Tradicionais
        culturas_tradicionais = formencode.ForEach(
            validators.String(not_empty=True))

        # ---- Sob aspectos de Ocupação do Meio
        ocupacao_do_meio = formencode.ForEach(validators.String(not_empty=True))

        # ---- Sob aspectos de Gênero
        genero = formencode.ForEach(validators.String(not_empty=True))

        # --- Quais são as Manifestações e Linguagens que o Projeto utiliza
        # em suas atividades?
        manifestacoes_linguagens = formencode.ForEach(validators.String(not_empty=True))

        participa_cultura_viva = validators.String(not_empty=True)

        # --- O Projeto participa de alguma Ação do Programa Cultura Viva?
        acao_cultura_viva = Dependent(schema=AtLeastOne(schema=formencode.ForEach(validators.String())), depend_field=('participa_cultura_viva', 'sim'))

        descricao = validators.String()

        documentacoes = validators.FieldStorageUploadConverter()


    class ParceriasProjeto(CdpcSchema):
        estabeleceu_parcerias = validators.String(not_empty=True)
        parcerias = Dependent(schema=AtLeastOne(schema=formencode.ForEach(validators.String())), depend_field=('estabeleceu_parcerias', 'sim'))


    class IndiceAcessoCultura(formencode.Schema):
        # -- Índice de acesso à cultura
        ind_oficinas = validators.Int()
        ind_expectadores = validators.Int()
        ind_populacao = validators.Int()


    class Avatar(formencode.Schema):
        avatar = validators.FieldStorageUploadConverter()


################################################################################
# Class Projeto, old implementation


class ProjetoOld(formencode.Schema):
    # -- Dados do projeto
    nome = validators.String(not_empty=True)
    tipo = validators.String(not_empty=True)
    tipo_convenio = validators.String(not_empty=True)
    numero_convenio = validators.String(not_empty=True)

    # -- Localização geográfica do projeto
    end_proj_cep = validators.String(not_empty=True)
    end_proj_numero = validators.String(not_empty=True)
    end_proj_logradouro = validators.String(not_empty=True)
    end_proj_complemento = validators.String()
    end_proj_uf = validators.String(not_empty=True)
    end_proj_cidade = validators.String(not_empty=True)
    end_proj_bairro = validators.String(not_empty=True)
    end_proj_latitude = validators.String()
    end_proj_longitude = validators.String()
    local_proj = validators.String(not_empty=True)
    end_outro_nome = validators.String()
    end_outro_cep = validators.String()
    end_outro_numero = validators.String()
    end_outro_logradouro = validators.String()
    end_outro_complemento = validators.String()
    end_outro_uf = validators.String()
    end_outro_cidade = validators.String()
    end_outro_bairro = validators.String()
    end_outro_latitude = validators.String()
    end_outro_longitude = validators.String()

    # -- Contatos e espaços na rede
    proj_tel = formencode.ForEach(BrazilPhoneNumber())
    email_proj = validators.Email(not_empty=True)
    website_proj = validators.URL()
    frequencia = validators.String()
    rs_nome = validators.String()
    rs_link = validators.String()
    feed_nome = validators.String()
    feed_link = validators.String()

    # -- Comunicação e Cultura Digital
    sede_possui_tel = validators.String(not_empty=True)
    tipo_tel_sede = validators.String()
    pq_sem_tel = validators.String()
    pq_sem_tel_outro = validators.String()
    sede_possui_net = validators.String(not_empty=True)
    tipo_internet = validators.String()
    pq_sem_internet = validators.String()
    pq_sem_internet_outro = validators.String()

    # -- Entidade Proponente
    nome_ent = validators.String(not_empty=True)
    endereco_ent_proj = validators.String(not_empty=True)

    ent_tel = formencode.ForEach(BrazilPhoneNumber())
    email_ent = validators.Email()
    website_ent = validators.URL()
    convenio_ent = validators.String()
    outro_convenio = validators.String()
    participa_cultura_viva = validators.Bool()
    estabeleceu_parcerias = validators.Bool()

    # -- Atividades exercidas pelo projeto
    # -- Qual a área de atuação das atividades do projeto
    atividade = formencode.ForEach(validators.String(not_empty=True))

    # ---  Com qual Público Alvo o Projeto é desenvolvido?
    # ---- Sob aspectos de Faixa Etária
    publico_alvo = formencode.ForEach(validators.String(not_empty=True))

    # ---- Sob aspectos das Culturas Tradicionais
    culturas_tradicionais = formencode.ForEach(
        validators.String(not_empty=True))

    # ---- Sob aspectos de Ocupação do Meio
    ocupacao_do_meio = formencode.ForEach(validators.String(not_empty=True))

    # ---- Sob aspectos de Gênero
    genero = formencode.ForEach(validators.String(not_empty=True))

    # --- Quais são as Manifestações e Linguagens que o Projeto utiliza
    # em suas atividades?
    manifestacoes_linguagens = formencode.ForEach(
        validators.String(not_empty=True))

    # --- O Projeto participa de alguma Ação do Programa Cultura Viva?
    acao_cultura_viva = formencode.ForEach(validators.String(not_empty=True))

    descricao = validators.String()

    documentacoes = validators.FieldStorageUploadConverter()

    # -- Parcerias do Projeto
    parcerias = formencode.ForEach(validators.String(not_empty=True))

    # -- Índice de acesso à cultura
    ind_oficinas = validators.Int()
    ind_expectadores = validators.Int()
    ind_populacao = validators.Int()

    avatar = validators.FieldStorageUploadConverter()

    # TODO:
    #   Validar endereços adicionados em Outros Locais e Entidade OK!
    #   Validar CEPs OK!
    #   Validar Telefones OK!
    #   Validar conjunto de checkbox, onde pelo menos uma deve estar preenchida OK!
    #   Validar e-mails OK! -> já existe, validators.Email

