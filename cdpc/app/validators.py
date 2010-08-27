# -*- coding: utf-8; Mode: Python -*-
#
# Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
# Copyright (C) 2010  Ministério da Cultura <http://cultura.gov.br>
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

import formencode
from formencode import validators

class CpfValidator(formencode.FancyValidator):
    def _to_python(self, value, state):
        # Tratando o tamanho mínimo do cpf
        if len(value) != 11:
            raise formencode.Invalid(u'Cpf inválido', value, state)

        # tratando os valores óbvios
        if value in [str(i) * 11 for i in range(10)]:
            raise formencode.Invalid(u'Cpf inválido', value, state)

        # transformando o cpf num int
        cpf = map(int, value)

        # gerando os dois últimos dígitos do cpf
        newval = cpf[:9]
        while len(newval) < 11:
            new_item =  \
                [(len(newval)+1-x)*y for x, y in enumerate(newval)]
            result = sum(new_item) % 11
            if result > 1:
                newval.append(11 - result)
            else:
                newval.append(0)

        # Comparando o cpf informado pelo usuário com o gerado pela
        # bagunça acima
        if newval != cpf:
            raise formencode.Invalid(u'Cpf inválido', value, state)
        return value

class Usuario(formencode.Schema):
    voce_eh = validators.String(not_empty=True)
    nome = validators.String(not_empty=True)
    cpf = CpfValidator(not_empty=True)
    data_nascimento = validators.String(not_empty=True)
    sexo = validators.String(not_empty=True)
    end_cep = validators.String(not_empty=True)
    end_numero = validators.String(not_empty=True)
    end_uf = validators.String(not_empty=True)
    end_cidade = validators.String(not_empty=True)
    end_bairro = validators.String(not_empty=True)
    telefone = validatores.String(not_empty=True)
    email = validators.String(not_empty=True)
    usuario = validators.String(not_empty=True)
    senha = validators.String(not_empty=True)
    confirmar_senha = validators.String(not_empty=True)

    # TODO:
    #   Comparar senha original e confimada
    #   Checar dados condicionais

class Projeto(formencode.Schema):
    voce_eh = validators.String(not_empty=True)
    tipo_convenio = validators.String(not_empty=True)
    numero_convenio = validators.String(not_empty=True)
    nome_proj = validators.String(not_empty=True)
    end_proj_cep = validators.String(not_empty=True)
    end_proj_numero = validators.String(not_empty=True)
    end_proj_uf = validators.String(not_empty=True)
    end_proj_cidade = validators.String(not_empty=True)
    end_proj_bairro = validators.String(not_empty=True)
    local_proj = validators.String(not_empty=True)
    tel_proj = validators.String(not_empty=True)
    email = validators.String(not_empty=True)
    sede_possui_tel = validators.String(not_empty=True)
    sede_possui_net = validators.String(not_empty=True)
    nome_ent = validators.String(not_empty=True)
    endereco_ent_proj = validators.String(not_empty=True)
    participa_cultura_viva = validators.String(not_empty=True)
    parcerias = validators.String(not_empty=True)

    # TODO:
    #   Validar endereços adicionados em Outros Locais e Entidade
    #   Validar CEPs
    #   Validar Telefones
    #   Validar conjunto de checkbox, onde pelo menos uma deve estar preenchida
    #   Validar e-mails
    #   Validar websites
    #   Validar que os índices são inteiros
