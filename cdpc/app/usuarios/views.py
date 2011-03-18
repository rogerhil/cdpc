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

"""Contém as visualizações para a gestão de usuários
"""
from hashlib import sha1
from math import ceil
from formencode import Invalid, htmlfill
from simplejson import dumps, loads
from flask import Module, request, render_template, flash, make_response, \
                  redirect, url_for
from elixir import session

from ..common import models as common_models
from ..index import get_authenticated_user, check_password
from ..utils.paginator import Paginator
from ..utils.filestorage import save_image
from . import cadastro
from . import models
from . import schemas
from .decorators import login_required

module = Module('..usuarios')

def _listing(title='Pessoas', fixedquery=None, xcontext={}, search_fields={}):

    trevent = {'event': 'onclick',
               'value': 'mostraPessoa(%s, this)',
               'params': ['id']}

    columns = [('nome',   {'title': 'Nome', 'ambiguity': 'pessoa'}),
               ('cidade', {'title': 'Cidade', 'mcol': 'endereco'}),
               ('uf',     {'title': 'Estado', 'mcol': 'endereco'}),
               ('data_cadastro', {'title': 'Data do cadastro', 'type': 'data'})]

    paginator = Paginator(models.Pessoa, columns, search_fields,
                          trevent=trevent, fixedquery=fixedquery)
    
    return render_template('usuarios/listing.html',
                           paginator=paginator.render(),
                           title=title,
                           **xcontext)

@module.route('/')
def listing():
    vals_uf = cadastro.VALORES_UF
    
    search_fields = [('nome',   {'label': 'Nome', 'type': 'text'}),
                     ('cidade', {'label': 'Cidade', 'type': 'text',
                                 'mcol': 'endereco'}),
                     ('uf',     {'label': 'Estado', 'type': 'select',
                                  'mcol': 'endereco',
                                 'choices': vals_uf})]
    return _listing(search_fields=search_fields)

@module.route('meusdados/')
@login_required
def meusdados():
    user = get_authenticated_user()
    d = ({'id': user.id}, {'id': {'exactly': True}})
    xc = {'meusdados': True}
    return _listing(title=u'Meus dados', fixedquery=d,
                    xcontext=xc, search_fields={})

@module.route("novo/", methods=('GET', 'POST'))
def novo():
    """Renderiza o formulário de cadastro de usuários
    """
    if request.method == 'POST':
        # instanciando o validador
        validator = schemas.Usuario()
        validado = {}
        try:
            data = dict(request.form.lists())
            data.update(request.files)
            data = cadastro.prepare_data(data, validator.fields)
            validado = validator.to_python(data)
            clean_list = lambda x: [i for i in x if i.strip()];

        except Invalid, e:
            print e
            errors = e.unpack_errors()
            if not isinstance(errors, dict):
                raise Exception(errors)
            errors_list = dict([(i,j) for i,j in errors.items() if type(j) == list])
            values_list = [i for i  in request.form.lists() if len(i[1]) > 1]
            rendered = render_template(
                'usuarios/novo.html',
                title=u'Cadastro de usuários',
                cadastro=cadastro,
                errors=dict([(i,j) for i,j in errors.items() if type(j) == list]),
                errors_list=dumps(errors_list),
                values_list=dumps(dict(values_list)),
                values=[i for i  in request.form.lists() if len(i[1]) > 1])
            errors = e.error_dict
            error_tag = lambda x : '<label generated="true" class="error">%s</label>' % x
            filled = htmlfill.render(rendered, request.form.to_dict(), errors, prefix_error=False, auto_error_formatter=error_tag)
            return make_response(filled)

        else:
            pessoa = models.Pessoa()
            validado['remote_addr'] = request.remote_addr
            cadastro.set_values_pessoa(pessoa, validado)
            flash(u'Usuário cadastrado com sucesso!', 'success')
            return redirect("/usuarios/")

    return render_template('usuarios/novo.html',
                           title=u'Cadastro de usuários',
                           cadastro=cadastro)

