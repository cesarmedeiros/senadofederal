from django.db import models

# Create your models here.

class Partido(models.Model):
	nome = models.CharField('Nome do Partido'
		, max_length = 100)
	
	sigla = models.CharField('Sigla'
		, max_length = 10)

	def __str__(self):
		return self.nome

	class Meta:
		ordering = ('sigla', )



class Parlamentar(models.Model):

	SEXO_OPTIONS = (
			('F', 'Feminino'),
			('M', 'Masculino')
		)
	
	codigo_parlamentar = models.CharField('Código do Parlamentar'
		, max_length = 10)

	nome = models.CharField('Nome Político'
		, max_length = 45)

	nome_completo = models.CharField('Nome Completo do Parlamentar'
		, max_length = 45)

	uf = models.CharField('UF do Estado que foi eleito'
		, max_length = 2)

	partido = models.ForeignKey(Partido)

	forma_tratamento = models.CharField('Forma de Tratamento',
			, max_length = 15)

	sexo = models.CharField(options = SEXO_OPTIONS
		, max_length = 1)

	email = models.EmailField()

	foto_url = URLField('URL para foto do Parlamentar')

	pagina_url = URLField('Endereço da Página do Parlamentar')


	def __str__(self):
		return self.nome

class Legislatura(models.Model):
	data_inicio = models.DateField('Data de início da Legislatura')
	
	data_fim = models.DateField('Data de fim da Legislatura')

	def __str__(self):
		return "{} - {}".format(self.inicio, self.fim)

class Mandato(models.Model):
	codigo_mandato = models.CharField('Código do Mandato'
		, max_length = 6)

	uf = models.CharField('UF do Estado ao qual o mandato é vinculado'
		, max_length = 2)

	participacao = models.CharField('O tipo de participação'
		, max_length = 20)

	primeira_legislatura = models.ForeignKey(Legislatura)

	segunda_legislatura = models.ForeignKey(Legislatura)


class Afastamento(models.Model):
	sigla = models.CharField('Sigla do Motivo do Afastamento'
		, unique = True
		, max_length = 6)

	descricao = models.CharField('Descrição do Afastamento'
		, max_length = 200)

	def __str__(self):
		return self.sigla

	class Meta:
		ordering = ('sigla', )

class Exercicio(models.Model):
	mandato = models.ForeignKey(Mandato)

	codigo = models.CharField('Código'
		, max_length = 6)

	data_inicio = models.DateField('Data do início do Exercício')

	data_fim = models.DateField('Data do fim do exercício'
		, null = True
		, blank = True)

	afastamento = models.ForeignKey(Afastamento) 

	class Meta:
		ordering = ('mandato', 'data_inicio', )

