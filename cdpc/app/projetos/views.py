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
from .decorators import edit_allowed, login_required
from ..index import get_user_or_login, get_authenticated_user
from ..utils.paginator import Paginator
from ..utils.schemas import CdpcSchema
from . import schemas
from . import models
from . import cadastro
from .models import Projeto


ERROR_TAG = lambda x : '<label generated="true" class="error">%s</label>' % x

module = Module('..projetos')


def _listing(title='Projetos', fixedquery=None, xcontext={}, search_fields={}):


    trevent = {
        'event': 'onclick',
        'value': 'mostraProjeto(%s, this)',
        'params': ['id']
    }

    columns = [
        ('nome', {'title': 'Nome', 'ambiguity': 'projeto_nome', 'width': 300}),
        ('responsavel.nome', {'title': 'Cadastrado por',
                              'ambiguity': 'pessoa_nome', 'width': 200}),
        ('endereco_sede.cidade', {'title': 'Cidade', 'width': 150}),
        ('endereco_sede.uf', {'title': 'UF', 'width': 20}),
        ('data_cadastro', {'title': 'Data cadastro', 'type': 'data'})
    ]

    paginator = Paginator(models.Projeto, columns, search_fields,
                          trevent=trevent, fixedquery=fixedquery)

    user = get_authenticated_user()
    
    return render_template('projetos/listing.html',
                           paginator=paginator.render(),
                           title=title,
                           user=user,
                           **xcontext)

@module.route('/')
def listing():

    vals_uf = cadastro.VALORES_UF
    vals_uf.sort(lambda a, b: a > b and 1 or -1)

    search_fields = [
        ('nome',   {'label': 'Nome', 'type': 'text'}),
        ('endereco_sede.cidade', {'label': 'Cidade', 'type': 'text'}),
        ('endereco_sede.uf', {'label': 'Estado', 'type': 'select', 
                              'choices': vals_uf})
    ]
    return _listing(search_fields=search_fields)

@module.route('meus/')
@login_required
def meus_projetos():
    user = get_authenticated_user()
    d = ({'responsavel.id': user.id}, {'responsavel.id': {'exactly': True}})
    xc = {'meus_projetos': True}

    vals_uf = cadastro.VALORES_UF
    vals_uf.sort(lambda a, b: a > b and 1 or -1)

    search_fields = [
        ('nome', {'label': 'Nome', 'type': 'text'}),
        ('endereco_sede.cidade', {'label': 'Cidade', 'type': 'text'}),
        ('endereco_sede.uf', {'label': 'Estado', 'type': 'select',
                              'choices': vals_uf})
    ]

    return _listing(title=u'Meus projetos', fixedquery=d,
                    xcontext=xc, search_fields=search_fields)

@module.route('<int:pid>/')
def view_projeto(pid):
    d = ({'id': long(pid)}, {'id': {'exactly': True}})
    xc = {'view_projeto': True}
    projeto = Projeto.get_by(id=long(pid))
    return _listing(title=u'Projeto %s' % projeto.nome, fixedquery=d,
                    xcontext=xc, search_fields={})

@module.route("novo/", methods=('GET', 'POST'))
@login_required
def novo():
    """Formulário de cadastro de projetos.

    O Usuário precisa estar autenticado para usar esse form.
    """
    user = get_authenticated_user()

    # Validação de dados já enviados pelo usuário
    if request.method == 'POST':
        # instanciando o validador
        schema = cadastro.make_schema()
        validator = schema()
        validado = {}
        try:
            data = dict(request.form.lists())
            data.update(request.files)
            data = cadastro.prepare_data(data, schema.fields)
            validado = validator.to_python(data)
        except Invalid, e:
            values_list = [i for i  in request.form.lists() if len(i[1]) > 1]
            errors_list = dict([(i,j) for i,j in e.unpack_errors().items() if \
                           type(j) == list])

            dynamic_values = dict(values_list)
            rendered = render_template(
                        'projetos/cadastro/main.html',
                        cadastro=cadastro,
                        dynamic_values=dumps(dynamic_values),
                        title=u'Cadastro de Projetos')
            errors = e.error_dict
            filled = htmlfill.render(rendered, request.form.to_dict(), errors,
                                     prefix_error=False,
                                     auto_error_formatter=ERROR_TAG)

            return make_response(filled)
        else:
            projeto = cadastro.cadastra_projeto(validado, user)
            flash(u'Projeto cadastrado com sucesso!', 'success')
            return redirect(url_for('projetos.view_projeto', pid=projeto.id))

    return render_template(
        'projetos/cadastro/main.html',
        cadastro=cadastro,
        title=u'Cadastro de Projetos')

