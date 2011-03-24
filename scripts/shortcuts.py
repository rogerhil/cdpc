# -*- coding: utf-8; Mode: Python -*-

import sys
sys.path.insert(0, '..')
from random import randint as r
from urllib import urlopen

from cdpc.app.projetos.cadastro import *
from cdpc.app.usuarios.cadastro import *

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
randuf = lambda : randchoice(VALORES_UF)
randcpf = lambda: unicode(r(1,99999999999)).zfill(11)
randdata = lambda: u"%s/%s/%s" % (unicode(r(1,28)).zfill(2), unicode(r(1,12)).zfill(2), unicode(r(1930,2005)))
randsexo = lambda : r(0,1) and 'masculino' or 'feminino'

randlist = lambda x: x[r(0, len(x)-1)]

def get_cep(cep):
    """
    """
    try:
        page = urlopen(CONSULTA_CEP % cep)
        content = page.read().decode('iso-8859-1')
        rua, bairro, cidade, _, ufraw = content.split('||', 4)
    except:
        cep = '88888888'
        rua, bairro, cidade, ufraw = randword(), randword(), randword(), randuf()
    return {'rua': rua, 'bairro': bairro, 'cidade': cidade, 'uf': ufraw.replace('|', ''), 'cep': cep}
        
def extract_value(value, data, key):
    
    tolist = lambda x : isinstance(x, list) and x or [x]
    
    if hasattr(value, '__call__'):
        func = value
        try:
            return tolist(func())
        except:
            return tolist(func(globals()[key.upper()]))
    elif isinstance(value, tuple):
        func, cond, v = value
        if v in data[cond]:
            try:
                return tolist(func())
            except:
                return tolist(func(globals()[key.upper()]))
    else:
        return tolist(value)

