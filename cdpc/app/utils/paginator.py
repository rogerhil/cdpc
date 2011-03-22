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

import re
from math import ceil

from flask import request, render_template
from sqlalchemy import desc, orm

from ..common import models as common_models
from ..projetos import models as projetos_models
from ..usuarios import models as usuarios_models

class Paginator(object):
    
    pages_display_limit_range = 3
    
    def __init__(self, model, columns, search_fields, cvars={},
                 quickview=None, trevent=None, fixedquery=None):
        self.model = model
        self.columns = columns
        self.search_fields = search_fields
        self.cvars = cvars
        self.limites = [10, 20, 30, 40, 50, 100, 200]
        self.quickview = quickview
        self.trevent = trevent
        self.fixedquery = fixedquery
    
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
            clause = oby.replace('-', '')
            key = clause
            if hasattr(getattr(self.model, clause, None), '__call__'):
                continue
            match = re.match('^([\w_]+)\.([\w_]+)$', clause)
            if match:
                attr, subattr = match.groups()
                clause = subattr
                key = subattr
                query = query.join(attr)

            amb = dict(self.columns)[clause].get('ambiguity')
            dcol = dict(self.columns)[clause].get('col')
            if dcol:
                clause = dcol
            if amb:
                clause = "%s.%s" % (amb, clause)    
            if oby.startswith('-'):
                query = query.order_by(desc(clause))
            else:
                query = query.order_by(clause)
            cssclass = oby.startswith('-') and "arrowup" or "arrowdown"
            cols[key]['thclass'] = cssclass
        self.columns = self._order_columns(cols)
        return query
    
    def _get_model(self, table):
        models = [common_models, projetos_models, usuarios_models]
        cmodel = None
        for mds in models:
            cmodel = getattr(mds, table.capitalize())
            if cmodel:
                return cmodel
    
    def _make_query(self):
        query = self.model.query
        args = request.args.copy()
        d = dict(self.search_fields).copy()
        if self.fixedquery:
            if self.fixedquery[1]:
                d.update(self.fixedquery[1])
            args.update(self.fixedquery[0])
        for col, props in d.items():
            subcol = None
            value = args.get(col, '')
            if col.find('.') != -1:
                col, subcol = col.split('.')
            if not value:
                continue
            if props.get('mcol'):
                mcol = props['mcol']
                col = props.get('col', col)
                if hasattr(getattr(self.model, mcol).property, 'mapper'):                
                    cmodel = getattr(self.model, mcol).property.mapper.class_
                    if props.get('exactly'):
                        query = query.filter(getattr(self.model, mcol).any(getattr(cmodel, col).op('=')(value)))
                    else:
                        query = query.filter(getattr(self.model, mcol).any(getattr(cmodel, col).contains(value)))
            else:
                if subcol:
                    cmodel = getattr(self.model, col).property.mapper.class_
                    if props.get('exactly'):
                        query = query.filter(getattr(self.model, col).has(getattr(cmodel, subcol).op('=')(value)))
                    else:
                        query = query.filter(getattr(self.model, col).has(getattr(cmodel, subcol).contains(value)))
                else:
                    if props.get('exactly'):
                        query = query.filter_by(**{col: value})                        
                    else:
                        query = query.filter(getattr(self.model, col).contains(value))

        return query
    
    @staticmethod
    def cel_content(item, cid, props):
        value = ""
        if props.get('call'):
            value = getattr(item, cid)()
        else:
            if props.get('mcol'):
                mcol = getattr(item, props['mcol'])
                if mcol:
                    if hasattr(mcol, '__iter__'):
                        value = ", ".join(list(set([getattr(i, cid) for i in mcol])))
                    else:
                        value = getattr(mcol, cid)
            else:
                value = getattr(item, cid)
        return value
    
    def tr_event(self, item):
        if not self.trevent:
            return ''
        event = self.trevent['event']
        func = self.trevent['value']
        params = self.trevent['params']
        func = func % tuple([getattr(item, p) for p in params])
        value = '%s="%s"' % (event, func)
        return value
        
    def render(self):
        natural = lambda x: x if x > 0 else 1
        page = natural(int(request.args.get('page', 1) or 1))
        limit = int(request.args.get('limit', 20))
        order_by = [i.strip() for i in request.args.get('order_by', '').split(' ') if i.strip()]
        
        query = self._make_query()
        query = self._order_items(order_by, query)
        count = query.count()
        pages = int(ceil(float(count)/limit))
        page = (page >= pages and pages) and pages or page
        index = limit*(page-1)               
        items = query[index:index+limit]

        display = min(limit, count)
        pagination = dict(count=count, limit=limit, pages=pages, page=page,
                          display=display)

        items_count = len(items)

        pd = self.pages_display_limit_range
        upd = lambda x: x + pd + 1 if (x - pd + 1) > 1 else 2*pd + 2
        dpd = lambda x: natural(page-pd) if (pages - x) > pd else natural(page-pd - (pd - (pages - x)))
        until = lambda x: upd(x) if upd(x) <= pages else pages + 1
        
        cvars = request.args.copy()
        cvars['limit'] = limit
        cvars['exibition'] = limit if limit <= items_count else items_count
        cvars['page'] = page
        cvars['pages_range'] = range(dpd(page), until(page))
        cvars['limites'] = [i for i in self.limites]
        cvars['order_by'] = " ".join(order_by)
        cvars.update(self.cvars)
        
        return render_template('utils/paginator.html',
                               items=items,
                               pagination=pagination,
                               search_fields=self.search_fields,
                               columns=self.columns,
                               cvars=cvars,
                               quickview=self.quickview,
                               string=str,
                               cel=Paginator.cel_content,
                               tr_event=self.tr_event)