@module.route("editar/<int:pid>/", methods=('GET', 'POST'))
@edit_allowed
def editar(pid):
    """Formulário de edicão de projetos.

    O Usuário precisa estar autenticado para usar esse form.
    """
    user = get_authenticated_user()
    projeto = Projeto.get_by(id=pid)

    # Validação de dados já enviados pelo usuário
    if request.method == 'POST':
        # instanciando o validador
        schema = cadastro.make_schema()
        validator = schema()
        validado = {}

        data = dict(request.form.lists())

        projeto = Projeto.get_by(id=long(data['projeto_id'][0]))
        if validator.fields.get('email_proj'):
            validator.fields['email_proj'].valid_email = projeto.email

        try:
            data.update(request.files)
            data = cadastro.prepare_data(data, schema.fields)
            validado = validator.to_python(data)
        except Invalid, e:
            rendered = render_template(
                        'projetos/cadastro/main.html',
                        title=u"Edição do projeto %s" % projeto.nome,
                        edit='true',
                        projeto=projeto,
                        cadastro=cadastro)
            errors = e.error_dict
            filled = htmlfill.render(rendered, request.form.to_dict(), errors,
                                     prefix_error=False,
                                     auto_error_formatter=ERROR_TAG)
            return make_response(filled)
        else:
            validado['files_to_remove'] = request.form['files_to_remove']
            projeto = cadastro.set_values_projeto(projeto, validado, user)

            flash(u'Projeto editado com sucesso!', 'success')
            return redirect(url_for('projetos.view_projeto', pid=projeto.id))
    
    values, dynamic_values = cadastro.values_dict(projeto)
    values['step'] = 'dadosProjeto'
    values['edit'] = 'true'
    values['projeto_id'] = projeto.id
    
    rendered = render_template(
                'projetos/cadastro/main.html',
                title=u"Edição do projeto %s" % projeto.nome,
                edit='true',
                projeto=projeto,
                cadastro=cadastro,
                dynamic_values=dumps(dynamic_values))
    
    filled = htmlfill.render(rendered, defaults=values)
    
    return make_response(filled)


@module.route("remover/<int:pid>/", methods=('GET', 'POST'))
@edit_allowed
def remover(pid):
    """View para remoção de projetos

    O Usuário precisa estar autenticado para remover
    """
    user = get_authenticated_user()
    projeto = Projeto.get_by(id=pid)
    projeto.delete()

    flash(u'Projeto removido com sucesso!', 'success')
    
    return redirect(url_for('projetos.listing'))
    

################################################################################
# Asyncronous views

@module.route("validar/", methods=('GET', 'POST'))
def validar():
    class_name = request.form.get("step_name")
    class_name = class_name[0].upper() + class_name[1:]
    validator = getattr(schemas.Projeto, class_name)()
    fields = validator.fields
    data = dict(request.form.lists())
    del data["step_name"]
    projeto = None
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
        rendered = render_template('projetos/cadastro/%s.html' % class_name.lower(),
                                    projeto=projeto,
                                    cadastro=cadastro)
        errors = dict([(i,j) for i,j in e.unpack_errors().items() \
                      if type(j) != list])
        filled = htmlfill.render(rendered, request.form.to_dict(), errors,
                                 prefix_error=False,
                                 auto_error_formatter=ERROR_TAG)

        ret = {'html': filled,
               'error': True,
               'errors_list': errors_list,
               'values_list': dict(values_list)}
        return make_response(dumps(ret))

    rendered = render_template(
                'projetos/cadastro/%s.html' % class_name.lower(),
                cadastro=cadastro,
                projeto=projeto,
                errors={},
                values=values_list)
    filled = htmlfill.render(rendered, request.form.to_dict(), {},
                             prefix_error=False)
    ret = {'html': filled,
           'error': False,
           'errors_list': errors_list,
           'values_list': dict(values_list)}
    return make_response(dumps(ret))

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
                               user=get_authenticated_user())
    data = {'content': rendered}

    return dumps(data)

