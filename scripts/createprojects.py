# -*- coding: utf-8; Mode: Python -*-

import sys
sys.path.insert(0, '..')
from random import randint as r
from urllib import urlopen
from optparse import OptionParser

from cdpc.app.projetos import schemas
from cdpc.app.usuarios.models import Pessoa
from cdpc.app.projetos.cadastro import *
from cdpc.main import setup_models

from shortcuts import *

setup_models()

latin = """
Lacus Laoreet Blandit Habitasse Elit Malesuada Est Litora Nunc Eros Hac Torquent
Tellus Consectetur Facilisi Sapien Metus Non Congue Nibh Tincidunt Bibendum Nisi
Consequat Condimentum Integer Odio Faucibus Ipsum Neque Mattis Nisl Nostra Curae
Viverra Augue Porta Lacinia Orci Ultricies Mi Auctor Sagittis Suscipit Sed
Sociosqu Vivamus Eu Et Sem Adipiscing Iaculis Diam Risus Nec Per Quisque Ligula
Molestie Mollis Himenaeos Elementum Hendrerit Aptent Velit Leo Inceptos Euismod
Magna Curabitur Maecenas Phasellus Amet Aenean Aliquam Vestibulum Eleifend Cras
Justo Libero Tempor Facilisis Nulla Placerat Proin Pharetra Ultrices Varius
Primis Purus Morbi Vel Venenatis Enim Ante Imperdiet Dui Praesent Quis Pretium
Interdum Fringilla Conubia Rhoncus Feugiat Luctus Lobortis Eget Vehicula Tempus
Taciti Scelerisque Ullamcorper Donec Suspendisse Accumsan Dapibus Tortor Ut
Sollicitudin Posuere Egestas Vulputate Volutpat Sodales Felis Ac Dictum Ad
Semper Cubilia Ornare Lectus Duis Erat At In Mauri Id Urna Nullam Mauris Sit
Platea Convallis Nam Etiam Massa Dignissim Vitae Pulvinar Arcu Commodo Gravida
Turpis Fusce Cursus Aliquet Lorem Class Porttitor Quam Dictumst Rutrum Tristique
Pellentesque Dolor Fermentum
""".strip()

latin = ' '.join(latin.splitlines()).split(' ')

#lista de ceps válidos (última atualizacão 15/12/2010)
ceps = """
20511330 20530350 13092150 13506555 20511170 20521110 13506555 30644300
30644400 31550300 31550500 30865100 30250100 30190100 30310100 30624100
30880100 60760100 04742100 83330100 57050100 71825100 08062100 70855100
85813300 19913100 57036180 03731170 77807190 14050000 91910170 74391400
54777120 37014760 59054470 75080730 26465320 01027020 26130130 82640470
52031060 07031150 58051840 89037500 45658330 03509010 75133760 29905220
38030030 03431030 23082160 38040310 05574170 41900290 03145010 74830380
40421640 82710430 04966150 40301460 06236030 05501000 23082140 75903070
05778270 30750030 60840110 02910090 14070180 65010530 11666290 21535590
25809610 04617020
""".strip()

ceps = ' '.join(ceps.splitlines()).split(' ')

urlsufixes = ['com', 'com.br', 'org', 'org.br', 'net', 'gov']

simnao = lambda : r(0,1) and 'sim' or 'nao'
randword = lambda : unicode(latin[r(0, len(latin)-1)])
randtext = lambda : unicode(" ".join([randword() for i in xrange(r(5,20))]).capitalize() + ".")
randnum = lambda: unicode(r(1,5000))
randcompl = lambda: unicode("ap %s" % r(1,999))
randcep = lambda : unicode(ceps[r(0, len(ceps)-1)])
randurlsufix = lambda : unicode(urlsufixes[r(0, len(urlsufixes)-1)])
randurl = lambda : "http://%s.%s" % (randword().lower(), randurlsufix())
randemail = lambda : "%s@%s.%s" % (randword().lower(), randword().lower(), randurlsufix())
randwordlist = lambda : [randword() for i in xrange(r(5,10))]
randurllist = lambda : [randurl() for i in xrange(r(5,10))]
randredesociallist = lambda : [(randword().capitalize(), randurl()) for i in xrange(r(5,10))]
randchoice = lambda X : X[r(0, len(X)-1)][0]
randchoices = lambda X : [X[i][0] for i in xrange(r(1, len(X)-1))]
randtel = lambda : (''.join([unicode(r(0,9)) for i in xrange(10)]), randchoice(TIPO_TEL_SEDE))
randtellist = lambda : [randtel() for i in xrange(5)]
randuf = lambda : randchoice(VALORES_UF)

