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
    g, url_for, redirect
from .models import Pessoa

module = Module(__name__)

@module.route("/")
def index():
    """Renderiza o template da index
    """
    return render_template("index.html")

@module.route('login', methods=('POST',))
def login():
    """Autentica o usuário se ele existir na tabeloa de pessoas
    """
    usuario = request.form.get('usuario')
    senha = sha1(request.form.get('senha')).hexdigest()
    proxima = request.form.get('proxima_pagina', request.referrer)
    try:
        g.usuario = Pessoa.query.filter_by(usuario=usuario, senha=senha).one()
        session['usuario'] = usuario
        return redirect(proxima)
    except NoResultFound:
        proxima += '?erro=1'
        return redirect(proxima)

@module.route('logout')
def logout():
    """Apaga o nome do usuário da sessão
    """
    if 'usuario' in session:
        session.pop('usuario')
    return redirect(url_for('index.index'))

def is_logged_in():
    """Retorna verdadeiro se o usuário estiver autenticado ou falso caso
    contrário.
    """
    return 'usuario' in session
