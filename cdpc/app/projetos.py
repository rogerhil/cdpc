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

from formencode import Invalid, foreach
from flask import Module, render_template, request, abort, make_response, \
                  url_for, redirect, flash
from elixir import session
from simplejson import dumps
from formencode import htmlfill

from . import schemas
from . import models
from .index import get_user_or_login
import cadastro
from schemas import CdpcSchema
from .paginator import Paginator

module = Module(__name__)

@module.route('/')
def listing():

    vals_uf = cadastro.VALORES_UF
    vals_uf.sort(lambda a, b: a > b and 1 or -1)

    trevent = {'event': 'onclick',
               'value': 'mostraProjeto(%s, this)',
               'params': ['id']}

    columns = [('nome',   {'title': 'Nome'}),
               ('responsaveis', {'title': 'Cadastrado por', 'call': True}),
               ('cidade', {'title': 'Cidade', 'mcol': 'enderecos'}),
               ('uf', {'title': 'Estado', 'mcol': 'enderecos'}),
               ('data_cadastro', {'title': 'Data do cadastro', 'type': 'data'})]

    search_fields = [('nome',   {'label': 'Nome', 'type': 'text'}),
                     ('cidade', {'label': 'Cidade', 'type': 'text', 'mcol': 'enderecos'}),
                     ('uf',     {'label': 'Estado', 'type': 'select', 'mcol': 'enderecos',
                                 'choices': vals_uf})]

    paginator = Paginator(models.Projeto, columns, search_fields, trevent=trevent)
    
    return render_template('projetos/listing.html', paginator=paginator.render())

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

    format_tel = lambda x : "(%s) %s.%s" % (x[:2], x[2:6], x[6:])
    
    rendered = render_template('projetos/quickview.html',
                               projeto=projeto,
                               format_tel=format_tel)
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
    data = cadastro.prepare_data(data, fields)
    values_list = [i for i  in request.form.lists() if len(i[1]) > 1]
    errors_list = {}    
    validado = {}
    try:
        validado = validator.to_python(data)
        
    except Invalid, e:
        print "Exception"
        print e
        errors_list = dict([(i,j) for i,j in e.unpack_errors().items() if type(j) == list])

        rendered = render_template(
                    'projetos/novo/%s.html' % class_name.lower(),
                    cadastro=cadastro,
                    errors=errors_list,
                    values=values_list)
        errors = dict([(i,j) for i,j in e.unpack_errors().items() if type(j) != list])
        error_tag = lambda x : '<label generated="true" class="error">%s</label>' % x
        filled = htmlfill.render(rendered, request.form.to_dict(), errors, prefix_error=False, auto_error_formatter=error_tag)
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
    filled = htmlfill.render(rendered, request.form.to_dict(), {}, prefix_error=False)
    ret = {'html': filled,
           'error': False,
           'errors_list': errors_list,
           'values_list': dict(values_list)}
    return make_response(dumps(ret))

