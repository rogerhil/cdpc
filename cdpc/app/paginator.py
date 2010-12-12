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

from . import models
from math import ceil
from flask import request, render_template
from sqlalchemy import desc

class Paginator(object):
    
    def __init__(self, model, columns, search_fields, cvars={}):
        self.model = model
        self.columns = columns
        self.search_fields = search_fields
        self.cvars = cvars
        self.limites = [10, 20, 30, 40, 50, 100, 200]
    
    def _order_columns(self, d):
        items = []
        for col, props in self.columns:
            items.append((col, d[col]))
        return items
    
    def _order_items(self, order_by, query):
        cols = dict(self.columns).copy()
        for key, props in cols.items():
            cols[key]['thclass'] = 'arrowdown'
        for oby in order_by:
            n = oby.replace('-', '')
            if not (n in self.model.__dict__.keys() and \
                    not hasattr(getattr(self.model, n), '__call__')):
                continue
            if oby.startswith('-'):
                query = query.order_by(desc(n))                
            else:
                query = query.order_by(oby)
            cssclass = oby.startswith('-') and "arrowup" or "arrowdown"
            cols[n]['thclass'] = cssclass
        self.columns = self._order_columns(cols)
        return query
    
    def _make_query(self):
        query = self.model.query
        for col, props in self.search_fields:
            value = request.args.get(col, '')
            if not value:
                continue
            if props.get('mcol'):
                mcol = props['mcol']
                if hasattr(getattr(self.model, mcol).property, 'mapper'):                
                    cmodel = getattr(self.model, mcol).property.mapper.class_
                    query = query.filter(getattr(self.model, mcol).any(getattr(cmodel, col).contains(value)))                
            else:
                if self.model.table.columns[col].foreign_keys._list:
                    fk = self.model.table.columns[col].foreign_keys[0]
                    table = fk.column.table.name
                    cmodel = getattr(models, table.capitalize())
                    query = query.filter(getattr(cmodel, col).contains(value))
                else:
                    query = query.filter(getattr(self.model, col).contains(value))

        return query
    
    def render(self):
        page = int(request.args.get('page', 1) or 1)
        limit = int(request.args.get('limit', 20))
        order_by = [i.strip() for i in request.args.get('order_by', '').split(' ') if i.strip()]
        
        query = self._make_query()
        query = self._order_items(order_by, query)
        count = query.count()
        pages = int(ceil(count / limit))
        page = (page >= pages and pages) and pages or page
        index = limit*(page-1)               
        items = query[index:index+limit]

        display = min(limit, count)
        pagination = dict(count=count, limit=limit, pages=pages, page=page,
                          display=display)

        cvars = request.args.copy()
        cvars['limit'] = limit
        cvars['page'] = page
        cvars['limites'] = [i for i in self.limites]
        cvars['order_by'] = " ".join(order_by)
        cvars.update(self.cvars)
        
        return render_template('utils/paginator.html',
                               items=items,
                               pagination=pagination,
                               search_fields=self.search_fields,
                               columns=self.columns,
                               cvars=cvars,
                               string=str)

