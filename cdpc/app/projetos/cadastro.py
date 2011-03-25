# -*- coding: utf-8; Mode: Python -*-
#
# Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
# Copyright (C) 2010  Rogerio Hilbert Lima <rogerhi@gmail.com>
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

from elixir import session
from urllib import urlopen
from simplejson import dumps, loads
from flask import Module, request
from formencode import foreach

from ..common import models as common_models
from ..utils.filestorage import save_image, save_file, remove_file
from ..utils.model import get_or_create
from ..utils.schemas import CdpcSchema

from . import models
from . import schemas as schemas_proj
from cdpc.app.common.cadastro import *


TIPO = format(
    [u'Ponto',
     u'Pontão',
     u'Iniciativa Premiada'])

TIPO_CONVENIO = format(
    [u'Internacional',
     u'Federal',
     u'Estadual',
     u'Municipal'])

ACAO_CULTURA_VIVA = format(
    [u'Agente Cultura Viva',
     u'Cultura Digital',
     u'Cultura e Saúde',
     u'Economia Viva',
     u'Escola Viva',
     u'Grios',
     u'Interações Estéticas',
     u'Mídias Livres',
     u'Pontinho de Cultura',
     u'Pontos de memória',
     u'Redes Indígenas',
     u'Tuxaua'])

PARCERIAS = format(
    [u'Biblioteca',
     u'Empresa',
     u'Equipamento de Saúde',
     u'Escola',
     u'Igreja',
     u'ONG',
     u'Poder público',
     u'Pontos de Memória',
     u'Redes Indígenas',
     u'Sistemas S (Sesc, Senai, etc)',
     u'Tuxaua',
     u'Outros'])

LOCAL_PROJ = format(
    [u'Sede',
     u'Itinerante',
     u'Outros locais'])

PQ_SEM_TEL = format(
    [u'Opção',
     u'Não há fornecimento de serviços na região',
     u'Falta de recursos',
     u'Outros'])

PQ_SEM_INTERNET = PQ_SEM_TEL

TIPO_INTERNET = format(
    [u'Discada',
     u'3G',
     u'ADSL/Cabo (Banda Larga)',
     u'Rádio',
     u'Gesac',
     u'Internet Pública'])

ATIVIDADE = format(
    [u'Cultura Popular',
     u'Direitos Humanos',
     u'Economia Solidária',
     u'Educação',
     u'Esportes e Lazer',
     u'Etnia',
     u'Gênero',
     u'Habitação',
     u'Meio ambiente',
     u'Memória',
     u'Patrimônio Histórico Imaterial',
     u'Patrimônio Histórico Material',
     u'Pesquisa e Extensão',
     u'Povos e comunidades tradicionais',
     u'Recreação',
     u'Religião',
     u'Saúde',
     u'Sexualidade',
     u'Tecnologia',
     u'Trabalho'])

PUBLICO_ALVO = format(
    [u'Crianças',
     u'Adolescentes',
     u'Adultos',
     u'Jovens'])
                
CULTURAS_TRADICIONAIS = format(
    [u'Quilombola',
     u'Pomerano',
     u'Caiçara',
     u'Indígena',
     u'Cigana',
     u'Ribeirinhos',
     u'Povos da Floresta'])


OCUPACAO_DO_MEIO = format(
    [u'Rural',
     u'Urbano'])

GENERO = format(
    [u'Mulheres',
     u'Homens',
     u'LGBT'])

MANIFESTACOES_LINGUAGENS = format(
    [u'Artes digitais',
     u'Artes plásticas',
     u'Audiovisual',
     u'Circo',
     u'Culinária',
     u'Dança',
     u'Fotografia',
     u'Grafite',
     u'Internet',
     u'Jornalismo',
     u'Literatura',
     u'Música',
     u'Rádio',
     u'Teatro',
     u'Tecnologias digitais',
     u'Tradição oral',
     u'TV',
     u'Outras'])