def cadastra_projeto(validado, user):
    # Instanciando o modelo e associando os campos validados e
    # transformados em valores python à instância que será
    # salva no db.
    projeto = models.Projeto()

    # -- Dados do projeto
    projeto.nome = validado['nome']
    projeto.tipo = validado['tipo']
    projeto.tipo_convenio = validado['tipo_convenio']
    projeto.numero_convenio = validado['numero_convenio']

    # -- Localização geográfica do projeto
    projeto.enderecos.append(
        models.Endereco(
            cep=validado['end_proj_cep'],
            numero=validado['end_proj_numero'],
            logradouro=validado['end_proj_logradouro'],
            complemento=validado['end_proj_complemento'],
            uf=validado['end_proj_uf'],
            cidade=validado['end_proj_cidade'],
            bairro=validado['end_proj_bairro'],
            latitude=validado['end_proj_latitude'],
            longitude=validado['end_proj_longitude']
            )
        )

    projeto.local = validado['local_proj']

    if projeto.local == 'outros':
        for i in range(len(validado['end_outro_nome'])):
            endereco = models.Endereco(nome=validado['end_outro_nome'][i],
                                       cep=validado['end_outro_cep'][i],
                                       numero=validado['end_outro_numero'][i],
                                       logradouro=validado['end_outro_logradouro'][i],
                                       complemento=validado['end_outro_complemento'][i],
                                       uf=validado['end_outro_uf'][i],
                                       cidade=validado['end_outro_cidade'][i],
                                       bairro=validado['end_outro_bairro'][i],
                                       latitude=validado['end_outro_latitude'][i],
                                       longitude=validado['end_outro_longitude'][i])
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

    for i in range(len(validado['rs_nome'])):
        rsocial = models.RedeSocial()
        rsocial.nome = validado['rs_nome'][i]
        rsocial.link = validado['rs_link'][i]
        projeto.redes_sociais.append(rsocial)

    for i in range(len(validado['feed_nome'])):
        feed = models.Feed()
        feed.nome = validado['feed_nome'][i]
        feed.link = validado['feed_link'][i]
        projeto.feeds.append(feed)

    # -- Comunicação e Cultura Digital
    
    projeto.email = validado['email_proj']
    projeto.website = validado['website_proj']    
    
    
    def get_tel(numero):
        tel = None
        if models.Telefone.query.filter_by(numero=numero).count() and \
           (numero in [t.numero for t in projeto.telefones] or \
            numero in [t.numero for t in user.telefones] or \
            projeto.entidade and numero in [t.numero for t in projeto.entidade.telefones]):
            if numero in [t.numero for t in projeto.telefones]:
                tel = [t for t in projeto.telefones if t.numero == numero][0]
            if numero in [t.numero for t in user.telefones]:
                tel = [t for t in user.telefones if t.numero == numero][0]
            if projeto.entidade and numero in [t.numero for t in projeto.entidade.telefones]:
                tel = [t for t in projeto.entidade.telefones if t.numero == numero][0]
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
        projeto.entidade.enderecos.append(
            models.Endereco(
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
            )
    else:
        for end in projeto.enderecos:
            projeto.entidade.enderecos.append(end)

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
    for i in validado['atividade']:
        obj = models.Atividade()
        obj.nome = i
        projeto.atividades.append(obj)

    # ---  Com qual Público Alvo o Projeto é desenvolvido?
    # ---- Sob aspectos de Faixa Etária
    for i in validado['publico_alvo']:
        obj = models.PublicoAlvo()
        obj.nome = i
        projeto.publico_alvo.append(obj)

    # ---- Sob aspectos das Culturas Tradicionais
    for i in validado['culturas_tradicionais']:
        obj = models.CulturaTradicional()
        obj.nome = i
        projeto.culturas_tradicionais.append(obj)

    # ---- Sob aspectos de Ocupação do Meio
    for i in validado['ocupacao_do_meio']:
        obj = models.OcupacaoDoMeio()
        obj.nome = i
        projeto.ocupacao_do_meio.append(obj)

    # ---- Sob aspectos de Gênero
    for i in validado['genero']:
        obj = models.Genero()
        obj.nome = i
        projeto.genero.append(obj)

    # --- Quais são as Manifestações e Linguagens que o Projeto utiliza
    # em suas atividades?
    for i in validado['manifestacoes_linguagens']:
        obj = models.ManifestacaoLinguagem()
        obj.nome = i
        projeto.manifestacoes_linguagens.append(obj)

    # --- O Projeto participa de alguma Ação do Programa Cultura Viva?
    if validado['participa_cultura_viva'] == 'sim':
        for i in validado['acao_cultura_viva']:
            obj = models.AcaoCulturaViva()
            obj.nome = i
            projeto.acao_cultura_viva.append(obj)

    descricao = validado['descricao']

    # TODO: Tratar upload de documentacoes

    # -- Parcerias do Projeto
    if validado['estabeleceu_parcerias'] == 'sim':
        for i in validado['parcerias']:
            obj = models.Parceiro()
            obj.nome = i
            projeto.parcerias.append(obj)

    # -- Índice de acesso à cultura
    projeto.ind_oficinas = validado['ind_oficinas']
    ind_expectadores = validado['ind_expectadores']
    ind_populacao = validado['ind_populacao']

    projeto.responsavel.append(user)

    # -- Avatar
    # TODO: Tratar upload de avatar
    
    try:
        session.commit()
    except Exception, e:
        session.rollback()
        raise e
    return projeto

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
        members = {}
        up = lambda x: members.update(x)
        map(up, [getattr(schemas.Projeto, class_name).fields for class_name in dir(schemas.Projeto) if not class_name.startswith("__")])
        class ProjetoSchema(CdpcSchema):
            pass

        for key, v in members.items():
            setattr(ProjetoSchema, key, v)
        ProjetoSchema.fields.update(members)
        validator = ProjetoSchema()
        validado = {}
        print 'POST'
        try:
            data = dict(request.form.lists())
            data = cadastro.prepare_data(data, ProjetoSchema.fields)
            validado = validator.to_python(data)

        except Invalid, e:
            rendered = render_template(
                        'projetos/novo/main.html',
                        cadastro=cadastro,
                        errors=dict([(i,j) for i,j in e.unpack_errors().items() if type(j) == list]),
                        values=[i for i  in request.form.lists() if len(i[1]) > 1])
            errors = e.error_dict
            
            error_tag = lambda x : '<label generated="true" class="error">%s</label>' % x
            filled = htmlfill.render(rendered, request.form.to_dict(), errors, prefix_error=False, auto_error_formatter=error_tag)
            return make_response(filled)
        else:

            projeto = cadastra_projeto(validado, user)

            flash(u'Projeto cadastrado com sucesso!', 'success')
            return redirect("/projetos")

    return render_template(
        'projetos/novo/main.html',
        cadastro=cadastro,
        errors={})
        
