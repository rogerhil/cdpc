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

from formencode import Schema, ForEach
from formencode import validators

from .models import Projeto
from ..utils.schemas import CdpcSchema
from ..utils.validators import Cpf, Cep, BrazilPhoneNumber, Dependent, \
    AtLeastOne, NotEmptyList, CdpcEmail

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
        acao_cultura_viva = Dependent(schema=AtLeastOne(schema=ForEach(validators.String())), depend_field=('participa_cultura_viva', 'sim'))
     
        estabeleceu_parcerias = validators.String(not_empty=True)
        parcerias = Dependent(schema=AtLeastOne(schema=ForEach(validators.String())), depend_field=('estabeleceu_parcerias', 'sim'))
        outro_parceiro = ForEach(validators.String())


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
        end_outro_nome = Dependent(schema=NotEmptyList(schema=ForEach(validators.String(not_empty=True))), depend_field=('local_proj', 'outros'))
        end_outro_cep = Dependent(schema=NotEmptyList(schema=ForEach(Cep(not_empty=True))), depend_field=('local_proj', 'outros'))
        end_outro_numero = Dependent(schema=NotEmptyList(schema=ForEach(validators.String(not_empty=True))), depend_field=('local_proj', 'outros'))
        end_outro_logradouro = Dependent(schema=NotEmptyList(schema=ForEach(validators.String(not_empty=True))), depend_field=('local_proj', 'outros'))
        end_outro_complemento = Dependent(schema=ForEach(validators.String()), depend_field=('local_proj', 'outros'))
        end_outro_uf = Dependent(schema=NotEmptyList(schema=ForEach(validators.String(not_empty=True))), depend_field=('local_proj', 'outros'))
        end_outro_cidade = Dependent(schema=NotEmptyList(schema=ForEach(validators.String(not_empty=True))), depend_field=('local_proj', 'outros'))
        end_outro_bairro = Dependent(schema=NotEmptyList(schema=ForEach(validators.String(not_empty=True))), depend_field=('local_proj', 'outros'))
        end_outro_latitude = Dependent(schema=ForEach(validators.String()), depend_field=('local_proj', 'outros'))
        end_outro_longitude = Dependent(schema=ForEach(validators.String()), depend_field=('local_proj', 'outros'))


    class EntidadeProponente(CdpcSchema):
        nome_ent = validators.String(not_empty=True)
        email_ent = validators.Email()
        website_ent = validators.URL()
        ent_tel = ForEach(BrazilPhoneNumber())
        ent_tel_tipo = ForEach(validators.String())

        convenio_ent = validators.String(not_empty=True)
        outro_convenio = Dependent(schema=ForEach(validators.String(not_empty=True)), depend_field=('convenio_ent', 'sim'))

        endereco_ent_proj = validators.String(not_empty=True)
        end_ent_cep = Dependent(schema=Cep(not_empty=True), depend_field=('endereco_ent_proj', 'nao'))
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
        sede_tel_tipo = Dependent(schema=ForEach(validators.String()), depend_field=('sede_possui_tel', 'sim'))
        sede_tel = Dependent(schema=NotEmptyList(schema=ForEach(BrazilPhoneNumber(not_empty=True))), depend_field=('sede_possui_tel', 'sim'))
        pq_sem_tel = Dependent(schema=validators.String(not_empty=True), depend_field=('sede_possui_tel', 'nao'))
        pq_sem_tel_outro = Dependent(schema=validators.String(not_empty=True), depend_field=('pq_sem_tel', 'outro'))
        sede_possui_net = validators.String(not_empty=True)
        tipo_internet =  Dependent(schema=validators.String(not_empty=True), depend_field=('sede_possui_net', 'sim'))
        pq_sem_internet =  Dependent(schema=validators.String(not_empty=True), depend_field=('sede_possui_net', 'nao'))
        pq_sem_internet_outro =  Dependent(schema=validators.String(not_empty=True), depend_field=('pq_sem_internet', 'outro'))

        rs_nome = ForEach(validators.String())
        rs_link = ForEach(validators.URL())
        feed_nome = ForEach(validators.String())
        feed_link = ForEach(validators.URL())

        chained_validators = [validators.RequireIfPresent('rs_nome', present='rs_link'),
                              validators.RequireIfPresent('rs_link', present='rs_nome'),
                              validators.RequireIfPresent('feed_nome', present='feed_link'),
                              validators.RequireIfPresent('feed_link', present='feed_nome')]

    class AtividadesExercidasProjeto(CdpcSchema):
        atividade = AtLeastOne(schema=ForEach(validators.String(not_empty=True)))


    class Publico(CdpcSchema):
        # ---  Com qual Público Alvo o Projeto é desenvolvido?
        # ---- Sob aspectos de Faixa Etária
        publico_alvo = ForEach(validators.String(not_empty=True))

        # ---- Sob aspectos das Culturas Tradicionais
        culturas_tradicionais = ForEach(validators.String(not_empty=True))

        # ---- Sob aspectos de Ocupação do Meio
        ocupacao_do_meio = ForEach(validators.String(not_empty=True))

        # ---- Sob aspectos de Gênero
        genero = ForEach(validators.String(not_empty=True))

        # --- Quais são as Manifestações e Linguagens que o Projeto utiliza
        # em suas atividades?
        manifestacoes_linguagens = ForEach(validators.String(not_empty=True))

        documentacoes = ForEach(validators.FieldStorageUploadConverter())

    class IndiceAcessoCultura(Schema):
        # -- Índice de acesso à cultura
        ind_oficinas = validators.Int()
        ind_expectadores = validators.Int()
        ind_populacao = validators.Int()


    #class ParceriasProjeto(CdpcSchema):
    #    estabeleceu_parcerias = validators.String(not_empty=True)
    #    parcerias = Dependent(schema=AtLeastOne(schema=ForEach(validators.String())), depend_field=('estabeleceu_parcerias', 'sim'))

    #class Avatar(formencode.Schema):
    #    avatar = validators.FieldStorageUploadConverter()


    # CAMPOS EXCLUIDOS!!!!!!!
    #class ContatosEspacoRede(CdpcSchema):
    #    proj_tel = ForEach(BrazilPhoneNumber(not_empty=True))
    #    email_proj = validators.Email(not_empty=True)
    #    website_proj = validators.URL()
    #    frequencia = validators.String()

