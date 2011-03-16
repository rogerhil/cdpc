# -*- coding: utf-8; Mode: Python -*-
#
# Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
# Copyright (C) 2010  Marco Túlio Gontijo e Silva <marcot@marcot.eti.br>
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
from flask import Module, render_template, request, abort, make_response, \
                  url_for, redirect, flash
from formencode import Invalid, htmlfill
from simplejson import dumps

from ..common import models as common_models
from ..index import get_user_or_login
from ..utils.paginator import Paginator
from ..utils.schemas import CdpcSchema
from ..utils.filestorage import save_image, save_file
from . import schemas
from . import models
from . import cadastro
from ..common import cadastro as common_cadastro
from .models import Projeto

ERROR_TAG = lambda x : '<label generated="true" class="error">%s</label>' % x

module = Module(__name__)

@module.route('/')
def listing():

    vals_uf = common_cadastro.VALORES_UF
    vals_uf.sort(lambda a, b: a > b and 1 or -1)

    trevent = {'event': 'onclick',
               'value': 'mostraProjeto(%s, this)',
               'params': ['id']}

    columns = [('nome',   {'title': 'Nome', 'ambiguity': 'projeto'}),
               ('responsaveis', {'title': 'Cadastrado por', 'call': True}),
               ('cidade', {'title': 'Cidade', 'mcol': 'endereco_sede'}),
               ('uf', {'title': 'Estado', 'mcol': 'endereco_sede'}),
               ('data_cadastro', {'title': 'Data do cadastro', 'type': 'data'})]

    search_fields = [('nome',   {'label': 'Nome', 'type': 'text'}),
                     ('cidade', {'label': 'Cidade', 'type': 'text',
                                 'mcol': 'enderecos'}),
                     ('uf',     {'label': 'Estado', 'type': 'select',
                                 'mcol': 'enderecos',
                                 'choices': vals_uf})]

    paginator = Paginator(models.Projeto, columns, search_fields,
                          trevent=trevent)
    
    return render_template('projetos/listing.html',
                           paginator=paginator.render())

@module.route('<int:pid>.json')
def projeto_json(pid):
    projeto = models.Projeto.query.filter_by(id=pid).first()
    if projeto is None:
        return '{}'

    # Levantando dados do projeto
    responsavel = ''
    if projeto.responsavel:
        responsavel = projeto.responsavel[0].nome

    # Montando o json que vai ser retornado pra interface
    ctx = {
        'id': projeto.id,
        'nome': projeto.nome,
        'tipo': projeto.tipo,
        'endereco': {
            'nome': projeto.enderecos[0].nome,
            'logradouro': projeto.enderecos[0].logradouro,
            'bairro': projeto.enderecos[0].bairro,
            'cidade': projeto.enderecos[0].cidade,
            'uf': projeto.enderecos[0].uf,
        },
        'email': projeto.email,
        'site': projeto.website,
        'telefones': [x.numero for x in projeto.telefones],
    }

    ctx['telefones'] = []
    for i in projeto.telefones:
        ctx['telefones'].append(i.numero)

    if projeto.responsavel:
        resp = projeto.responsavel[0]
        ctx['responsavel'] = {
            'nome': resp.nome,
            'email': resp.email,
            'website': resp.website,
        }

    return dumps(ctx)

@module.route('<int:pid>.quickview.json')
def projeto_quickview_json(pid):
    projeto = models.Projeto.query.filter_by(id=pid).first()
    if projeto is None:
        return dumps({'error': 'Projeto não encontrado.'})
    
    rendered = render_template('projetos/quickview.html',
                               projeto=projeto,
                               cadastro=cadastro,
                               dict=dict)
    data = {'content': rendered}

    return dumps(data)
    