def set_values_projeto(projeto, validado, user):
    blank = lambda x: None if not x.strip() else x.strip()

    # -- Dados do projeto
    projeto.nome = validado['nome']
    if validado['tipo'] == 'outro':
        projeto.tipo = validado['tipo_outro']
    else:    
        projeto.tipo = validado['tipo']
    projeto.tipo_convenio = validado['tipo_convenio']
    projeto.numero_convenio = validado['numero_convenio']
    
    # -- Localização geográfica do projeto
    endsede = get_or_create(common_models.Endereco, 
        cep=validado['end_proj_cep'],
        numero=validado['end_proj_numero'],
        logradouro=validado['end_proj_logradouro'],
        complemento=blank(validado['end_proj_complemento']),
        uf=validado['end_proj_uf'],
        cidade=validado['end_proj_cidade'],
        bairro=validado['end_proj_bairro'],
        latitude=blank(validado['end_proj_latitude']),
        longitude=blank(validado['end_proj_longitude']))[0]

    projeto.endereco_sede = endsede

    projeto.local = validado['local_proj']

    projeto.enderecos = []

    if projeto.local == 'outros':
        for i in range(len(validado['end_outro_nome'])):
            endereco = get_or_create(common_models.Endereco,
                nome=validado['end_outro_nome'][i],
                cep=validado['end_outro_cep'][i],
                numero=validado['end_outro_numero'][i],
                logradouro=validado['end_outro_logradouro'][i],
                complemento=blank(validado['end_outro_complemento'][i]),
                uf=validado['end_outro_uf'][i],
                cidade=validado['end_outro_cidade'][i],
                bairro=validado['end_outro_bairro'][i],
                latitude=blank(validado['end_outro_latitude'][i]),
                longitude=blank(validado['end_outro_longitude'][i]))[0]
            projeto.enderecos.append(endereco)

    # -- Contatos e espaços na rede

    ######################
    # CAMPOS EXCLUÍDOS!!!
    #projeto.frequencia = validado['frequencia']   
    ######################

    projeto.redes_sociais = []

    for i in range(len(validado['rs_nome'])):
        rsocial = get_or_create(common_models.RedeSocial,
                                nome=validado['rs_nome'][i],
                                link=validado['rs_link'][i])[0]
        projeto.redes_sociais.append(rsocial)

    projeto.feeds = []

    for i in range(len(validado['feed_nome'])):
        feed = get_or_create(common_models.Feed,
                             nome = validado['feed_nome'][i],
                             link = validado['feed_link'][i])[0]
        projeto.feeds.append(feed)

    # -- Comunicação e Cultura Digital
    
    projeto.email = validado['email_proj']
    projeto.website = validado['website_proj']

    def get_tel(numero, tipo):
        tel = get_or_create(common_models.Telefone, numero=numero, tipo=tipo)[0]
        return tel

    projeto.sede_possui_tel = validado['sede_possui_tel'] == 'sim'
    if projeto.sede_possui_tel:
        for i, t in enumerate(validado['sede_tel']):
            tel = get_tel(t, validado['sede_tel_tipo'][i])
            projeto.telefones.append(tel)
    else:
        projeto.pq_sem_tel = validado['pq_sem_tel']
        if projeto.pq_sem_tel == 'outro':
            projeto.pq_sem_tel = validado['pq_sem_tel_outro']
    projeto.sede_possui_net = validado['sede_possui_net'] == 'sim'
    if projeto.sede_possui_net:
        projeto.tipo_internet = validado['tipo_internet']
    else:
        projeto.pq_sem_internet = validado['pq_sem_internet']
        if projeto.pq_sem_internet == 'outro':
            projeto.pq_sem_internet = validado['pq_sem_internet_outro']

    # -- Entidade Proponente
    projeto.entidade = get_or_create(models.Entidade,
                                     nome=validado['nome_ent'])[0]

    if validado.get('endereco_ent_proj') == 'nao':
        projeto.entidade.endereco = get_or_create(common_models.Endereco,
            nome=validado['nome_ent'],
            cep=validado['end_ent_cep'],
            numero=validado['end_ent_numero'],
            logradouro=validado['end_ent_logradouro'],
            complemento=blank(validado['end_ent_complemento']),
            uf=validado['end_ent_uf'],
            cidade=validado['end_ent_cidade'],
            bairro=validado['end_ent_bairro'],
            latitude=blank(validado['end_ent_latitude']),
            longitude=blank(validado['end_ent_longitude']))[0]
    else:
        projeto.entidade.endereco = projeto.endereco_sede

    projeto.entidade.telefones = []

    for i, t in enumerate(validado['ent_tel']):
        tel = get_tel(t, validado['ent_tel_tipo'][i])
        projeto.entidade.telefones.append(tel)

    projeto.entidade.email = validado['email_ent']
    projeto.entidade.website = validado['website_ent']

    projeto.entidade.convenios = []
    if validado['convenio_ent'] == 'sim':
        for i in validado['outro_convenio']:
            conv = get_or_create(models.Convenio, nome=i)[0]
            projeto.entidade.convenios.append(conv)

    # -- Atividades exercidas pelo projeto
    # --- Qual a área de atuação das atividades do Projeto?
    projeto.atividades = []
    for i in validado['atividade']:
        obj = get_or_create(models.Atividade, nome=i)[0]
        projeto.atividades.append(obj)

    # ---  Com qual Público Alvo o Projeto é desenvolvido?
    # ---- Sob aspectos de Faixa Etária
    projeto.publico_alvo = []
    for i in validado['publico_alvo']:
        obj = get_or_create(models.PublicoAlvo, nome=i)[0]
        projeto.publico_alvo.append(obj)

    # ---- Sob aspectos das Culturas Tradicionais
    projeto.culturas_tradicionais = []
    for i in validado['culturas_tradicionais']:
        obj = get_or_create(models.CulturaTradicional, nome=i)[0]
        projeto.culturas_tradicionais.append(obj)

    # ---- Sob aspectos de Ocupação do Meio
    projeto.ocupacao_do_meio = []
    for i in validado['ocupacao_do_meio']:
        obj = get_or_create(models.OcupacaoDoMeio, nome=i)[0]
        projeto.ocupacao_do_meio.append(obj)

    # ---- Sob aspectos de Gênero
    projeto.genero = []
    for i in validado['genero']:
        obj = get_or_create(models.Genero, nome=i)[0]
        projeto.genero.append(obj)

    # --- Quais são as Manifestações e Linguagens que o Projeto utiliza
    # em suas atividades?
    projeto.manifestacoes_linguagens = []
    for i in validado['manifestacoes_linguagens']:
        obj = get_or_create(models.ManifestacaoLinguagem, nome=i)[0]
        projeto.manifestacoes_linguagens.append(obj)

    # --- O Projeto participa de alguma Ação do Programa Cultura Viva?
    projeto.acao_cultura_viva = []
    if validado['participa_cultura_viva'] == 'sim':
        for i in validado['acao_cultura_viva']:
            obj = get_or_create(models.AcaoCulturaViva, nome=i)[0]
            projeto.acao_cultura_viva.append(obj)

    projeto.descricao = validado['descricao']

    # -- Parcerias do Projeto
    projeto.parcerias = []
    if validado['estabeleceu_parcerias'] == 'sim':
        for i in validado['parcerias'] + validado['outro_parceiro']:
            obj = get_or_create(models.Parceiro, nome=i)[0]
            projeto.parcerias.append(obj)

    # -- Índice de acesso à cultura
    projeto.ind_oficinas = validado['ind_oficinas']
    projeto.ind_expectadores = validado['ind_expectadores']
    projeto.ind_populacao = validado['ind_populacao']

    projeto.responsavel = user
    
    try:
        session.commit()
    except Exception, e:
        session.rollback()
        raise e

    projeto = save_files(projeto, validado['avatar'], validado['documentacoes'])

    if validado.get('files_to_remove'):
        projeto = remove_docs(projeto, validado['files_to_remove'])    
    
    try:
        session.commit()
    except Exception, e:
        session.rollback()
        raise e
        
    return projeto

