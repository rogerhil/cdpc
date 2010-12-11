from random import randint as r

simnao = lambda : r(1,2) and 'sim' or 'nao'

latin = """
Pri Putent Antiopam Convenire An Putent Erroribus Vel Dicunt Democritum Vel
No At Erat Utroque Aliquyam Qui Ad Sea Euismod Inermis Intellegebat Id Mel
Nonummy Electram Doctus Labitur Ponderum Id Pri Eos Vidit Quodsi Accumsan Ea
Per Omnes Aeterno Minimum In Nibh Duis Reformidans Sea Eu Dico Legimus Ex Ius
""".strip().split(' ')

ceps = """
78956000 78994000 20511330 78993000 20530350 78968000 13092150 78994800
13506555 78973000 20511170 78993000 13500000 13500110 20521110 13506555
13500000 13092150 78931000 20511170 78994800 13500313 78990000 78967800
""".strip().split(' ')

randword = lambda : unicode(latin[r(0, len(latin)-1)])
randtext = lambda : unicode(" ".join([randword() for i \
                                      in r(5,20)]).capitalize() + ".")
randnum = lambda: unicode(r(1,5000))
randcompl = lambda: unicode("ap %s" % r(1,999))
randcep = lambda : unicode(ceps[r(0, len(ceps)-1)])

base = {'endereco_ent_proj': u'sim',    
        'participa_cultura_viva': u'nao',
        'rs_link': '',
        'sede_possui_net': u'nao',
        'ind_populacao': None,
        'nome_ent': randword,
        'ind_oficinas': None,
        'documentacoes': None,
        'rs_nome': '',
        'feed_nome': '',
        'pq_sem_internet': u'opcao',
        'end_proj_cep': randcep,
        'end_proj_complemento': randcompl,
        'end_proj_longitude': '',
        'end_proj_numero': randnum,
        'end_proj_cidade': '',
        'end_proj_latitude': '',
        'end_proj_bairro': '',
        'end_proj_logradouro': '',
        'end_proj_uf': '',
        'atividade': [randword],
        'pq_sem_tel': u'opcao',
        'sede_possui_tel': u'nao',
        'nome': u'Projeto',
        'culturas_tradicionais': [],
        'publico_alvo': [],
        'numero_convenio': randnum,
        'ind_expectadores': None,
        'descricao': randtext,
        'genero': [],
        'local_proj': randword,
        'website_ent': None,
        'feed_link': '',
        'ocupacao_do_meio': [],
        'ent_tel': [],
        'tipo_convenio': randword,
        'estabeleceu_parcerias': u'nao',
        'convenio_ent': u'nao',
        'avatar': None,
        'email_ent': '',
        'manifestacoes_linguagens': [],
        'tipo': u'iniciativa_premiada'}

def extract_value(value):
    if hasattr(value, '__call__'):
        return value()
    elif isinstance(value, list):
        [extract_value(i) for i in value]
    else:
        return value    

cep = randcep()
base['end_proj_cep'] = cep
data = {}

for key, value in base.items():
    
    if key.startswith('end_proj_'):
        
        continue
    data[key] = extract_value(value)
    
    
print data