@module.route("meusdados/editar/", methods=('GET', 'POST'))
@login_required
def editar_meusdados():
    """Renderiza o formulário de cadastro de usuários
    """
    
    user = get_authenticated_user()
    pessoa = user
    
    if request.method == 'POST':
        # instanciando o validador
        schema = schemas.Usuario
        schema.chained_validators.pop(0)
        validator = schema()
        validator.fields['email'].valid_email = user.email
        validator.fields['cpf'].valid_cpf = user.cpf
        del validator.fields['senha']
        del validator.fields['confirmar_senha']
        validado = {}
        try:
            data = dict(request.form.lists())
            data.update(request.files)
            data = cadastro.prepare_data(data, validator.fields)
            validado = validator.to_python(data)
            clean_list = lambda x: [i for i in x if i.strip()];

        except Invalid, e:
            print e
            errors = e.unpack_errors()
            if not isinstance(errors, dict):
                raise Exception(errors)
            errors_list = dict([(i,j) for i,j in errors.items() \
                                if type(j) == list])
            values_list = [i for i  in request.form.lists() if len(i[1]) > 1]
            rendered = render_template(
                'usuarios/novo.html',
                title=u'Meus dados',
                pessoa=pessoa,
                cadastro=cadastro,
                edit=True,
                errors=dict([(i,j) for i,j in errors.items() \
                            if type(j) == list]),
                errors_list=dumps(errors_list),
                values_list=dumps(dict(values_list)),
                values=[i for i  in request.form.lists() if len(i[1]) > 1])
            errors = e.error_dict
            error_tag = lambda x : '<label generated="true" ' \
                                   'class="error">%s</label>' % x
            filled = htmlfill.render(rendered, request.form.to_dict(), errors,
                                     prefix_error=False,
                                     auto_error_formatter=error_tag)
            return make_response(filled)

        else:
            validado['remote_addr'] = request.remote_addr
            cadastro.set_values_pessoa(pessoa, validado)
            flash(u'Dados editados com sucesso!', 'success')
            return redirect(url_for('usuarios.meusdados'))

    values, values_list = cadastro.values_dict(pessoa)

    rendered = render_template(
        'usuarios/novo.html',
        title=u'Meus dados',
        pessoa=pessoa,
        cadastro=cadastro,
        values_list=dumps(values_list),
        values=[i for i in values.items() if len(unicode(i[1])) > 1],
        edit=True)

    filled = htmlfill.render(rendered, values)

    return make_response(filled)



################################################################################
# Asyncronous views

@module.route('<int:pid>.quickview.json')
def pessoa_quickview_json(pid):
    pessoa = models.Pessoa.get_by(id=pid)
    if pessoa is None:
        return dumps({'error': 'Pessoa não encontrada.'})
    
    rendered = render_template('usuarios/quickview.html',
                               pessoa=pessoa,
                               cadastro=cadastro,
                               dict=dict)
    data = {'content': rendered}
    return dumps(data)

@module.route('meusdados/<int:pid>.quickview.json')    
@login_required
def meusdados_quickview_json(pid):
    return pessoa_quickview_json(pid)


@module.route('meusdados/trocarsenha/trocarsenha.json', methods=('POST', ))
def trocar_senha_json():
    pessoa = get_authenticated_user()
    data = request.form.to_dict()
    res = {'success': True, 'msg': []}

    if not data['senha_nova']:
        res['success'] = False
        res['msg'] = ['trocar_senha', u'Senha nova vazia']
    elif not data['confirmar_senha']:
        res['success'] = False
        res['msg'] = ['confirmar_trocar_senha', u'Confimação de senha vazia']

    if res['success']:
        if check_password(pessoa, data['senha_antiga']):
            if data['senha_nova'] == data['confirmar_senha']:
                cadastro.set_senha(pessoa, data['senha_nova'])
            else:
                res['success'] = False
                res['msg'] = ['trocar_senha', u'As senhas não batem.']
        else:
            res['success'] = False
            res['msg'] = ['senha_antiga', u'Senha antiga incorreta.']

    return dumps(res)

