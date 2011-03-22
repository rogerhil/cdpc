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

from elixir import session
from hashlib import sha1

from ..common import models as common_models
from ..utils.filestorage import save_image
from ..utils.model import get_or_create
from . import models
from cdpc.app.common.cadastro import *

def set_senha(usuario, password):
    usuario.senha = sha1(password).hexdigest()

def set_values_pessoa(usuario, validado):
    # Instanciando o modelo e associando os campos validados e
    # transformados em valores python à instância que será
    # salva no db.

    usuario.ip_addr = validado['remote_addr']

    # -- Dados de acesso
    usuario.email = validado['email']
    if validado.get('senha'):
        set_senha(usuario, validado['senha'])

    # -- Dados pessoais
    usuario.nome = validado['nome']
    usuario.cpf = validado['cpf']
    usuario.data_nascimento = validado['data_nascimento']
    usuario.sexo = validado['sexo']

    # -- Sobre a sua localização geográfica
    endereco = get_or_create(common_models.Endereco,
        cep=validado['end_cep'],
        uf=validado['end_uf'],
        cidade=validado['end_cidade'],
        bairro=validado['end_bairro'],
        logradouro=validado['end_logradouro'],
        numero=validado['end_numero'],
        complemento=validado['end_complemento'],
        latitude=validado['end_latitude'],
        longitude=validado['end_longitude'])[0]
    
    usuario.endereco = endereco

    # -- Contatos e espaços na rede
    usuario.website = validado['website']
    
    usuario.telefones = []
    for i, num in enumerate(validado['pessoa_tel']):
        tel = get_or_create(common_models.Telefone, numero=num,
                            tipo=validado['pessoa_tel_tipo'][i])[0]
        usuario.telefones.append(tel)
    
    usuario.redes_sociais = []
    if validado.has_key('rs_nome'):
        for i in range(len(validado['rs_nome'])):
            rsocial = get_or_create(common_models.RedeSocial,
                                    nome=validado['rs_nome'][i],
                                    link=validado['rs_link'][i])[0]
            usuario.redes_sociais.append(rsocial)
            
    usuario.feeds = []
    if validado.has_key('feed_nome'):
        for i in range(len(validado['feed_nome'])):
            feed = get_or_create(common_models.Feed,
                                 nome = validado['feed_nome'][i],
                                 link = validado['feed_link'][i])[0]
            usuario.feeds.append(feed)

    try:
        session.commit()
    except Exception, e:
        session.rollback()
        raise e

    if validado['avatar']:
        save_image(validado['avatar'].stream, usuario.id, 'pessoa')
        
    return usuario


def values_dict(pessoa):

    values = {}
    dynamic_values = {}

    values['email'] = pessoa.email    
    values['nome'] = pessoa.nome
    values['cpf'] = pessoa.cpf
    values['data_nascimento'] = pessoa.data_nascimento.strftime('%d/%m/%Y')
    values['sexo'] = pessoa.sexo

    dynamic_values['pessoa_tel'] = map(lambda x: x.numero, pessoa.telefones)
    dynamic_values['pessoa_tel_tipo'] = map(lambda x: x.tipo, pessoa.telefones)
    
    values['end_cep'] = pessoa.endereco.cep
    values['end_logradouro'] = pessoa.endereco.logradouro
    values['end_numero'] = pessoa.endereco.numero
    values['end_complemento'] = pessoa.endereco.complemento
    values['end_bairro'] = pessoa.endereco.bairro
    values['end_cidade'] = pessoa.endereco.cidade
    values['end_uf'] = pessoa.endereco.uf

    values['website'] = pessoa.website

    dynamic_values['rs_nome'] = map(lambda x: x.nome, pessoa.redes_sociais)
    dynamic_values['rs_link'] = map(lambda x: x.link, pessoa.redes_sociais)
        
    dynamic_values['feed_nome'] = map(lambda x: x.nome, pessoa.feeds)
    dynamic_values['feed_link'] = map(lambda x: x.link, pessoa.feeds)
    
    return values, dynamic_values


