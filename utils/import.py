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

from senadores.models import Parlamentar, Partido, Mandato, Legislatura


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


def create_or_update_parlamentar():
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
		print('   Mandato Criado')

print('Criando/atualizando listagem de partidos')
create_or_update_partido()

print('Criando/atualizando listagem de parlamentares')
create_or_update_parlamentar()