def remove_docs(projeto, docs):
    docs = map(long, docs.split(','))
    saved_docs = [i for i in projeto.documentacoes]
    projeto.documentacoes = []
    for doc in saved_docs:
        if doc.id in docs:
            try:
                remove_file(projeto.id, doc.doc)
            except Exception, e:
                print
                print e
                print
            doc.delete()
        else:
            projeto.documentacoes.append(doc)
    return projeto

def save_files(projeto, avatar=None, docs=None):

    if avatar:
        try:
            save_image(avatar.stream, projeto.id, 'projeto')
        except Exception, e:
            print
            print e
            print

    if docs:
        try:
            for f in docs:
                filename = f.filename
                save_file(f, projeto.id)
                doc = models.Documentacao()
                doc.doc = filename
                projeto.documentacoes.append(doc)
        except Exception, e:
            print
            print e
            print

    return projeto

def cadastra_projeto(validado, user):
    # Instanciando o modelo e associando os campos validados e
    # transformados em valores python à instância que será
    # salva no db.
    projeto = models.Projeto()
    return set_values_projeto(projeto, validado, user)

def make_schema():
    members = {}
    up = lambda x: members.update(x)
    map(up, [getattr(schemas_proj.Projeto, class_name).fields for class_name in \
        dir(schemas_proj.Projeto) if not class_name.startswith("__")])
    class ProjetoSchema(CdpcSchema):
        pass

    for key, v in members.items():
        setattr(ProjetoSchema, key, v)
    ProjetoSchema.fields.update(members)
    schema = ProjetoSchema
    return schema