@module.route("validar/", methods=('GET', 'POST'))
def validar():
    class_name = request.form.get("step_name")
    class_name = class_name[0].upper() + class_name[1:]
    validator = getattr(schemas.Projeto, class_name)()
    fields = validator.fields
    data = dict(request.form.lists())
    del data["step_name"]
    if data.get('edit') and data['edit'][0]:
        projeto = Projeto.get_by(id=long(data['projeto_id'][0]))
        if validator.fields.get('email_proj'):
            validator.fields['email_proj'].valid_email = projeto.email
        del data['edit']
        del data['projeto_id']

    data = cadastro.prepare_data(data, fields)

    values_list = [i for i  in request.form.lists() if len(i[1]) > 1]
    errors_list = {}    
    validado = {}
    try:
        validado = validator.to_python(data)
    except Invalid, e:
        print "Exception"
        print e
        errors_list = dict([(i,j) for i,j in e.unpack_errors().items() if \
                           type(j) == list])
        rendered = render_template('projetos/novo/%s.html' % class_name.lower(),
                                   cadastro=cadastro)
        errors = dict([(i,j) for i,j in e.unpack_errors().items() \
                      if type(j) != list])
        filled = htmlfill.render(rendered, request.form.to_dict(), errors,
                                 prefix_error=False,
                                 auto_error_formatter=ERROR_TAG)

        print "--------------"
        print values_list
        print "--------------"
        ret = {'html': filled,
               'error': True,
               'errors_list': errors_list,
               'values_list': dict(values_list)}
        return make_response(dumps(ret))

    rendered = render_template(
                'projetos/novo/%s.html' % class_name.lower(),
                cadastro=cadastro,
                errors={},
                values=values_list)
    filled = htmlfill.render(rendered, request.form.to_dict(), {},
                             prefix_error=False)
    ret = {'html': filled,
           'error': False,
           'errors_list': errors_list,
           'values_list': dict(values_list)}
    return make_response(dumps(ret))

