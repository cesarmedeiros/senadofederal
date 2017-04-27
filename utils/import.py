import os, sys

import requests

import json


proj_path = "/Users/cesar/dev/ello/"
# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "senado.settings")
sys.path.append(proj_path)

# This is so my local_settings.py gets loaded.
os.chdir(proj_path)

# This is so models get loaded.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from senadores.models import Parlamentar, Partido, Mandato, Legislatura\
							, Exercicio, Afastamento, MandatoSuplentes


def get_from_url(url):
	headers = {'Accept' : 'application/json'}
	response_sen = requests.get(url, headers=headers)

	return response_sen.json()


def create_or_update_partido():
	url_senador_atual_partidos = "http://legis.senado.leg.br/dadosabertos/senador/partidos"
	partido_list_json = get_from_url(url_senador_atual_partidos)
	for partido in partido_list_json['ListaPartidos']['Partidos']['Partido']:
		partidoobj = Partido.get_or_create(partido['Sigla']
			, partido['Nome']
			, partido['DataCriacao']
			, partido['Codigo']
			)
		if partidoobj:
			print("Criado o partido %s - %s"%(partidoobj.sigla, partidoobj.nome))

def get_key_value(dicionario, key):
	if key in dicionario:
		return dicionario[key]
	else:
		return None

def create_or_update_parlamentar(codigo_parlamentar, uf_parlamentar):
	url = "http://legis.senado.leg.br/dadosabertos/senador/" + codigo_parlamentar
	parlamentarobj = Parlamentar.objects.filter(codigo_parlamentar=codigo_parlamentar)
	if parlamentarobj:
		parlamentarobj = parlamentarobj[0]
	else:
		parlamentar_list_json = get_from_url(url)

		dados = parlamentar_list_json['DetalheParlamentar']['Parlamentar']['IdentificacaoParlamentar']

		parlamentarobj = Parlamentar()
		parlamentarobj.codigo_parlamentar = codigo_parlamentar
		parlamentarobj.nome =  get_key_value(dados, 'NomeParlamentar') 
		parlamentarobj.nome_completo = dados['NomeCompletoParlamentar']
		parlamentarobj.forma_tratamento = dados['FormaTratamento'] 
		parlamentarobj.sexo = dados['SexoParlamentar'][0]
		parlamentarobj.email = ''
		key='UrlFotoParlamentar'
		value=""
		if key in dados.keys():
			value = dados[key]
		parlamentarobj.foto_url = value
		
		key='UrlPaginaParlamentar'
		value=""
		if key in dados.keys():
			value = dados[key]
		parlamentarobj.pagina_url = value
		#parlamentarobj.uf = parlamentar_list_json['DetalheParlamentar']['Parlamentar']['UltimoMandato']['UfParlamentar']
		parlamentarobj.uf = uf_parlamentar

		key='SiglaPartidoParlamentar'
		if key in dados.keys():
			value = dados['SiglaPartidoParlamentar']
		else:
			value = 'SEMPARTIDO'
		
		parlamentarobj.partido = Partido.get_or_create(value)

		parlamentarobj.save()

	return parlamentarobj