randlist = lambda x: x[r(0, len(x)-1)]
    
base = [('nome', randword),
        ('descricao', randtext),
        ('tipo', randchoice),
        ('tipo_convenio', randchoice),
        ('numero_convenio', randnum),
        ('avatar', None),
        ('participa_cultura_viva', simnao),
        ('acao_cultura_viva', (randchoices, 'participa_cultura_viva', 'sim')),
        ('estabeleceu_parcerias', simnao),
        ('parcerias', (randchoices, 'estabeleceu_parcerias', 'sim')),


        ('local_proj', randchoice),
        ('end_proj_cep', ''),
        ('end_proj_complemento', ''),
        ('end_proj_numero', ''),
        ('end_proj_cidade', ''),
        ('end_proj_bairro', ''),
        ('end_proj_logradouro', ''),
        ('end_proj_uf', ''),
        ('end_proj_longitude', ''),
        ('end_proj_latitude', ''),

        ('nome_ent', randword),
        ('website_ent', randurl),
        ('email_ent', randemail),
        ('ent_tel', randtellist),
        ('convenio_ent', simnao),
        ('outro_convenio', (randwordlist, 'convenio_ent', 'sim')),
        ('endereco_ent_proj', simnao),

        ('end_ent_cep', randcep),
        ('end_ent_complemento', randcompl),
        ('end_ent_numero', randnum),
        ('end_ent_cidade', ''),
        ('end_ent_bairro', ''),
        ('end_ent_logradouro', ''),
        ('end_ent_uf', ''),
        ('end_ent_longitude', ''),
        ('end_ent_latitude', ''),

        ('email_proj', randemail),
        ('website_proj', randurl),
        ('sede_possui_tel', simnao),
        ('pq_sem_tel', (randchoice, 'sede_possui_tel', 'nao')),
        ('sede_tel', (randtellist, 'sede_possui_tel', 'sim')),
        ('sede_possui_net', simnao),
        ('pq_sem_internet', (randchoice, 'sede_possui_net', 'nao')),
        ('tipo_internet', (randchoice, 'sede_possui_net', 'sim')),
        ('rss', randredesociallist),
        ('feeds', randredesociallist),

        ('atividade', randchoices),

        ('publico_alvo', randchoices),
        ('culturas_tradicionais', randchoices),
        ('ocupacao_do_meio', randchoices),
        ('genero', randchoices),
        ('manifestacoes_linguagens', randchoices),
        ('documentacoes', None),
            
        ('ind_populacao', randnum),  
        ('ind_oficinas', randnum),
        ('ind_expectadores', randnum)]

