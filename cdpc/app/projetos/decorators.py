# -*- coding: utf-8; Mode: Python -*-
#
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

from functools import wraps

from ..common.decorators import *
from ..index import redirect_to_main, get_user_or_login
from .models import Projeto

def edit_allowed(f):
    """
    """
    @wraps(f)
    def check(pid, *args, **kwargs):
        user = get_user_or_login()
        projeto = Projeto.get_by(id=pid)
        if not projeto:
            redirect_to_main(u'Projeto não existe.', 'error')
        if not user or not user.id in [p.id for p in projeto.responsavel]:
            redirect_to_main(u'Acesso proibido.', 'error')
        return f(pid, *args, **kwargs)

    return check