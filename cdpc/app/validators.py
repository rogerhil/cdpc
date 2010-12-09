# -*- coding: utf-8; Mode: Python -*-
#
# Copyright (C) 2010  Lincoln de Sousa <lincoln@comum.org>
# Copyright (C) 2010  Ministério da Cultura <http://cultura.gov.br>
# Copyright (C) 2010  Marco Túlio Gontijo e Silva <marcot@marcot.eti.br>
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

import formencode, re
from formencode import validators
from formencode.validators import _, Invalid

from formencode.interfaces import *
from formencode.api import *
from formencode.schema import format_compound_error


class CpfValidator(formencode.FancyValidator):
    def _to_python(self, value, state):
        # Tratando o tamanho mínimo do cpf
        if len(value) != 11:
            raise formencode.Invalid(u'Cpf inválido', value, state)

        # tratando os valores óbvios
        if value in [str(i) * 11 for i in range(10)]:
            raise formencode.Invalid(u'Cpf inválido', value, state)

        # transformando o cpf num int
        cpf = map(int, value)

        # gerando os dois últimos dígitos do cpf
        newval = cpf[:9]
        while len(newval) < 11:
            new_item =  \
                [(len(newval)+1-x)*y for x, y in enumerate(newval)]
            result = sum(new_item) % 11
            if result > 1:
                newval.append(11 - result)
            else:
                newval.append(0)

        # Comparando o cpf informado pelo usuário com o gerado pela
        # bagunça acima
        if newval != cpf:
            raise formencode.Invalid(u'Cpf inválido', value, state)
        return value

class BrazilPhoneNumber(formencode.FancyValidator):

    """
    Validates, and converts phone numbers to ##-########
    Adapted from formencode.validators.national.InternationPhoneNumber

    ::

        >>> valid = BrazilPhoneNumber()
        >>> valid.to_python("(31) 12345678")
        '3112345678'
        >>> valid.to_python("(31) 1234 5678")
        '3112345678'
        >>> valid.to_python("(31) 1234-5678")
        '3112345678'
        >>> valid.to_python("(31) 1234.5678")
        '3112345678'
        >>> valid.to_python("(31)-1234.5678")
        '3112345678'
        >>> valid.to_python("(31).1234.5678")
        '3112345678'
        >>> valid.to_python(" ( 31 ) . 1234 . 5678 ")
        '3112345678'
        >>> valid.to_python(" 31  - 1234 . 5678 ")
        '3112345678'
        >>> valid.to_python("3112345678")
        '3112345678'
        >>> valid.to_python("31-1234.5678a")
            ...
        formencode.api.Invalid: Please enter a number, with area code, in the form (##)########.
        >>> valid.to_python("31-12349.5678")
            ...
        formencode.api.Invalid: Please enter a number, with area code, in the form (##)########.

    """

    strip = True
    _br_phone_re = [re.compile(r"^\s*\(\s*(\d{2})\s*\)[\s\.\-/_|]*(\d{4})[\s\.\-/_|]*(\d{4})\s*$"),
                   re.compile(r"^\s*(\d{2})[\s\.\-/_|]*(\d{4})[\s\.\-/_|]*(\d{4})\s*$")]
    _store_format = "%s%s%s"
    messages = {
        'phoneFormat': _('Please enter a number, with area code, in the form (##)########.'),
        'alreadyExists': _('This phone number already exists in database, please choose another one.')
        }


    def _to_python(self, value, state):
        from models import Telefone
        phone = ""
        self.assert_string(value, state)
        try:
            value = value.encode('ascii', 'replace')
        except:
            raise Invalid(self.message('phoneFormat', state), value, state)
        clean_value = value.strip().replace(' ', '')
        for regexp in self._br_phone_re:
            match = regexp.match(clean_value)
            if match:
                phone = self._store_format % match.groups()
                break
        if phone:
            if Telefone.query.filter_by(numero=phone).count():
                raise Invalid(self.message('alreadyExists', state), value, state)
            return phone        
        raise Invalid(self.message('phoneFormat', state), value, state)

class Cep(formencode.FancyValidator):

    """
    Validates, and converts Cep numbers to ########
    Adapted from formencode.validators.national.InternationPhoneNumber

    >>> valid = Cep()
    >>> valid.to_python("12345-678")
    '12345-678'
    >>> valid.to_python("12345678")
    '12345-678'
    >>> valid.to_python("12345 678")
    '12345-678'
    >>> valid.to_python("12345_678")
    '12345-678'
    >>> valid.to_python("12345/678")
    '12345-678'
    >>> valid.to_python("12 345-678")
    '12345-678'
    >>> valid.to_python(" 12345 - - - 678 ")
    '12345-678'
    >>> valid.to_python("12345-6789")
        ...
    formencode.api.Invalid: Please enter a valid cep number in the format #####-###.
    >>> valid.to_python("12 3459-678")
        ...
    formencode.api.Invalid: Please enter a valid cep number in the format #####-###.
    >>> 
    """

    strip = True
    _cep_re = [re.compile(r"^(\d{2})[-_/\.\\ ]*(\d{3})[-_/\.\\ ]*(\d{3})$")]
    _store_format = "%s-%s-%s"
    messages = {
        'cepFormat': _('Please enter a valid cep number in the format #####-###.')
        }


    def _to_python(self, value, state):
        self.assert_string(value, state)
        try:
            value = value.encode('ascii', 'replace')
        except:
            raise Invalid(self.message('cepFormat', state), value, state)
        clean_value = value.strip().replace(' ', '')
        for regexp in self._cep_re:
            match = regexp.match(clean_value)
            if match:
                return self._store_format % match.groups()
        raise Invalid(self.message('cepFormat', state), value, state)


class Dependent(formencode.FancyValidator):
    schema = None
    depend_field = None

    def to_python(self, value, state):
        self.schema.depend_field = self.depend_field
        return self.schema.to_python(value, state)

class AtLeastOne(formencode.FancyValidator):
    schema = None
    msg = None
    messages = {
        'errorMessage': _('Please mark at least one option'),
        }
    def to_python(self, value, state):
        print "####"
        print value
        print "####"
        if isinstance(value, list):
            clean_value = [i for i in value if i.strip()]
        if isinstance(value, list) and len(clean_value) >= 1 or \
           ((isinstance(value, str) or isinstance(value, unicode)) and value):
            return self.schema.to_python(value, state)
        else:
            if self.msg:
                raise Invalid(self.msg, value, state)
            raise Invalid(self.message('errorMessage', state), value, state)


class NotEmptyList(formencode.FancyValidator):
    schema = None
    messages = {
        'errorMessage': _('Please enter a value'),
        }
    def to_python(self, value, state):
        if not value:        
            raise Invalid(self.message('errorMessage', state), value, state)
        if isinstance(value, list):
            for cv in value:
                if not cv:
                    raise Invalid(self.message('errorMessage', state), value, state)
        return self.schema.to_python(value, state)

            
