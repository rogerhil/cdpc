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

from formencode import ForEach, Schema
from formencode import validators

from ..utils.validators import Cpf, Cep, BrazilPhoneNumber, NotEmptyList, \
    CdpcEmail
from .models import Pessoa

################################################################################
# Usuario Validation


class Usuario(Schema):
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
    pessoa_tel = NotEmptyList(schema=ForEach(BrazilPhoneNumber()))
    pessoa_tel_tipo = ForEach(validators.String())
    avatar = validators.FieldStorageUploadConverter()

    # -- Sobre a sua geolocalização
    end_cep = Cep(not_empty=True)
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
    rs_nome = ForEach(validators.String())
    rs_link = ForEach(validators.URL())
    feed_nome = ForEach(validators.String())
    feed_link = ForEach(validators.URL())
    
    chained_validators = [
        validators.FieldsMatch('senha', 'confirmar_senha'),
        validators.RequireIfPresent('rs_nome', present='rs_link'),
        validators.RequireIfPresent('rs_link', present='rs_nome'),
        validators.RequireIfPresent('feed_nome', present='feed_link'),
        validators.RequireIfPresent('feed_link', present='feed_nome')
    ]

