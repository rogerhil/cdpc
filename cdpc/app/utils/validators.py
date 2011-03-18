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


import re
from formencode import FancyValidator
from formencode.validators import _, Invalid, Email
#from formencode.interfaces import *
#from formencode.api import *

class CdpcEmail(Email):

    """
    Validates user in Cdpc Site
    >>> cpf = CdpcUser()
    """
    model = None
    valid_email = None
    strip = True
    _cpf_re = [re.compile(r"^(\d{3})[-_/\.\\ ]*(\d{3})[-_/\.\\ ]*(\d{3})[-_/\.\\ ]*(\d{2})$")]
    _store_format = "%s%s%s%s"
    messages = {'stringFormat': _('Invalid format.'),
                'alreadyExists': _('This e-mail already exists in ' \
                                   'database, please choose another e-mail address.')}
    def _to_python(self, value, state):
        self.assert_string(value, state)
        try:
            value = value.encode('ascii', 'replace')
        except:
            raise Invalid(self.message('stringFormat', state), value, state)
        clean_value = value.strip()

        user = self.model.query.filter_by(email=clean_value)
        alreadyExists = bool(user.count())

        if self.valid_email:
            alreadyExists = self.valid_email not in [u.email for u in user]
        
        if alreadyExists:
            raise Invalid(self.message('alreadyExists', state), value, state)
            
        return clean_value

class Cpf(FancyValidator):

    """
    Validates, and converts Cpf codes to ########### (11 charactes)
    >>> cpf = Cpf()
    >>> cpf.to_python("012.345.678-90")
    '01234567890'
    >>> cpf.to_python("012 345 678 90")
    '01234567890'
    >>> cpf.to_python("012_345_678_90")
    '01234567890'
    >>> cpf.to_python("012.345.678.90")
    '01234567890'
    >>> cpf.to_python("01234567890")
    '01234567890'
    >>> cpf.to_python(" 0 1 2 3 4 5 6 7 8 9 0 ")
    '01234567890'
    >>> cpf.to_python("012--345--678--90")
    '01234567890'
    >>> cpf.to_python("0.12.345.678-90")
    ...
    formencode.api.Invalid: Please enter a valid cep number in the format ###.###.###-##.
    >>> cpf.to_python("012.345.678-900")
    ...
    formencode.api.Invalid: Please enter a valid cep number in the format ###.###.###-##.
    >>> 
    """

    strip = True
    valid_cpf = None
    _cpf_re = [re.compile(r"^(\d{3})[-_/\.\\ ]*(\d{3})[-_/\.\\ ]*(\d{3})[-_/\.\\ ]*(\d{2})$")]
    _store_format = "%s%s%s%s"
    messages = {'cpfFormat': _('Please enter a valid cep number in the ' \
                               'format ###.###.###-##.'),
                'alreadyExists': _('This cpf already exists in ' \
                                   'database, please choose another one.')}
    def _to_python(self, value, state):
        from ..usuarios.models import Pessoa
        self.assert_string(value, state)
        try:
            value = value.encode('ascii', 'replace')
        except:
            raise Invalid(self.message('cpfFormat', state), value, state)
        clean_value = value.strip().replace(' ', '')
        cpf = None
        for regexp in self._cpf_re:
            match = regexp.match(clean_value)
            if match:
                cpf = self._store_format % match.groups()
                break
        if cpf:
            user = Pessoa.query.filter_by(cpf=cpf)
            alreadyExists = bool(user.count())
            if self.valid_cpf:
                alreadyExists = self.valid_cpf not in [u.cpf for u in user]
            if alreadyExists:
                raise Invalid(self.message('alreadyExists', state), value, state)
            return cpf
        raise Invalid(self.message('cpfFormat', state), value, state)

class BrazilPhoneNumber(FancyValidator):

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
    messages = {'phoneFormat': _('Please enter a number, with area code, in ' \
                                 'the form (##)########.'),
                'alreadyExists': _('This phone number already exists in ' \
                                   'database, please choose another one.')}

    def _to_python(self, value, state):
        from ..common.models import Telefone
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
        #    if Telefone.query.filter_by(numero=phone).count():
        #        raise Invalid(self.message('alreadyExists', state), value, state)
            return phone        
        raise Invalid(self.message('phoneFormat', state), value, state)

class Cep(FancyValidator):

    """
    Validates, and converts Cep numbers to ########

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
    _store_format = "%s%s%s"
    messages = {'cepFormat': _('Please enter a valid cep number ' \
                               'in the format #####-###.')}

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


class Dependent(FancyValidator):
    """
    """
    schema = None
    depend_field = None

    def to_python(self, value, state):
        self.schema.depend_field = self.depend_field
        return self.schema.to_python(value, state)

class AtLeastOne(FancyValidator):
    """
    """
    schema = None
    msg = None
    messages = {'errorMessage': _('Please mark at least one option')}

    def to_python(self, value, state):
        if isinstance(value, list):
            clean_value = [i for i in value if i.strip()]
        if isinstance(value, list) and len(clean_value) >= 1 or \
           ((isinstance(value, str) or isinstance(value, unicode)) and value):
            return self.schema.to_python(value, state)
        else:
            if self.msg:
                raise Invalid(self.msg, value, state)
            raise Invalid(self.message('errorMessage', state), value, state)


class NotEmptyList(FancyValidator):
    """
    """
    schema = None
    messages = {'errorMessage': _('Please enter a value')}

    def to_python(self, value, state):
        if not value:        
            raise Invalid(self.message('errorMessage', state), value, state)
        if isinstance(value, list):
            for cv in value:
                if not cv:
                    raise Invalid(self.message('errorMessage', state),
                                  value, state)
        return self.schema.to_python(value, state)

            
