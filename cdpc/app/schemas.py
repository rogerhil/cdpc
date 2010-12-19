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
from validators import Cpf, Cep, BrazilPhoneNumber, Dependent, \
                       AtLeastOne, NotEmptyList, CdpcEmail
from models import Pessoa, Projeto

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
        return super(CdpcSchema, self)._to_python(value_dict, state)


################################################################################
# Usuario Validation


class Usuario(formencode.Schema):
    # -- Dados de acesso
    senha = validators.String(not_empty=True)
    confirmar_senha = validators.String(not_empty=True)
    email = CdpcEmail(not_empty=True, model=Pessoa)
    # TODO: Comparar senha original e confimada

    # -- Dados pessoais
    nome = validators.String(not_empty=True)
    cpf = Cpf(not_empty=True)
    data_nascimento = validators.DateConverter(month_style='dd/mm/yyyy')
    sexo = validators.String(not_empty=True)
    pessoa_tel = NotEmptyList(schema=formencode.ForEach(BrazilPhoneNumber()))
    pessoa_tel_tipo = formencode.ForEach(validators.String())
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
    rs_nome = formencode.ForEach(validators.String())
    rs_link = formencode.ForEach(validators.URL())
    feed_nome = formencode.ForEach(validators.String())
    feed_link = formencode.ForEach(validators.URL())
    
    chained_validators = [validators.FieldsMatch('senha', 'confirmar_senha'),
                          validators.RequireIfPresent('rs_nome', present='rs_link'),
                          validators.RequireIfPresent('rs_link', present='rs_nome'),
                          validators.RequireIfPresent('feed_nome', present='feed_link'),
                          validators.RequireIfPresent('feed_link', present='feed_nome')]


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
    class DadosProjeto(CdpcSchema):
        nome = validators.String(not_empty=True)
        descricao = validators.String(not_empty=True)
        tipo = validators.String(not_empty=True)
        tipo_convenio = validators.String(not_empty=True)
        avatar = validators.FieldStorageUploadConverter()
        numero_convenio = validators.String(not_empty=True)

        participa_cultura_viva = validators.String(not_empty=True)
        acao_cultura_viva = Dependent(schema=AtLeastOne(schema=formencode.ForEach(validators.String())), depend_field=('participa_cultura_viva', 'sim'))
     
        estabeleceu_parcerias = validators.String(not_empty=True)
        parcerias = Dependent(schema=AtLeastOne(schema=formencode.ForEach(validators.String())), depend_field=('estabeleceu_parcerias', 'sim'))


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
        end_outro_nome = Dependent(schema=NotEmptyList(schema=formencode.ForEach(validators.String(not_empty=True))), depend_field=('local_proj', 'outros'))
        end_outro_cep = Dependent(schema=NotEmptyList(schema=formencode.ForEach(validators.String(not_empty=True))), depend_field=('local_proj', 'outros'))
        end_outro_numero = Dependent(schema=NotEmptyList(schema=formencode.ForEach(validators.String(not_empty=True))), depend_field=('local_proj', 'outros'))
        end_outro_logradouro = Dependent(schema=NotEmptyList(schema=formencode.ForEach(validators.String(not_empty=True))), depend_field=('local_proj', 'outros'))
        end_outro_complemento = Dependent(schema=formencode.ForEach(validators.String()), depend_field=('local_proj', 'outros'))
        end_outro_uf = Dependent(schema=NotEmptyList(schema=formencode.ForEach(validators.String(not_empty=True))), depend_field=('local_proj', 'outros'))
        end_outro_cidade = Dependent(schema=NotEmptyList(schema=formencode.ForEach(validators.String(not_empty=True))), depend_field=('local_proj', 'outros'))
        end_outro_bairro = Dependent(schema=NotEmptyList(schema=formencode.ForEach(validators.String(not_empty=True))), depend_field=('local_proj', 'outros'))
        end_outro_latitude = Dependent(schema=formencode.ForEach(validators.String()), depend_field=('local_proj', 'outros'))
        end_outro_longitude = Dependent(schema=formencode.ForEach(validators.String()), depend_field=('local_proj', 'outros'))


    class EntidadeProponente(CdpcSchema):
        nome_ent = validators.String(not_empty=True)
        email_ent = validators.Email()
        website_ent = validators.URL()
        ent_tel = formencode.ForEach(BrazilPhoneNumber())
        ent_tel_tipo = formencode.ForEach(validators.String())

        convenio_ent = validators.String(not_empty=True)
        outro_convenio = Dependent(schema=formencode.ForEach(validators.String(not_empty=True)), depend_field=('convenio_ent', 'sim'))

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


    class ComunicacaoCulturaDigital(CdpcSchema):
        email_proj = CdpcEmail(not_empty=True, model=Projeto)
        website_proj = validators.URL()
        
        sede_possui_tel = validators.String(not_empty=True)
        sede_tel_tipo = Dependent(schema=formencode.ForEach(validators.String()), depend_field=('sede_possui_tel', 'sim'))
        sede_tel = Dependent(schema=NotEmptyList(schema=formencode.ForEach(BrazilPhoneNumber(not_empty=True))), depend_field=('sede_possui_tel', 'sim'))
        pq_sem_tel = Dependent(schema=validators.String(not_empty=True), depend_field=('sede_possui_tel', 'nao'))
        pq_sem_tel_outro = Dependent(schema=validators.String(not_empty=True), depend_field=('pq_sem_tel', 'outro'))
        sede_possui_net = validators.String(not_empty=True)
        tipo_internet =  Dependent(schema=validators.String(not_empty=True), depend_field=('sede_possui_net', 'sim'))
        pq_sem_internet =  Dependent(schema=validators.String(not_empty=True), depend_field=('sede_possui_net', 'nao'))
        pq_sem_internet_outro =  Dependent(schema=validators.String(not_empty=True), depend_field=('pq_sem_internet', 'outro'))

        rs_nome = formencode.ForEach(validators.String())
        rs_link = formencode.ForEach(validators.URL())
        feed_nome = formencode.ForEach(validators.String())
        feed_link = formencode.ForEach(validators.URL())

        chained_validators = [validators.RequireIfPresent('rs_nome', present='rs_link'),
                              validators.RequireIfPresent('rs_link', present='rs_nome'),
                              validators.RequireIfPresent('feed_nome', present='feed_link'),
                              validators.RequireIfPresent('feed_link', present='feed_nome')]

    class AtividadesExercidasProjeto(CdpcSchema):
        atividade = AtLeastOne(schema=formencode.ForEach(validators.String(not_empty=True)))


    class Publico(CdpcSchema):
        # ---  Com qual Público Alvo o Projeto é desenvolvido?
        # ---- Sob aspectos de Faixa Etária
        publico_alvo = formencode.ForEach(validators.String(not_empty=True))

        # ---- Sob aspectos das Culturas Tradicionais
        culturas_tradicionais = formencode.ForEach(validators.String(not_empty=True))

        # ---- Sob aspectos de Ocupação do Meio
        ocupacao_do_meio = formencode.ForEach(validators.String(not_empty=True))

        # ---- Sob aspectos de Gênero
        genero = formencode.ForEach(validators.String(not_empty=True))

        # --- Quais são as Manifestações e Linguagens que o Projeto utiliza
        # em suas atividades?
        manifestacoes_linguagens = formencode.ForEach(validators.String(not_empty=True))

        documentacoes = formencode.ForEach(validators.FieldStorageUploadConverter())

    class IndiceAcessoCultura(formencode.Schema):
        # -- Índice de acesso à cultura
        ind_oficinas = validators.Int()
        ind_expectadores = validators.Int()
        ind_populacao = validators.Int()


    #class ParceriasProjeto(CdpcSchema):
    #    estabeleceu_parcerias = validators.String(not_empty=True)
    #    parcerias = Dependent(schema=AtLeastOne(schema=formencode.ForEach(validators.String())), depend_field=('estabeleceu_parcerias', 'sim'))

    #class Avatar(formencode.Schema):
    #    avatar = validators.FieldStorageUploadConverter()


    # CAMPOS EXCLUIDOS!!!!!!!
    #class ContatosEspacoRede(CdpcSchema):
    #    proj_tel = formencode.ForEach(BrazilPhoneNumber(not_empty=True))
    #    email_proj = validators.Email(not_empty=True)
    #    website_proj = validators.URL()
    #    frequencia = validators.String()

