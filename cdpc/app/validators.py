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
    # -- Sobre a sua participação
    voce_eh = validators.String(not_empty=True)
    nome_iniciativa = validators.String()
    papel = validators.String()

    # -- Dados pessoais
    nome = validators.String(not_empty=True)
    cpf = CpfValidator(not_empty=True)
    data_nascimento = validators.DateConverter(month_style='dd/mm/yyyy')
    sexo = validators.String(not_empty=True)
    avatar = validators.FieldStorageUploadConverter()

    # -- Sobre a sua geolocalização
    end_cep = validators.String(not_empty=True)
    end_numero = validators.String(not_empty=True)
    end_uf = validators.String(not_empty=True)
    end_cidade = validators.String(not_empty=True)
    end_bairro = validators.String(not_empty=True)
    end_logradouro = validators.String(not_empty=True)
    end_complemento = validators.String(not_empty=True)
    end_longitude = validators.String()
    end_latitude = validators.String()

    # -- Contatos e Espaços na rede
    telefone = validators.String(not_empty=True)
    email = validators.String(not_empty=True)
    website = validators.URL()
    rs_nome = validators.String()
    rs_link = validators.String()
    feed_nome = validators.String()
    feed_link = validators.String()

    # -- Dados de acesso
    usuario = validators.String(not_empty=True)
    senha = validators.String(not_empty=True)
    confirmar_senha = validators.String(not_empty=True)

    # TODO:
    #   Comparar senha original e confimada
    #   Checar dados condicionais

class Projeto(formencode.Schema):
    # -- Dados do projeto
    voce_eh = validators.String(not_empty=True)
    tipo_convenio = validators.String(not_empty=True)
    numero_convenio = validators.String(not_empty=True)
    nome_proj = validators.String(not_empty=True)

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
    tel_proj = validators.String()
    email_proj = validators.String(not_empty=True)
    website_proj = validators.URL()
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
    tel_ent = validators.String()
    email_ent = validators.String()
    website_ent = validators.URL()
    convenio_ent = validators.String()
    outro_ent = validators.String()

    # -- Atividades exercidas pelo projeto
    # -- Qual a área de atuação das atividades do projeto
    cultura_popular = validators.Bool()
    direitos_humanos = validators.Bool()
    economia_solidaria = validators.Bool()
    educacao = validators.Bool()
    esportes_e_lazer = validators.Bool()
    etnia = validators.Bool()
    genero = validators.Bool()
    habitacao = validators.Bool()
    meio_ambiente = validators.Bool()
    memoria = validators.Bool()
    patrimonio_historico_imaterial = \
        validators.Bool()
    patrimonio_historico_material = \
        validators.Bool()
    pesquisa_e_extensao = validators.Bool()
    povos_tradicionais = validators.Bool()
    recreacao = validators.Bool()
    religiao = validators.Bool()
    saude = validators.Bool()
    sexualidade = validators.Bool()
    tecnologia = validators.Bool()
    trabalho = validators.Bool()
    outras_atividades = validators.Bool()
    quais_outras_atividades = validators.String()

    # ---  Com qual Público Alvo o Projeto é desenvolvido?
    # ---- Sob aspectos de Faixa Etária
    criancas = validators.Bool()
    adolescentes = validators.Bool()
    adultos = validators.Bool()
    jovens = validators.Bool()

    # ---- Sob aspectos das Culturas Tradicionais
    quilombola = validators.Bool()
    pomerano = validators.Bool()
    caicara = validators.Bool()
    indigena = validators.Bool()
    cigana = validators.Bool()
    povos_da_floresta = validators.Bool()
    ribeirinhos = validators.Bool()
    outras_culturas = validators.Bool()
    quais_outras_culturas = validators.String()

    # ---- Sob aspectos de Ocupação do Meio
    rural = validators.Bool()
    urbano = validators.Bool()
    outro = validators.Bool()
    outra_ocupacao = validators.Bool()
    qual_outra_ocupacao = validators.String()

    # ---- Sob aspectos de Gênero
    mulheres = validators.Bool()
    homens = validators.Bool()
    lgbt = validators.Bool()

    # --- Quais são as Manifestações e Linguagens que o Projeto utiliza
    # em suas atividades?
    artes_digitais = validators.Bool()
    artes_plasticas = validators.Bool()
    audiovisual = validators.Bool()
    circo = validators.Bool()
    culinaria = validators.Bool()
    danca = validators.Bool()
    fotografia = validators.Bool()
    grafite = validators.Bool()
    internet = validators.Bool()
    jornalismo = validators.Bool()
    literatura = validators.Bool()
    musica = validators.Bool()
    radio = validators.Bool()
    teatro = validators.Bool()
    tecnologias_digitais = validators.Bool()
    tradicao_oral = validators.Bool()
    tv = validators.Bool()
    outras_manifestacoes = validators.Bool()
    quais_outras_manifestacoes = validators.String()

    # --- O Projeto participa de alguma Ação do Programa Cultura Viva?
    participa_cultura_viva = validators.String(not_empty=True)
    agente_cultura_viva = validators.Bool()
    cultura_digital = validators.Bool()
    cultura_e_saude = validators.Bool()
    economia_viva = validators.Bool()
    escola_viva = validators.Bool()
    grios = validators.Bool()
    interacoes_esteticas = validators.Bool()
    midias_livres = validators.Bool()
    pontinho_de_cultura = validators.Bool()
    pontos_de_memoria = validators.Bool()
    redes_indigenas = validators.Bool()
    tuxaua = validators.Bool()

    descricao = validators.String()

    documentacoes = validators.FieldStorageUploadConverter()

    # -- Parcerias do Projeto
    parcerias = validators.String(not_empty=True)
    parc_biblioteca = validators.Bool()
    parc_empresa = validators.Bool()
    parc_equipamento_de_saude = validators.Bool()
    parc_escola = validators.Bool()
    parc_igreja = validators.Bool()
    parc_ong = validators.Bool()
    parc_poder_publico = validators.Bool()
    parc_pontos_de_memoria = validators.Bool()
    parc_redes_indigenas = validators.Bool()
    parc_sistema_s = validators.Bool()
    parc_tuxaua = validators.Bool()
    outros_parceiros = validators.Bool()
    quais_outros_parceiros = validators.String()
    parc_nome = validators.String()

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
