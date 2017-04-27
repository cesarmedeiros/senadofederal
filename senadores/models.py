from django.db import models

# Create your models here.

class Partido(models.Model):
	nome = models.CharField('Nome do Partido'
		, max_length = 100)
	
	sigla = models.CharField('Sigla'
		, max_length = 10)

	data_criacao = models.DateField('Data de Criação'
		, null = True)

	codigo = models.CharField('Código do Partido'
		, max_length = 6)

	def __str__(self):
		return self.nome

	def get_or_create(sigla, nome="", data_criacao="", codigo=""):
		partido = Partido.objects.filter(sigla=sigla)
		if partido:
			partido = partido[0]
		else:
			if nome == '':
				nome = sigla
			partido = Partido()
			partido.sigla = sigla
			partido.nome = nome
			partido.data_criacao = data_criacao
			partido.codigo = codigo
			partido.save()
		return partido

	class Meta:
		ordering = ('sigla', )
		app_label = 'senadores'



class Parlamentar(models.Model):

	SEXO_CHOICE = (
			('F', 'Feminino'),
			('M', 'Masculino')
		)
	
	codigo_parlamentar = models.CharField('Código do Parlamentar'
		, max_length = 10)

	nome = models.CharField('Nome Político'
		, max_length = 45
		, null = True)

	nome_completo = models.CharField('Nome Completo do Parlamentar'
		, max_length = 45)

	uf = models.CharField('UF do Estado que foi eleito'
		, max_length = 2)

	partido = models.ForeignKey(Partido)

	forma_tratamento = models.CharField('Forma de Tratamento'
		, max_length = 15)

	sexo = models.CharField(choices = SEXO_CHOICE
		, max_length = 1)

	email = models.EmailField(null=True)

	foto_url = models.URLField('URL para foto do Parlamentar')

	pagina_url = models.URLField('Endereço da Página do Parlamentar')


	def __str__(self):
		return self.codigo_parlamentar

	class Meta:
		app_label = 'senadores'


class Legislatura(models.Model):

	codigo = models.CharField('Código da Legislatura'
		, max_length = 6
		, unique = True)

	data_inicio = models.DateField('Data de início da Legislatura')
	
	data_fim = models.DateField('Data de fim da Legislatura')

	def __str__(self):
		return "{} - {}".format(self.data_inicio, self.data_fim)

	def get_or_create(codigo, data_inicio, data_fim):
		legislatura = Legislatura.objects.filter(codigo=codigo)

		if legislatura:
			legislatura = legislatura[0]
		else:
			legislatura = Legislatura()
			legislatura.codigo = codigo
			legislatura.data_inicio = data_inicio
			legislatura.data_fim = data_fim
			legislatura.save()

		return legislatura

	class Meta:
		app_label = 'senadores'


class Mandato(models.Model):

	parlamentar = models.ForeignKey(Parlamentar)

	codigo_mandato = models.CharField('Código do Mandato'
		, max_length = 6)

	uf = models.CharField('UF do Estado ao qual o mandato é vinculado'
		, max_length = 2)

	participacao = models.CharField('O tipo de participação'
		, max_length = 20)

	primeira_legislatura = models.ForeignKey(Legislatura, related_name='primeira')

	segunda_legislatura = models.ForeignKey(Legislatura, related_name='segunda')

	class Meta:
		app_label = 'senadores'


class Afastamento(models.Model):
	sigla = models.CharField('Sigla do Motivo do Afastamento'
		, unique = True
		, max_length = 6)

	descricao = models.CharField('Descrição do Afastamento'
		, max_length = 200)

	def __str__(self):
		return self.sigla

	def get_or_create(sigla, descricao):
		if len(sigla)==0:
			return None
		else:
			afastamento = Afastamento.objects.filter(sigla=sigla)
			
			if afastamento:
				afastamento = afastamento[0]
			else:
				afastamento = Afastamento(sigla=sigla, descricao=descricao)
				afastamento.save()
		
			return afastamento

	class Meta:
		ordering = ('sigla', )
		app_label = 'senadores'


class Exercicio(models.Model):
	mandato = models.ForeignKey(Mandato)

	codigo = models.CharField('Código'
		, max_length = 6)

	data_inicio = models.DateField('Data do início do Exercício')

	data_fim = models.DateField('Data do fim do exercício'
		, null = True
		, blank = True)

	afastamento = models.ForeignKey(Afastamento
		, null = True
		, blank = True) 

	class Meta:
		ordering = ('mandato', 'data_inicio', )
		app_label = 'senadores'


class MandatoSuplentes(models.Model):
	mandato = models.ForeignKey(Mandato)

	suplente = models.ForeignKey(Parlamentar)

	descricao = models.CharField('Descrição da participação',
		max_length = 50)

	def __str__(self):
		return "{} {} de {} ".format(self.suplente, self.descricao, self.mandato.parlamentar)

	class Meta:
		ordering = ('mandato', 'suplente', )
		app_label = 'senadores'
