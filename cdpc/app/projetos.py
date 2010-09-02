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

from formencode import Invalid
from flask import Module, render_template, request

from . import validators
from . import models
from cadastro import VALORES_UF

module = Module(__name__)

@module.route("novo/", methods=('GET', 'POST'))
def novo():
    """
    """
    if request.method == 'POST':
        # instanciando o validador
        validator = validators.Projeto()
        validado = {}
        print 'POST'
        try:
            validado = validator.to_python(request.form)

            rs_nomes = clean_list(request.form.getlist('rs_nome'))
            rs_links = clean_list(request.form.getlist('rs_link'))
            assert len(rs_nomes) == len(rs_links)

            feed_nomes = clean_list(request.form.getlist('feed_nome'))
            feed_links = clean_list(request.form.getlist('feed_link'))
            assert len(feed_nomes) == len(feed_links)

        except Invalid, e:
            # Dar um feedback pro usuário usando a instância da
            # exceção "e".
            print 'Exceção'
            print e
            pass
        else:
            print 'ELSE'
            # Instanciando o modelo e associando os campos validados e
            # transformados em valores python à instância que será
            # salva no db.
            projeto = models.Projeto()

            # -- Dados do projeto
            projeto.voce_eh = validado['voce_eh']
            projeto.tipo_convenio = validado['tipo_convenio']
            projeto.numero_convenio = validado['numero_convenio']
            projeto.nome_proj = validado['nome_proj']

            # -- Localização geográfica do projeto
            projeto.end_proj = [models.Endereco(
                    cep=validado['end_proj_cep'],
                    numero=validado['end_proj_numero'],
                    logradouro=validado['end_proj_logradouro'],
                    complemento=validado['end_proj_complemento'],
                    uf=validado['end_proj_uf'],
                    cidade=validado['end_proj_cidade'],
                    bairro=validado['end_proj_bairro'],
                    latitude=validado['end_proj_latitude'],
                    longitude=validado['end_proj_longitude']
                    )]
            projeto.local_proj = validado['local_proj']
            if(projeto.local_proj == 'outros'):
                projeto.end_outros = [models.Endereco(
                        nome=validado['end_outro_nome'],
                        cep=validado['end_outro_cep'],
                        numero=validado['end_outro_numero'],
                        logradouro=validado['end_outro_logradouro'],
                        complemento=validado['end_outro_complemento'],
                        uf=validado['end_outro_uf'],
                        cidade=validado['end_outro_cidade'],
                        bairro=validado['end_outro_bairro'],
                        latitude=validado['end_outro_latitude'],
                        longitude=validado['end_outro_longitude']
                        )]

            # -- Contatos e espaços na rede
            projeto.email = validado['email_proj']
            projeto.website = validado['website_proj']
            projeto.frequencia = validado['frequencia']
            for i in request.form.getlist('tel_proj'):
                tel = models.Telefone()
                tel.numero = i
                projeto.telefones.append(tel)

            for i in range(len(rs_nomes)):
                rsocial = models.RedeSocial()
                rsocial.nome = rs_nomes[i]
                rsocial.link = rs_links[i]
                projeto.redes_sociais.append(rsocial)

            for i in range(len(feed_nomes)):
                feed = models.Feed()
                feed.nome = feed_nomes[i]
                feed.link = feed_links[i]
                projeto.feeds.append(feed)

            # -- Comunicação e Cultura Digital
            projeto.sede_possui_tel = validado['sede_possui_tel'] == 'sim'
            if(projeto.sede_possui_tel):
                projeto.tipo_tel_sede = validado['tipo_tel_sede']
            else:
                projeto.pq_sem_tel = validado['pq_sem_tel']
                if(projeto.pq_sem_tel == 'outro'):
                    projeto.pq_sem_tel_outro = validado['pq_sem_tel_outro']
            projeto.sede_possui_net = validado['sede_possui_net']
            if(projeto.sede_possui_net):
                projeto.tipo_internet = validado['tipo_internet']
            else:
                projeto.pq_sem_internet = validado['pq_sem_internet']
                if(projeto.pq_sem_internet == 'outro'):
                    projeto.pq_sem_internet_outro = \
                        validado['pq_sem_internet_outro']

            # -- Entidade Proponente
            projeto.nome_ent = validado['nome_ent']
            projeto.endereco_ent_proj = validado['endereco_ent_proj'] == 'sim'
            if(not projeto.endereco_ent_proj):
                projeto.end_ent= [models.Endereco(
                        cep=validado['end_ent_cep'],
                        numero=validado['end_ent_numero'],
                        logradouro=validado['end_ent_logradouro'],
                        complemento=validado['end_ent_complemento'],
                        uf=validado['end_ent_uf'],
                        cidade=validado['end_ent_cidade'],
                        bairro=validado['end_ent_bairro'],
                        latitude=validado['end_ent_latitude'],
                        longitude=validado['end_ent_longitude']
                        )]
            projeto.tel_ent = [models.Telefone(numero=validado['tel_ent'])]
            projeto.email_ent = validado['email_ent']
            projeto.website_ent = validado['website_ent']
            projeto.convenio_ent = validado['convenio_ent'] == 'sim'

            if(projeto.convenio_ent):
                for i in request.form.getlist('outro_convenio'):
                    conv = models.Convenio()
                    tel.nome = i
                    projeto.outro_convenio.append(conv)

            # -- Atividades exercidas pelo projeto
            # --- Qual a área de atuação das atividades do Projeto?
            projeto.cultura_popular = validado['cultura_popular']
            projeto.direitos_humanos = validado['direitos_humanos']
            projeto.economia_solidaria = validado['economia_solidaria']
            projeto.educacao = validado['educacao']
            projeto.esportes_e_lazer = validado['esportes_e_lazer']
            projeto.etnia = validado['etnia']
            projeto.genero = validado['genero']
            projeto.habitacao = validado['habitacao']
            projeto.meio_ambiente = validado['meio_ambiente']
            projeto.memoria = validado['memoria']
            projeto.patrimonio_historico_imaterial = \
                validado['patrimonio_historico_imaterial']
            projeto.patrimonio_historico_material = \
                validado['patrimonio_historico_material']
            projeto.pesquisa_e_extensao = validado['pesquisa_e_extensao']
            projeto.povos_tradicionais = validado['povos_tradicionais']
            projeto.recreacao = validado['recreacao']
            projeto.religiao = validado['religiao']
            projeto.saude = validado['saude']
            projeto.sexualidade = validado['sexualidade']
            projeto.tecnologia = validado['tecnologia']
            projeto.trabalho = validado['trabalho']
            projeto.outras_atividades = validado['outras_atividades']
            if(projeto.outras_atividades):
                projeto.quais_outras_atividades = \
                    validado['quais_outras_atividades']

            # ---  Com qual Público Alvo o Projeto é desenvolvido?
            # ---- Sob aspectos de Faixa Etária
            projeto.criancas = validado['criancas']
            projeto.adolescentes = validado['adolescentes']
            projeto.adultos = validado['adultos']
            projeto.jovens = validado['jovens']

            # ---- Sob aspectos das Culturas Tradicionais
            projeto.quilombola = validado['quilombola']
            projeto.pomerano = validado['pomerano']
            projeto.caicara = validado['caicara']
            projeto.indigena = validado['indigena']
            projeto.cigana = validado['cigana']
            projeto.povos_da_floresta = validado['povos_da_floresta']
            projeto.ribeirinhos = validado['ribeirinhos']
            projeto.outras_culturas = validado['outras_culturas']
            if(projeto.outras_culturas):
                projeto.quais_outras_culturas = \
                    validado['quais_outras_culturas']

            # ---- Sob aspectos de Ocupação do Meio
            projeto.rural = validado['rural']
            projeto.urbano = validado['urbano']
            projeto.outro = validado['outro']
            projeto.outra_ocupacao = validado['outra_ocupacao']
            if(projeto.outra_ocupacao):
                projeto.qual_outra_ocupacao = validado['qual_outra_ocupacao']

            # ---- Sob aspectos de Gênero
            projeto.mulheres = validado['mulheres']
            projeto.homens = validado['homens']
            projeto.lgbt = validado['lgbt']

            # --- Quais são as Manifestações e Linguagens que o Projeto utiliza
            # em suas atividades?
            projeto.artes_digitais = validado['artes_digitais']
            projeto.artes_plasticas = validado['artes_plasticas']
            projeto.audiovisual = validado['audiovisual']
            projeto.circo = validado['circo']
            projeto.culinaria = validado['culinaria']
            projeto.danca = validado['danca']
            projeto.fotografia = validado['fotografia']
            projeto.grafite = validado['grafite']
            projeto.internet = validado['internet']
            projeto.jornalismo = validado['jornalismo']
            projeto.literatura = validado['literatura']
            projeto.musica = validado['musica']
            projeto.radio = validado['radio']
            projeto.teatro = validado['teatro']
            projeto.tecnologias_digitais = validado['tecnologias_digitais']
            projeto.tradicao_oral = validado['tradicao_oral']
            projeto.tv = validado['tv']
            projeto.outras_manifestacoes = validado['outras_manifestacoes']
            if(projeto.outras_manifestacoes):
                projeto.quais_outras_manifestacoes = \
                    validado['quais_outras_manifestacoes']

            # --- O Projeto participa de alguma Ação do Programa Cultura Viva?
            projeto.participa_cultura_viva = validado['participa_cultura_viva']
            projeto.agente_cultura_viva = validado['agente_cultura_viva']
            projeto.cultura_digital = validado['cultura_digital']
            projeto.cultura_e_saude = validado['cultura_e_saude']
            projeto.economia_viva = validado['economia_viva']
            projeto.escola_viva = validado['escola_viva']
            projeto.grios = validado['grios']
            projeto.interacoes_esteticas = validado['interacoes_esteticas']
            projeto.midias_livres = validado['midias_livres']
            projeto.pontinho_de_cultura = validado['pontinho_de_cultura']
            projeto.pontos_de_memoria = validado['pontos_de_memoria']
            projeto.redes_indigenas = validado['redes_indigenas']
            projeto.tuxaua = validado['tuxaua']

            descricao = validado['descricao']

            # TODO: Tratar upload de documentacoes

            # -- Parcerias do Projeto
            projeto.parcerias = validado['parcerias']
            projeto.parc_biblioteca = validado['parc_biblioteca']
            projeto.parc_empresa = validado['parc_empresa']
            projeto.parc_equipamento_de_saude = validado['parc_equipamento_de_saude']
            projeto.parc_escola = validado['parc_escola']
            projeto.parc_igreja = validado['parc_igreja']
            projeto.parc_ong = validado['parc_ong']
            projeto.parc_poder_publico = validado['parc_poder_publico']
            projeto.parc_pontos_de_memoria = validado['parc_pontos_de_memoria']
            projeto.parc_redes_indigenas = validado['parc_redes_indigenas']
            projeto.parc_sistema_s = validado['parc_sistema_s']
            projeto.parc_tuxaua = validado['parc_tuxaua']
            projeto.outros_parceiros = validado['outros_parceiros']
            if(projeto.outros_parceiros):
                projeto.quais_outros_parceiros = validado['quais_outros_parceiros']

            for i in request.form.getlist('parc_nome'):
                parc = models.Parceiro()
                parc.nome = i
                projeto.outro_convenio.append(parc)

            # -- Índice de acesso à cultura
            projeto.ind_oficinas = validado['ind_oficinas']
            ind_expectadores = validado['ind_expectadores']
            ind_populacao = validado['ind_populacao']

            # -- Avatar
            # TODO: Tratar upload de avatar

            session.commit()

            # FIXME: Avisar ao usuário que tudo deu certo.

    return render_template(
        'projetos/novo.html',
        vals_uf=VALORES_UF)
