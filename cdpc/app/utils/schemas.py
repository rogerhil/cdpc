# -*- coding: utf-8; Mode: Python -*-
#
# Copyright (C) 2010  Rogério Hilbert Lima <rogerhil@gmail.com>
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

import formencode

class CdpcSchema(formencode.Schema):
    """
    Customized schema to treat depending fields
    """
    def _to_python(self, value_dict, state):
        if value_dict:
            for name in self.fields.keys():
                validator = self.fields[name]                
                if hasattr(validator, 'depend_field') and \
                   validator.depend_field:
                    fname, fvalue = validator.depend_field
                    if value_dict.has_key(fname) and \
                       value_dict[fname] != fvalue or \
                       not value_dict.has_key(fname):
                        if value_dict.has_key(name):
                            del value_dict[name]
                        del self.fields[name]
        return super(CdpcSchema, self)._to_python(value_dict, state)

