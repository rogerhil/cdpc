# -*- coding: utf-8; Mode: Python -*-
#
# Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
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

"""Controllers da index
"""
from hashlib import sha1
from sqlalchemy.orm.exc import NoResultFound
from flask import Module, request, render_template, session, \
    g, url_for, redirect, abort, flash
from .models import Pessoa

module = Module(__name__)

@module.route("/")
def index():
    """Renderiza o template da index
    """
    email = request.args.get('email', '')
    return render_template("index.html", email=email)

@module.route('login', methods=('POST',))
def login():
    """Autentica o usuário se ele existir na tabeloa de pessoas
    """
    usuario = request.form.get('email')
    senha = sha1(request.form.get('senha')).hexdigest()
    proxima = request.form.get('proxima', request.referrer)

    try:
        g.usuario = Pessoa.query.filter_by(email=usuario, senha=senha).one()
        session['usuario'] = usuario
        return redirect(proxima)
    except NoResultFound:
        proxima = '%s?erro=1&email=%s' % (proxima.split("?")[0], usuario)
        return redirect(proxima)

@module.route('login_form')
def login_form():
    """Exibe o form de login
    """
    proxima = request.args.get('proxima', request.referrer)
    email = request.args.get('email', '')
    if proxima == url_for('index.login_form'):
        proxima = url_for('index.index')
    if is_logged_in():
        flash(u'Usuário logado com sucesso!', 'success')
        return redirect(proxima)
    return render_template('login.html', proxima=proxima, email=email)

@module.route('logout')
def logout():
    """Apaga o nome do usuário da sessão
    """
    if 'usuario' in session:
        session.pop('usuario')
    flash(u'Sessão finalizada!', 'info')
    return redirect(url_for('index.index'))

def is_logged_in():
    """Retorna verdadeiro se o usuário estiver autenticado ou falso caso
    contrário.
    """
    return 'usuario' in session

def get_authenticated_user():
    """Retorna o usuário que está autenticado na sessão atual ou None.
    """
    usuario = getattr(g, 'usuario', None)
    if usuario is None and 'usuario' in session:
        g.usuario = Pessoa.query.filter_by(email=session['usuario']).one()
        return g.usuario
    return None

def get_user_or_login():
    """Retorna o usuário autenticado ou redireciona para a página de login
    """
    user = get_authenticated_user()
    if user is None:
        url = '%s?proxima=%s' % (url_for('index.login_form'), request.url)
        abort(redirect(url))
    return user