def set_values_projeto(projeto, validado, user):

    # -- Dados do projeto
    projeto.nome = validado['nome']
    projeto.tipo = validado['tipo']
    projeto.tipo_convenio = validado['tipo_convenio']
    projeto.numero_convenio = validado['numero_convenio']

    # -- Localização geográfica do projeto
    endsede = common_models.Endereco(cep=validado['end_proj_cep'],
                              numero=validado['end_proj_numero'],
                              logradouro=validado['end_proj_logradouro'],
                              complemento=validado['end_proj_complemento'],
                              uf=validado['end_proj_uf'],
                              cidade=validado['end_proj_cidade'],
                              bairro=validado['end_proj_bairro'],
                              latitude=validado['end_proj_latitude'],
                              longitude=validado['end_proj_longitude'])
    projeto.endereco_sede = endsede

    projeto.local = validado['local_proj']

    projeto.enderecos = []

    if projeto.local == 'outros':
        for i in range(len(validado['end_outro_nome'])):
            endereco = common_models.Endereco(
                nome=validado['end_outro_nome'][i],
                cep=validado['end_outro_cep'][i],
                numero=validado['end_outro_numero'][i],
                logradouro=validado['end_outro_logradouro'][i],
                #complemento=validado['end_outro_complemento'][i],
                uf=validado['end_outro_uf'][i],
                cidade=validado['end_outro_cidade'][i],
                bairro=validado['end_outro_bairro'][i])
                #latitude=validado['end_outro_latitude'][i],
                #longitude=validado['end_outro_longitude'][i])
            projeto.enderecos.append(endereco)

    # -- Contatos e espaços na rede

    ######################
    # CAMPOS EXCLUÍDOS!!!
    #projeto.email = validado['email_proj']        ------------> INCLUIDO
    #projeto.website = validado['website_proj']    ------------> INCLUIDO
    #projeto.frequencia = validado['frequencia']   
    #for i in validado['proj_tel']:                ------------> INCLUIDO
    #    tel = models.Telefone()
    #    tel.numero = i
    #    projeto.telefones.append(tel)
    ######################

    projeto.redes_sociais = []

    for i in range(len(validado['rs_nome'])):
        rsocial = common_models.RedeSocial()
        rsocial.nome = validado['rs_nome'][i]
        rsocial.link = validado['rs_link'][i]
        projeto.redes_sociais.append(rsocial)

    projeto.feeds = []

    for i in range(len(validado['feed_nome'])):
        feed = common_models.Feed()
        feed.nome = validado['feed_nome'][i]
        feed.link = validado['feed_link'][i]
        projeto.feeds.append(feed)

    # -- Comunicação e Cultura Digital
    
    projeto.email = validado['email_proj']
    projeto.website = validado['website_proj']

    def get_tel(numero):
        tel = None
        if common_models.Telefone.query.filter_by(numero=numero).count() and \
           (numero in [t.numero for t in projeto.telefones] or \
            numero in [t.numero for t in user.telefones] or \
            projeto.entidade and numero in \
            [t.numero for t in projeto.entidade.telefones]):
            if numero in [t.numero for t in projeto.telefones]:
                tel = [t for t in projeto.telefones if t.numero == numero][0]
            if numero in [t.numero for t in user.telefones]:
                tel = [t for t in user.telefones if t.numero == numero][0]
            if projeto.entidade and numero in \
               [t.numero for t in projeto.entidade.telefones]:
                tel = [t for t in projeto.entidade.telefones if \
                       t.numero == numero][0]
        else:
            tel = models.Telefone(numero=numero)
        return tel

    projeto.sede_possui_tel = validado['sede_possui_tel'] == 'sim'
    if projeto.sede_possui_tel:
        for i, t in enumerate(validado['sede_tel']):
            tel = get_tel(t)
            if validado['sede_tel_tipo']:
                tel.tipo = validado['sede_tel_tipo'][i]
            projeto.telefones.append(tel)
    else:
        projeto.pq_sem_tel = validado['pq_sem_tel']
        if projeto.pq_sem_tel == 'outro':
            projeto.pq_sem_tel_outro = validado['pq_sem_tel_outro']
    projeto.sede_possui_net = validado['sede_possui_net'] == 'sim'
    if projeto.sede_possui_net:
        projeto.tipo_internet = validado['tipo_internet']
    else:
        projeto.pq_sem_internet = validado['pq_sem_internet']
        if projeto.pq_sem_internet == 'outro':
            projeto.pq_sem_internet_outro = \
                validado['pq_sem_internet_outro']

    # -- Entidade Proponente
    projeto.entidade = models.Entidade(
        nome=validado['nome_ent'],
        )

    if validado.get('endereco_ent_proj') == 'nao':
        projeto.entidade.endereco =  common_models.Endereco(
                nome=validado['nome_ent'],
                cep=validado['end_ent_cep'],
                numero=validado['end_ent_numero'],
                logradouro=validado['end_ent_logradouro'],
                complemento=validado['end_ent_complemento'],
                uf=validado['end_ent_uf'],
                cidade=validado['end_ent_cidade'],
                bairro=validado['end_ent_bairro'],
                latitude=validado['end_ent_latitude'],
                longitude=validado['end_ent_longitude']
                )
    else:
        projeto.entidade.endereco = projeto.endereco_sede

    projeto.entidade.telefones = []

    for i, t in enumerate(validado['ent_tel']):
        tel = get_tel(t)
        if validado['ent_tel_tipo']:
            tel.tipo = validado['ent_tel_tipo'][i]        
        projeto.entidade.telefones.append(tel)

    projeto.entidade.email = validado['email_ent']
    projeto.entidade.website = validado['website_ent']

    if validado['convenio_ent'] == 'sim':
        for i in validado['outro_convenio']:
            conv = models.Convenio()
            conv.nome = i
            projeto.entidade.convenios.append(conv)

    # -- Atividades exercidas pelo projeto
    # --- Qual a área de atuação das atividades do Projeto?
    projeto.atividades = []
    for i in validado['atividade']:
        obj = models.Atividade()
        obj.nome = i
        projeto.atividades.append(obj)

    # ---  Com qual Público Alvo o Projeto é desenvolvido?
    # ---- Sob aspectos de Faixa Etária
    projeto.publico_alvo = []
    for i in validado['publico_alvo']:
        obj = models.PublicoAlvo()
        obj.nome = i
        projeto.publico_alvo.append(obj)

    # ---- Sob aspectos das Culturas Tradicionais
    projeto.culturas_tradicionais = []
    for i in validado['culturas_tradicionais']:
        obj = models.CulturaTradicional()
        obj.nome = i
        projeto.culturas_tradicionais.append(obj)

    # ---- Sob aspectos de Ocupação do Meio
    projeto.ocupacao_do_meio = []
    for i in validado['ocupacao_do_meio']:
        obj = models.OcupacaoDoMeio()
        obj.nome = i
        projeto.ocupacao_do_meio.append(obj)

    # ---- Sob aspectos de Gênero
    projeto.genero = []
    for i in validado['genero']:
        obj = models.Genero()
        obj.nome = i
        projeto.genero.append(obj)

    # --- Quais são as Manifestações e Linguagens que o Projeto utiliza
    # em suas atividades?
    projeto.manifestacoes_linguagens = []
    for i in validado['manifestacoes_linguagens']:
        obj = models.ManifestacaoLinguagem()
        obj.nome = i
        projeto.manifestacoes_linguagens.append(obj)

    # --- O Projeto participa de alguma Ação do Programa Cultura Viva?
    projeto.acao_cultura_viva = []
    if validado['participa_cultura_viva'] == 'sim':
        for i in validado['acao_cultura_viva']:
            obj = models.AcaoCulturaViva()
            obj.nome = i
            projeto.acao_cultura_viva.append(obj)

    projeto.descricao = validado['descricao']

    # TODO: Tratar upload de documentacoes

    # -- Parcerias do Projeto
    projeto.parcerias = []
    if validado['estabeleceu_parcerias'] == 'sim':
        ov = cadastro.item_format('Outros')
        outros = []
        if ov in validado['parcerias']:
            outros = validado.get('outro_parceiro', [])
            validado['parcerias'].remove(ov)
        for i in validado['parcerias'] + outros:
            obj = models.Parceiro()
            obj.nome = i
            projeto.parcerias.append(obj)

    # -- Índice de acesso à cultura
    projeto.ind_oficinas = validado['ind_oficinas']
    projeto.ind_expectadores = validado['ind_expectadores']
    projeto.ind_populacao = validado['ind_populacao']

    projeto.responsavel = []
    projeto.responsavel.append(user)
    
    try:
        session.commit()
    except Exception, e:
        session.rollback()
        raise e

    if validado['avatar']:
        try:
            save_image(validado['avatar'].stream, projeto.id, 'projeto')
        except Exception, e:
            print
            print e
            print
            pass

    if validado['documentacoes']:
        try:
            for f in validado['documentacoes']:
                filename = f.filename
                save_file(f, projeto.id)
                doc = models.Documentacao()
                doc.doc = filename
                projeto.documentacoes.append(doc)
        except Exception, e:
            print
            print e
            print
            pass

    try:
        session.commit()
    except Exception, e:
        session.rollback()
        raise e
        
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
    map(up, [getattr(schemas.Projeto, class_name).fields for class_name in \
        dir(schemas.Projeto) if not class_name.startswith("__")])
    class ProjetoSchema(CdpcSchema):
        pass

    for key, v in members.items():
        setattr(ProjetoSchema, key, v)
    ProjetoSchema.fields.update(members)
    schema = ProjetoSchema
    return schema

