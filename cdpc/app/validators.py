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

import formencode, re
from formencode import validators
from formencode.validators import _, Invalid

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

class BrazilPhoneNumber(formencode.FancyValidator):

    """
    Validates, and converts phone numbers to ##-########
    Adapted from formencode.validators.national.InternationPhoneNumber

    ::

        >>> valid = BrazilPhoneNumber()
        >>> valid.to_python("(31) 12345678")
        '31-'
        >>> valid.to_python("(31) 1234 5678")
        '31-12345678'
        >>> valid.to_python("(31) 1234-5678")
        '31-12345678'
        >>> valid.to_python("(31) 1234.5678")
        '31-12345678'
        >>> valid.to_python("(31)-1234.5678")
        '31-12345678'
        >>> valid.to_python("(31).1234.5678")
        '31-12345678'
        >>> valid.to_python(" ( 31 ) . 1234 . 5678 ")
        '31-12345678'
        >>> valid.to_python(" 31  - 1234 . 5678 ")
        '31-12345678'
        >>> valid.to_python("3112345678")
        '31-12345678'
        >>> valid.to_python("31-1234.5678a")
            ...
        formencode.api.Invalid: Please enter a number, with area code, in the form (##)########.
        >>> valid.to_python("31-12349.5678")
            ...
        formencode.api.Invalid: Please enter a number, with area code, in the form (##)########.

    """

    strip = True
    _br_phone_re = [re.compile(r"^\s*\(\s*(\d{2})\s*\)[\s\.\-/_|]*(\d{4})[\s\.\-/_|]*(\d{4})\s*$"),
                   re.compile(r"^\s*(\d{2})[\s\.\-/_|]*(\d{4})[\s\.\-/_|]*(\d{4})\s*$")]
    _store_format = "%s-%s%s"
    messages = {
        'phoneFormat': _('Please enter a number, with area code, in the form (##)########.'),
        }


    def _to_python(self, value, state):
        self.assert_string(value, state)
        try:
            value = value.encode('ascii', 'replace')
        except:
            raise Invalid(self.message('phoneFormat', state), value, state)
        clean_value = value.strip().replace(' ', '')
        for regexp in self._br_phone_re:
            match = regexp.match(clean_value)
            if match:
                return self._store_format % match.groups()
        raise Invalid(self.message('phoneFormat', state), value, state)


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

class Projeto(formencode.Schema):
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
    tel_proj = formencode.ForEach(BrazilPhoneNumber())
    email_proj = validators.String(not_empty=True)
    website_proj = validators.URL(not_empty=True)
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
    end_ent_cep = validators.String()
    end_ent_numero = validators.String()
    end_ent_logradouro = validators.String()
    end_ent_complemento = validators.String()
    end_ent_uf = validators.String()
    end_ent_cidade = validators.String()
    end_ent_bairro = validators.String()
    end_ent_latitude = validators.String()
    end_ent_longitude = validators.String()
    tel_ent = BrazilPhoneNumber()
    email_ent = validators.String()
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
    #   Validar endereços adicionados em Outros Locais e Entidade
    #   Validar CEPs
    #   Validar Telefones
    #   Validar conjunto de checkbox, onde pelo menos uma deve estar preenchida
    #   Validar e-mails