def generate_data():
    data = {}
    endprojfilled = False
    endentfilled = False

    for key, value in base:

        if key.startswith('end_proj_'):
            if endprojfilled:
                continue
            cep = randcep()
            d = get_cep(cep)
            data['end_proj_cep'] = [d['cep']]
            data['end_proj_logradouro'] = [d['rua']]
            data['end_proj_bairro'] = [d['bairro']]
            data['end_proj_cidade'] = [d['cidade']]
            data['end_proj_uf'] = [d['uf']]
            data['end_proj_numero'] = [randnum()]
            data['end_proj_complemento'] = [randcompl()]
            data['end_proj_latitude'] = [randnum()]
            data['end_proj_longitude'] = [randnum()]


            if 'outros' in data['local_proj']:
                rang = range(r(1,5))
                data['end_outro_nome'] = []
                data['end_outro_cep'] = []
                data['end_outro_logradouro'] = []
                data['end_outro_bairro'] = []
                data['end_outro_cidade'] = []
                data['end_outro_uf'] = []
                data['end_outro_numero'] = []
                data['end_outro_complemento'] = []
                data['end_outro_latitude'] = []
                data['end_outro_longitude'] = []
                            
                for i in rang:
                    cep = randcep()
                    d = get_cep(cep)
                    data['end_outro_nome'].append(randword())
                    data['end_outro_cep'].append(d['cep'])
                    data['end_outro_logradouro'].append(d['rua'])
                    data['end_outro_bairro'].append(d['bairro'])
                    data['end_outro_cidade'].append(d['cidade'])
                    data['end_outro_uf'].append(d['uf'])
                    data['end_outro_numero'].append(randnum())
                    data['end_outro_complemento'].append(randcompl())
                    data['end_outro_latitude'].append(randnum())
                    data['end_outro_longitude'].append(randnum())
                            
            endprojfilled = True
            continue

        if key.startswith('end_ent_'):
            if endentfilled:
                continue
            cep = randcep()
            d = get_cep(cep)
            data['end_ent_cep'] = [d['cep']]
            data['end_ent_logradouro'] = [d['rua']]
            data['end_ent_bairro'] = [d['bairro']]
            data['end_ent_cidade'] = [d['cidade']]
            data['end_ent_uf'] = [d['uf']]
            data['end_ent_numero'] = [dict(base)['end_ent_numero']()]
            data['end_ent_complemento'] = [dict(base)['end_ent_complemento']()]
            data['end_ent_latitude'] = ['']
            data['end_ent_longitude'] = ['']
            endentfilled = True
            continue

        result = extract_value(value, data, key)
        if result and key in ['sede_tel', 'ent_tel']:
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
    return data            

def validate_and_create(data, user):
    # instanciando o validador
    members = {}
    up = lambda x: members.update(x)
    map(up, [getattr(schemas.Projeto, class_name).fields for class_name in dir(schemas.Projeto) if not class_name.startswith("__")])
    class ProjetoSchema(schemas.CdpcSchema):
        pass

    for key, v in members.items():
        setattr(ProjetoSchema, key, v)
    ProjetoSchema.fields.update(members)
    validator = ProjetoSchema()
    validado = {}
    try:
        data = dict(data)
        data = prepare_data(data, ProjetoSchema.fields)
        validado = validator.to_python(data)
    except Exception, e:
        print "-"*20
        print e
        print "-"*20
    else:
        projeto = cadastra_projeto(validado, user)
        print
        print 'Projeto "%s" cadastrado com sucesso' % projeto.nome
        print

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-n", "--nprojetos", dest="n", help=u"Número de projetos a serem gerados < 500")
    parser.add_option("-e", "--email", dest="email", help=u"E-mail do usuário dono do projeto")
    options, args = parser.parse_args()

    if not options.n:
        print
        print "Número de projetos a serem gerados não foi especificado. Use -n #."
        print
        exit(1)
    if not options.n.isdigit():
        print
        print "Número de projetos precisa ser um número inteiro."
        print
        exit(2)

    if int(options.n) > 500:
        print
        print "Número de projetos muito grande, forneca um valor < 500."
        print
        exit(3)
        
    if not options.email:
        print
        print "Email do usuário não especificado"
        print
        exit(4)        


    if options.email == 'RANDOMALL':
        users = Pessoa.query.all()
    else:
        try:
            users = [Pessoa.query.filter_by(email=u).one() \
                     for u in options.email.split(',')]
            
        except:
            print
            print "Usuário '%s' não encontrado." % options.email
            print
            exit(5)

    print "Gerando..."
    n = int(options.n)
    for i in xrange(n):
        data = generate_data()
        validate_and_create(data, randlist(users))