@module.route("novo/", methods=('GET', 'POST'))
def novo():
    """Formulário de cadastro de projetos.

    O Usuário precisa estar autenticado para usar esse form.
    """
    # Tenta pegar o usuário na sessão ou redireciona para o form de
    # login.
    user = get_user_or_login()

    # Validação de dados já enviados pelo usuário
    if request.method == 'POST':
        # instanciando o validador
        schema = make_schema()
        validator = schema()
        validado = {}
        try:
            data = dict(request.form.lists())
            data.update(request.files)
            data = cadastro.prepare_data(data, schema.fields)
            validado = validator.to_python(data)
        except Invalid, e:
            rendered = render_template(
                        'projetos/novo/main.html',
                        cadastro=cadastro,
                        title=u'Cadastro de Projetos')
            errors = e.error_dict
            filled = htmlfill.render(rendered, request.form.to_dict(), errors,
                                     prefix_error=False,
                                     auto_error_formatter=ERROR_TAG)
            return make_response(filled)
        else:
            projeto = cadastra_projeto(validado, user)
            flash(u'Projeto cadastrado com sucesso!', 'success')
            return redirect("/projetos")

    return render_template(
        'projetos/novo/main.html',
        cadastro=cadastro,
        title=u'Cadastro de Projetos')

def values_dict(projeto):

    simnao = lambda x: 'sim' if x else 'nao'
    end = lambda x: [getattr(e, x) for e in projeto.enderecos]
    tel = lambda x, tels: [getattr(t, x) for t in tels]
    rss = lambda x: [getattr(r, x) for r in projeto.redes_sociais]
    fee = lambda x: [getattr(f, x) for f in projeto.feeds]
    nom = lambda x: [i.nome for i in x]

    parc = lambda x: [i.nome for i in x \
                      if unicode(i.nome) in dict(cadastro.PARCERIAS).keys()]
    outr_parc = lambda x: [i.nome for i in x \
                           if i.nome not in dict(cadastro.PARCERIAS).keys()]

    #import pdb; pdb.set_trace()

    values = {}
    dynamic_values = {}
    
    #DadosProjeto
    values['nome'] = projeto.nome
    values['descricao'] = projeto.descricao
    values['tipo'] = projeto.tipo
    values['tipo_convenio'] = projeto.tipo_convenio
    #values['avatar'] = projeto.avatar
    values['numero_convenio'] = projeto.numero_convenio
    values['acao_cultura_viva'] = map(lambda x: x.nome,
                                      projeto.acao_cultura_viva)
    values['participa_cultura_viva'] = simnao(values['acao_cultura_viva'])
    values['parcerias'] = parc(projeto.parcerias)
    dynamic_values['parcerias'] = outr_parc(projeto.parcerias)
    values['estabeleceu_parcerias'] = simnao(values['parcerias'] or \
                                             dynamic_values['parcerias'])
    
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
    values['endereco_ent_proj'] = simnao(projeto.entidade.endereco.id == \
                                         projeto.endereco_sede.id)
    if not values['endereco_ent_proj']:
        values['end_ent_cep'] = projeto.entidade.endereco.cep
        values['end_ent_numero'] = projeto.entidade.endereco.numero
        values['end_ent_logradouro'] = projeto.entidade.endereco.logradouro
        values['end_ent_complemento'] = projeto.entidade.endereco.complemento
        values['end_ent_uf'] = projeto.entidade.endereco.uf
        values['end_ent_cidade'] = projeto.entidade.endereco.cidade
        values['end_ent_bairro'] = projeto.entidade.endereco.bairro
        values['end_ent_latitude'] = projeto.entidade.endereco.latitude
        values['end_ent_longitude'] = projeto.entidade.endereco.longitude

    #ComunicacaoCulturaDigital
    values['email_proj'] = projeto.email
    values['website_proj'] = projeto.website
    values['sede_possui_tel'] = simnao(projeto.sede_possui_tel)
    dynamic_values['sede_tel_tipo'] = tel('tipo', projeto.telefones)
    dynamic_values['sede_tel'] = tel('numero', projeto.telefones)
    values['pq_sem_tel'] = projeto.pq_sem_tel
    values['pq_sem_tel_outro'] = projeto.pq_sem_tel
    values['sede_possui_net'] = simnao(projeto.sede_possui_net)
    values['tipo_internet'] = projeto.tipo_internet
    values['pq_sem_internet'] = projeto.pq_sem_internet
    values['pq_sem_internet_outro'] = projeto.pq_sem_internet
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
    