def create_or_update_parlamentares():
	url_senador_atual = "http://legis.senado.leg.br/dadosabertos/senador/lista/atual"
	parlamentar_list_json = get_from_url(url_senador_atual)

	for parlamentar in parlamentar_list_json['ListaParlamentarEmExercicio']['Parlamentares']['Parlamentar']:
		codigo_parlamentar = parlamentar['IdentificacaoParlamentar']['CodigoParlamentar']

		parlamentarobj = Parlamentar.objects.filter(codigo_parlamentar=codigo_parlamentar)
		if parlamentarobj:
			parlamentarobj = parlamentarobj[0]
			print(parlamentar['IdentificacaoParlamentar']['NomeParlamentar'])
		else:
			parlamentarobj = Parlamentar()
			parlamentarobj.codigo_parlamentar = codigo_parlamentar
			parlamentarobj.nome = parlamentar['IdentificacaoParlamentar']['NomeParlamentar'] 
			parlamentarobj.nome_completo = parlamentar['IdentificacaoParlamentar']['NomeCompletoParlamentar']
			parlamentarobj.forma_tratamento = parlamentar['IdentificacaoParlamentar']['FormaTratamento'] 
			parlamentarobj.sexo = parlamentar['IdentificacaoParlamentar']['SexoParlamentar'][0]
			parlamentarobj.email = parlamentar['IdentificacaoParlamentar']['EmailParlamentar']
			parlamentarobj.foto_url = parlamentar['IdentificacaoParlamentar']['UrlFotoParlamentar']
			parlamentarobj.pagina_url = parlamentar['IdentificacaoParlamentar']['UrlPaginaParlamentar']
			parlamentarobj.uf = parlamentar['IdentificacaoParlamentar']['UfParlamentar']
			parlamentarobj.partido = Partido.get_or_create(parlamentar['IdentificacaoParlamentar']['SiglaPartidoParlamentar'])
			parlamentarobj.save()


			print('Parlamentar Criado - %s' % parlamentarobj.nome)

		mandato = parlamentar['Mandato']
		mandatoobj = Mandato()
		mandatoobj.parlamentar = parlamentarobj;
		mandatoobj.codigo_mandato = mandato['CodigoMandato']
		mandatoobj.uf = mandato['UfParlamentar']
		mandatoobj.participacao = mandato['DescricaoParticipacao']
		primeira_legislaturaobj= Legislatura.get_or_create(mandato['PrimeiraLegislaturaDoMandato']['NumeroLegislatura']
											, mandato['PrimeiraLegislaturaDoMandato']['DataInicio']
											, mandato['PrimeiraLegislaturaDoMandato']['DataFim'])
		mandatoobj.primeira_legislatura = primeira_legislaturaobj

		segunda_legislaturaobj = Legislatura.get_or_create(mandato['SegundaLegislaturaDoMandato']['NumeroLegislatura']
											, mandato['SegundaLegislaturaDoMandato']['DataInicio']
											, mandato['SegundaLegislaturaDoMandato']['DataFim'])
		mandatoobj.segunda_legislatura = segunda_legislaturaobj
		mandatoobj.save()

		print('	Mandato Criado')

		exercicios = mandato['Exercicios']
		exercicios_list = []
		tipo = type(exercicios['Exercicio'])
		if tipo == dict:	
			exercicios_list.append(exercicios['Exercicio'])
		else:
			exercicios_list = exercicios['Exercicio']

		for exercicio in exercicios_list:
			data_fim=None
			sigla_afastamento=''
			descricao_afastamento=''
			key = 'DataFim' 
			if key in exercicio.keys():
				data_fim = exercicio['DataFim']
				key = 'SiglaCausaAfastamento'
				if key in exercicio.keys():
					sigla_afastamento = exercicio['SiglaCausaAfastamento']
					descricao_afastamento = exercicio['DescricaoCausaAfastamento']
			exercicioobj = Exercicio()
			exercicioobj.mandato = mandatoobj
			exercicioobj.codigo = exercicio['CodigoExercicio']
			exercicioobj.data_inicio = exercicio['DataInicio']
			exercicioobj.data_fim = data_fim
			exercicioobj.afastamento = Afastamento.get_or_create(sigla_afastamento, descricao_afastamento)
			exercicioobj.save()
			print('		Exercício criado')

		#Importação de suplentes

		suplentes = mandato['Suplentes']
		suplentes_list = []
		tipo = type(suplentes['Suplente'])
		if tipo == dict:	
			suplentes_list.append(suplentes['Suplente'])
		else:
			suplentes_list = suplentes['Suplente']

		for suplente in suplentes_list:
			suplenteobj = MandatoSuplentes()
			suplenteobj.descricao = suplente['DescricaoParticipacao']
			suplenteobj.mandato = mandatoobj
			suplenteobj.suplente = create_or_update_parlamentar(suplente['CodigoParlamentar'], mandatoobj.uf)
			suplenteobj.save()
			print('			Suplente %s criado'%suplenteobj.suplente)







print('Criando/atualizando listagem de partidos')
create_or_update_partido()

print('Criando/atualizando listagem de parlamentares')
create_or_update_parlamentares()