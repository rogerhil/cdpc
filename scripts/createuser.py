# -*- coding: utf-8; Mode: Python -*-

import sys
sys.path.insert(0, '..')
from optparse import OptionParser

from cdpc.app.usuarios import schemas
from cdpc.app.usuarios import models
from cdpc.app.usuarios.cadastro import *
from cdpc.main import setup_models

from shortcuts import *

setup_models()

print schemas.Usuario

password = lambda : 'alabama'
    
base = [('email', randemail),
        ('nome', randword),
        ('senha', password),
        ('confirmar_senha', password),
        ('avatar', ''),
        ('cpf', randcpf),
        ('data_nascimento', randdata),
        ('sexo', randsexo),
        ('pessoa_tel', randtellist),

        ('end_cep', ''),
        ('end_complemento', ''),
        ('end_numero', ''),
        ('end_cidade', ''),
        ('end_bairro', ''),
        ('end_logradouro', ''),
        ('end_uf', ''),
        ('end_longitude', ''),
        ('end_latitude', ''),

        ('website', randurl),

        ('rss', randredesociallist),
        ('feeds', randredesociallist),
]

def generate_data(email=None):
    data = {}
    endfilled = False

    for key, value in base:
        if key.startswith('end_'):
            if endfilled:
                continue
            cep = randcep()
            print cep
            d = get_cep(cep)
            data['end_cep'] = [d['cep']]
            data['end_logradouro'] = [d['rua']]
            data['end_bairro'] = [d['bairro']]
            data['end_cidade'] = [d['cidade']]
            data['end_uf'] = [d['uf']]
            data['end_numero'] = [randnum()]
            data['end_complemento'] = [randcompl()]
            data['end_latitude'] = [randnum()]
            data['end_longitude'] = [randnum()]
                            
            endfilled = True
            continue


        result = extract_value(value, data, key)
        if result and key == 'pessoa_tel':
            data[key] = []
            data[key + '_tipo'] = []
            for item in result:
                tel, tipo = item
                data[key].append(tel)
                data[key + '_tipo'].append(tipo)
            continue
        if key in ['feeds', 'rss']:
            data[key[:-1] + '_nome'] = []
            data[key[:-1] + '_link'] = []
            for item in result:
                nome, link = item
                data[key[:-1] + '_nome'].append(nome)
                data[key[:-1] + '_link'].append(link)
            continue
        data[key] = result
    if email:
        data['email'] = [email]
        data['nome'] = [email.split('@')[0]]
    return data            

def validate_and_create(data):
    # instanciando o validador
    validator = schemas.Usuario()
    validado = {}
    try:
        data = dict(data)
        data = prepare_data(data, schemas.Usuario.fields)
        validado = validator.to_python(data)
        print "!"*40
        print "OK! "*10
        print "!"*40
    except Exception, e:
        print "-"*20
        print e
        print "-"*20
    else:
        pessoa = models.Pessoa()
        validado['remote_addr'] = 'n/a'
        pessoa = set_values_pessoa(pessoa, validado)
        print
        print 'Pessoa "%s" cadastrada com sucesso' % pessoa.email
        print

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-n", "--npessoas", dest="n", help=u"Número de pessoas a serem geradas < 20")
    parser.add_option("-e", "--email", dest="e", help=u"Cria usuário específico")
    options, args = parser.parse_args()

    if not options.e and not options.n:
        print
        print "Número de pessoas a serem geradas não foi especificado. Use -n #."
        print
        exit(1)
    if not options.e and not options.n.isdigit():
        print
        print "Número de pessoas precisa ser um número inteiro."
        print
        exit(2)

    if not options.e and int(options.n) > 20:
        print
        print "Número de pessoas muito grande, forneca um valor < 20."
        print
        exit(3)

    print "Gerando..."
    if not options.e:
        n = int(options.n)
        for i in xrange(n):
            data = generate_data()
            validate_and_create(data)
    else:
        if options.e.find('@') != -1:
            data = generate_data(options.e)
            validate_and_create(data)