def values_dict(projeto):

    simnao = lambda x: 'sim' if x else 'nao'
    end = lambda x: [getattr(e, x) for e in projeto.enderecos]
    tel = lambda x, tels: [getattr(t, x) for t in tels]
    rss = lambda x: [getattr(r, x) for r in projeto.redes_sociais]
    fee = lambda x: [getattr(f, x) for f in projeto.feeds]
    nom = lambda x: [i.nome for i in x]

    parc = lambda x: [i.nome for i in x \
                      if unicode(i.nome) in dict(PARCERIAS).keys()]
    outr_parc = lambda x: [i.nome for i in x \
                           if i.nome not in dict(PARCERIAS).keys()]

    getop =  lambda x, y: 'outro' if x is not None and x not in y else x
    getopoutro = lambda x, y: x if x not in y else None

    values = {}
    dynamic_values = {}
    
    #DadosProjeto
    values['nome'] = projeto.nome
    values['descricao'] = projeto.descricao
    values['tipo'] = getop(projeto.tipo,
                           ['ponto', 'pontao', 'iniciativa_premiada'])
    values['tipo_outro'] = getopoutro(projeto.tipo,
                           ['ponto', 'pontao', 'iniciativa_premiada'])
    values['tipo_convenio'] = projeto.tipo_convenio
    #values['avatar'] = projeto.avatar
    values['numero_convenio'] = projeto.numero_convenio
    values['acao_cultura_viva'] = map(lambda x: x.nome,
                                      projeto.acao_cultura_viva)
    values['participa_cultura_viva'] = simnao(values['acao_cultura_viva'])
    dynamic_values['parcerias'] = parc(projeto.parcerias)
    dynamic_values['outro_parceiro'] = outr_parc(projeto.parcerias)
    values['estabeleceu_parcerias'] = simnao(dynamic_values['parcerias'] or \
                                             dynamic_values['outro_parceiro'])
    
    #LocalizacaoGeoProjeto
    values['end_proj_cep'] = projeto.endereco_sede.cep
    values['end_proj_numero'] = projeto.endereco_sede.numero
    values['end_proj_logradouro'] = projeto.endereco_sede.logradouro
    values['end_proj_complemento'] = projeto.endereco_sede.complemento
    values['end_proj_uf'] = projeto.endereco_sede.uf
    values['end_proj_cidade'] = projeto.endereco_sede.cidade
    values['end_proj_bairro'] = projeto.endereco_sede.bairro
    values['end_proj_latitude'] = projeto.endereco_sede.latitude
    values['end_proj_longitude'] = projeto.endereco_sede.longitude
    values['local_proj'] = projeto.local
    dynamic_values['end_outro_nome'] = end('nome')
    dynamic_values['end_outro_cep'] = end('cep')
    dynamic_values['end_outro_numero'] = end('numero')
    dynamic_values['end_outro_logradouro'] = end('logradouro')
    dynamic_values['end_ent_complemento'] = end('complemento')
    dynamic_values['end_outro_uf'] = end('uf')
    dynamic_values['end_outro_cidade'] = end('cidade')
    dynamic_values['end_outro_bairro'] = end('bairro')
    dynamic_values['end_outro_latitude'] = end('latitude')
    dynamic_values['end_outro_longitude'] = end('longitude')
    
    #EntidadeProponente
    values['nome_ent'] = projeto.entidade.nome
    values['email_ent'] = projeto.entidade.email
    values['website_ent'] = projeto.entidade.website
    dynamic_values['ent_tel'] = tel('numero', projeto.entidade.telefones)
    dynamic_values['ent_tel_tipo'] = tel('tipo', projeto.entidade.telefones)
    values['convenio_ent'] = simnao(projeto.entidade.convenios)
    dynamic_values['outro_convenio'] = map(lambda x: x.nome,
                                           projeto.entidade.convenios)
    mesmo_que_sede = projeto.entidade.endereco.id == projeto.endereco_sede.id
    values['endereco_ent_proj'] = simnao(mesmo_que_sede)
    if not mesmo_que_sede:
        dynamic_values['end_ent_cep'] = [projeto.entidade.endereco.cep]
        dynamic_values['end_ent_numero'] = [projeto.entidade.endereco.numero]
        dynamic_values['end_ent_logradouro'] = [projeto.entidade.endereco.logradouro]
        dynamic_values['end_ent_complemento'] = [projeto.entidade.endereco.complemento]
        dynamic_values['end_ent_uf'] = [projeto.entidade.endereco.uf]
        dynamic_values['end_ent_cidade'] = [projeto.entidade.endereco.cidade]
        dynamic_values['end_ent_bairro'] = [projeto.entidade.endereco.bairro]
        dynamic_values['end_ent_latitude'] = [projeto.entidade.endereco.latitude]
        dynamic_values['end_ent_longitude'] = [projeto.entidade.endereco.longitude]

    #ComunicacaoCulturaDigital
    values['email_proj'] = projeto.email
    values['website_proj'] = projeto.website
    values['sede_possui_tel'] = simnao(projeto.sede_possui_tel)
    dynamic_values['sede_tel_tipo'] = tel('tipo', projeto.telefones)
    dynamic_values['sede_tel'] = tel('numero', projeto.telefones)
    values['pq_sem_tel'] = getop(projeto.pq_sem_tel, PQ_SEM_TEL)
    values['pq_sem_tel_outro'] = getopoutro(projeto.pq_sem_tel, PQ_SEM_TEL)
    values['sede_possui_net'] = simnao(projeto.sede_possui_net)
    values['tipo_internet'] = projeto.tipo_internet
    values['pq_sem_internet'] = getop(projeto.pq_sem_internet, PQ_SEM_INTERNET)
    values['pq_sem_internet_outro'] = getopoutro(projeto.pq_sem_internet,
                                                 PQ_SEM_INTERNET)
    dynamic_values['rs_nome'] = rss('nome')
    dynamic_values['rs_link'] = rss('link')
    dynamic_values['feed_nome'] = fee('nome')
    dynamic_values['feed_link'] = fee('link')

    #AtividadesExercidasProjeto
    values['atividade'] = nom(projeto.atividades)
    
    #Publico
    values['publico_alvo'] = nom(projeto.publico_alvo)
    values['culturas_tradicionais'] = nom(projeto.culturas_tradicionais)
    values['ocupacao_do_meio'] = nom(projeto.ocupacao_do_meio)
    values['genero'] = nom(projeto.genero)
    values['manifestacoes_linguagens'] = nom(projeto.manifestacoes_linguagens)

    #IndiceAcessoCultura
    values['ind_oficinas'] = projeto.ind_oficinas
    values['ind_expectadores'] = projeto.ind_expectadores
    values['ind_populacao'] = projeto.ind_populacao
    
    return values, dynamic_values

