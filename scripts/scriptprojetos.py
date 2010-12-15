# -*- coding: utf-8; Mode: Python -*-

from random import randint as r

latin = """
Pri Putent Antiopam Convenire An Putent Erroribus Vel Dicunt Democritum Vel
No At Erat Utroque Aliquyam Qui Ad Sea Euismod Inermis Intellegebat Id Mel
Nonummy Electram Doctus Labitur Ponderum Id Pri Eos Vidit Quodsi Accumsan Ea
Per Omnes Aeterno Minimum In Nibh Duis Reformidans Sea Eu Dico Legimus Ex Ius
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

TIPO = [(u'ponto', u'Ponto'),
        (u'pontao', u'Pontão'),
        (u'iniciativa_premiada', u'Iniciativa Premiada')]

TIPO_CONVENIO = [(u'internacional', u'Internacional'),
                 (u'federal', u'Federal'),
                 (u'estadual', u'Estadual'),
                 (u'municipal', u'Municipal')]

ACAO_CULTURA_VIVA = [(u'Agente Cultura Viva', u'Agente Cultura Viva'),
                     (u'Cultura Digital', u'Cultura Digital'),
                     (u'Cultura e Saúde', u'Cultura e Saúde'),
                     (u'Economia Viva', u'Economia Viva'),
                     (u'Escola Viva', u'Escola Viva'),
                     (u'Grios', u'Grios'),
                     (u'Interações Estéticas', u'Interações Estéticas'),
                     (u'Mídias Livres', u'Mídias Livres'),
                     (u'Pontinho de Cultura', u'Pontinho de Cultura'),
                     (u'Pontos de memória', u'Pontos de memória'),
                     (u'Redes Indígenas', u'Redes Indígenas'),
                     (u'Tuxaua', u'Tuxaua')]

PARCERIAS = [(u'Biblioteca', u'Biblioteca'),
             (u'Empresa', u'Empresa'),
             (u'Equipamento de Saúde', u'Equipamento de Saúde'),
             (u'Escola', u'Escola'),
             (u'Igreja', u'Igreja'),
             (u'ONG', u'ONG'),
             (u'Poder público', u'Poder público'),
             (u'Pontos de Memória', u'Pontos de Memória'),
             (u'Redes Indígenas', u'Redes Indígenas'),
             (u'Sistemas S', u'Sistemas S (Sesc, Senai, etc)'),
             (u'Tuxaua', u'Tuxaua')]

LOCAL_PROJ = [(u'sede', u'Sede'),
              (u'itinerante', u'Itinerante'),
              (u'outros', u'Outros locais')]

PQ_SEM_TEL = [(u'opcao', u'Opção'),
              (u'fornecimento', u'Não há fornecimento de serviços na região'),
              (u'recursos', u'Falta de recursos'),
              (u'outros', u'Outros')]

PQ_SEM_INTERNET = PQ_SEM_TEL

TIPO_TEL_SEDE = [(u'fixo', u'Fixo'),
                 (u'celular', u'Celular'),
                 (u'radio', u'Rádio'),
                 (u'rural', u'Rural'),
                 (u'publico', u'Público')]

TIPO_INTERNET = [(u'discada', u'Discada'),
                 (u'3g', u'3G'),
                 (u'adsl', u'ADSL/Cabo (Banda Larga)'),
                 (u'radio', u'Rádio'),
                 (u'gesac', u'Gesac'),
                 (u'public', u'Internet Pública')]

ATIVIDADE = [(u'Agente cultura viva', u'Agente Cultura Viva'),
             (u'Cultura digital', u'Cultura Digital'),
             (u'Cultura e saúde', u'Cultura e Saúde'),
             (u'Economia viva', u'Economia Viva'),
             (u'Escola viva', u'Escola Viva'),
             (u'Grios', u'Grios'),
             (u'Interacoes estéticas', u'Interações Estéticas'),
             (u'Mídias livres', u'Mídias Livres'),
             (u'Pontinho de cultura', u'Pontinho de Cultura'),
             (u'Pontos de memoria', u'Pontos de memória'),
             (u'Redes indígenas', u'Redes Indígenas'),
             (u'Tuxaua', u'Tuxaua')]

PUBLICO_ALVO = [(u'Criancas', u'Crianças'),
                (u'Adolescentes', u'Adolescentes'),
                (u'Adultos', u'Adultos'),
                (u'Jovens', u'Jovens')]
                
CULTURAS_TRADICIONAIS = [(u'Quilombola', u'Quilombola'),
                         (u'Pomerano', u'Pomerano'),
                         (u'Caiçara', u'Caiçara'),
                         (u'Indígena', u'Indígena'),
                         (u'Cigana', u'Cigana'),
                         (u'Ribeirinhos', u'Ribeirinhos'),
                         (u'Povos da floresta', u'Povos da Floresta')]


OCUPACAO_DO_MEIO = [(u'Rural', u'Rural'),
                    (u'Urbano', u'Urbano')]

GENERO = [(u'Mulheres', u'Mulheres'),
          (u'Homens', u'Homens'),
          (u'LGBT', u'LGBT')]

MANIFESTACOES_LINGUAGENS = [(u'Artes digitais', u'Artes digitais'),
                            (u'Artes plásticas', u'Artes plásticas'),
                            (u'Audiovisual', u'Audiovisual'),
                            (u'Circo', u'Circo'),
                            (u'Culinária', u'Culinária'),
                            (u'Dança', u'Dança'),
                            (u'Fotografia', u'Fotografia'),
                            (u'Grafite', u'Grafite'),
                            (u'Internet', u'Internet'),
                            (u'Jornalismo', u'Jornalismo'),
                            (u'Literatura', u'Literatura'),
                            (u'Música', u'Música'),
                            (u'Rádio', u'Rádio'),
                            (u'Teatro', u'Teatro'),
                            (u'Tecnologias digitais', u'Tecnologias digitais'),
                            (u'Tradição oral', u'Tradição oral'),
                            (u'TV', u'TV')]

simnao = lambda : r(0,1) and 'sim' or 'nao'
randword = lambda : unicode(latin[r(0, len(latin)-1)])
randtext = lambda : unicode(" ".join([randword() for i in xrange(r(5,20))]).capitalize() + ".")
randnum = lambda: unicode(r(1,5000))
randcompl = lambda: unicode("ap %s" % r(1,999))
randcep = lambda : unicode(ceps[r(0, len(ceps)-1)])
randurlsufix = lambda : unicode(urlsufixes[r(0, len(urlsufixes)-1)])
randurl = lambda : "http://%s.%s" % (randword().lower(), randurlsufix())
randemail = lambda : "%s@%s" % (randword().lower(), randurlsufix())
randwordlist = lambda : [randword() for i in xrange(r(5,10))]
randurllist = lambda : [randurl() for i in xrange(r(5,10))]
randredesociallist = lambda : [(randword().capitalize(), randurl()) for i in xrange(r(5,10))]
randtel = lambda : ''.join([unicode(r(0,9)) for i in xrange(10)])
randtellist = lambda : [randtel() for i in xrange(5)]
randchoices = lambda X : [i for i, j in X]
    
base = [('nome', randword),
        ('descricao', randtext),
        ('tipo', randchoices),
        ('tipo_convenio', randchoices),
        ('numero_convenio', randnum),
        ('avatar', None),
        ('participa_cultura_viva', simnao),
        ('acao_cultura_viva', (randchoices, 'participa_cultura_viva', 'sim')),
        ('estabeleceu_parcerias', simnao),
        ('parcerias', (randchoices, 'estabeleceu_parcerias', 'sim')),


        ('end_proj_cep', randcep),
        ('end_proj_complemento', randcompl),
        ('end_proj_numero', randnum),
        ('end_proj_cidade', ''),
        ('end_proj_bairro', ''),
        ('end_proj_logradouro', ''),
        ('end_proj_uf', ''),
        ('end_proj_longitude', ''),
        ('end_proj_latitude', ''),
        ('local_proj', randchoices),

        ('nome_ent', randword),
        ('website_ent', randurl),
        ('email_ent', randemail),
        ('ent_tel', randtellist),
        ('convenio_ent', simnao),
        ('outro_convenio', (randwordlist, 'convenio_ent', 'sim')),
        ('endereco_ent_proj', simnao),

        ('end_ent_cep', randcep),
        ('end_ent_complemento', randcompl),
        ('end_ent_numero', randnum()),
        ('end_ent_cidade', ''),
        ('end_ent_bairro', ''),
        ('end_ent_logradouro', ''),
        ('end_ent_uf', ''),
        ('end_ent_longitude', ''),
        ('end_ent_latitude', ''),

        ('sede_possui_tel', simnao),
        ('pq_sem_tel', (randchoices, 'sede_possui_tel', 'nao')),
        ('tipo_tel_sede', (randchoices, 'sede_possui_tel', 'sim')),
        ('sede_tel', (randtel, 'sede_possui_tel', 'sim')),
        ('sede_possui_net', simnao),
        ('pq_sem_internet', (randchoices, 'sede_possui_net', 'nao')),
        ('tipo_internet', (randchoices, 'sede_possui_net', 'sim')),
        ('redes', randredesociallist),
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




CONSULTA_CEP = 'http://viavirtual.com.br/webservicecep.php?cep=%s'
from urllib import urlopen

def get_cep(cep):
    """
    """
    try:
        page = urlopen(CONSULTA_CEP % cep)
        content = page.read().decode('iso-8859-1')
        rua, bairro, cidade, _, ufraw = content.split('||', 4)
    except:
        cep = '00000000'
        rua, bairro, cidade, ufraw = randword(), randword(), randword(), randword()
    return {'rua': rua, 'bairro': bairro, 'cidade': cidade, 'uf': ufraw.replace('|', ''), 'cep': cep}
        
def extract_value(value, data, key):
    if hasattr(value, '__call__'):
        func = value
        try:
            return func()
        except:
            return func(globals()[key.upper()])
    elif isinstance(value, tuple):
        func, cond, v = value
        if data[cond] == v:
            try:
                return func()
            except:
                return func(globals()[key.upper()])
    else:
        return value    

data = {}

endprojfilled = False
endentfilled = False

for key, value in base:

    if key.startswith('end_proj_'):
        if endprojfilled:
            continue
        data['end_proj_cep'] = []
        data['end_proj_logradouro'] = []
        data['end_proj_bairro'] = []
        data['end_proj_cidade'] = []
        data['end_proj_uf'] = []

        for i in xrange(r(1,5)):
            cep = randcep()
            d = get_cep(cep)
            data['end_proj_cep'].append(d['cep'])
            data['end_proj_logradouro'].append(d['rua'])
            data['end_proj_bairro'].append(d['bairro'])
            data['end_proj_cidade'].append(d['cidade'])
            data['end_proj_uf'].append(d['uf'])
        
        endprojfilled = True
        continue

    if key.startswith('end_ent_'):
        if endentfilled:
            continue
        cep = randcep()
        d = get_cep(cep)
        data['end_ent_cep'] = d['cep']
        data['end_ent_logradouro'] = d['rua']
        data['end_ent_bairro'] = d['bairro']
        data['end_ent_cidade'] = d['cidade']
        data['end_ent_uf'] = d['uf']
        endentfilled = True
        continue

    data[key] = extract_value(value, data, key)
    
    
for key, item in data.items():
    if not item:
        print key, item

print 
#for key, item in data.items():
#    if item:
#        print key, item