@module.route("editar/<int:pid>/", methods=('GET', 'POST'))
def editar(pid):
    """Formulário de edicão de projetos.

    O Usuário precisa estar autenticado para usar esse form.
    """
    # Tenta pegar o usuário na sessão ou redireciona para o form de
    # login.
    #user = get_user_or_login()
    projeto = Projeto.get_by(id=pid)
    if not projeto:
        return make_response(u"Projeto não existe!")

    # Validação de dados já enviados pelo usuário
    if request.method == 'POST':
        # instanciando o validador
        schema = make_schema()
        validator = schema()
        validado = {}

        data = dict(request.form.lists())

        if data.get('edit') and data['edit'][0]:
            projeto = Projeto.get_by(id=long(data['projeto_id'][0]))
            if validator.fields.get('email_proj'):
                validator.fields['email_proj'].valid_email = projeto.email
            del data['edit']
            del data['projeto_id']


        try:
            data.update(request.files)
            data = cadastro.prepare_data(data, schema.fields)
            validado = validator.to_python(data)
        except Invalid, e:
            rendered = render_template(
                        'projetos/novo/main.html',
                        title=u"Edição do projeto %s" % projeto.nome,
                        edit='true',
                        projeto_id=projeto.id,
                        cadastro=cadastro)
            errors = e.error_dict
            filled = htmlfill.render(rendered, request.form.to_dict(), errors,
                                     prefix_error=False,
                                     auto_error_formatter=ERROR_TAG)
            return make_response(filled)
        else:

            projeto = set_values_projeto(projeto, validado, user)

            flash(u'Projeto editado com sucesso!', 'success')
            return redirect("/projetos")
    
    values, dynamic_values = values_dict(projeto)
    values['step'] = 'dadosProjeto'
    values['edit'] = 'true'
    values['projeto_id'] = projeto.id
    
    rendered = render_template(
                'projetos/novo/main.html',
                title=u"Edição do projeto %s" % projeto.nome,
                edit='true',
                projeto_id=projeto.id,
                cadastro=cadastro,
                dynamic_values=dumps(dynamic_values))
    
    filled = htmlfill.render(rendered, defaults=values)
    
    #filled = rendered
    print
    print values
    print
    return make_response(filled)

#    return render_template(
#        'projetos/novo/main.html',
#        cadastro=cadastro,
#        errors={})

