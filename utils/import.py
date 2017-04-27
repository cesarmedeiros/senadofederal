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

from senadores.models import Parlamentar, Partido


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

		if Parlamentar.objects.filter(codigo_parlamentar=codigo_parlamentar):
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
			print('Criado - %s' % parlamentarobj.nome)

print('Criando/atualizando listagem de partidos')
create_or_update_partido()

print('Criando/atualizando listagem de parlamentares')
create_or_update_parlamentar()