from django.db import models
from django.urls import reverse
from shortuuid.django_fields import ShortUUIDField

# Create your models here.
class MyModelName(models.Model):
    myFieldName = models.CharField(max_length=20, help_text='Primeiro Nome')

    class Meta:
        ordering = ['myFieldName'] #ordenação dos dados por nome

    def get_absolute_url(self):
        """Retorna a url para acessar uma instancia específica de MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String para representar o objeto MyModelName (no site Admin)."""
        return self.myFieldName

class Genero(models.Model):
    """Modelo que representa o genero do livro."""
    nome = models.CharField(max_length=200, help_text='Digite o genero do livro (Ex: Ficção Científica)')

    def __str__(self):
        """String for representing the Model object."""
        return self.nome
    
class Book(models.Model):
    titulo = models.TextField('Titulo', max_length=200, help_text='Digite o título do livro')
    #tipo primitivo que permite estar vinculado a vários objetos
    #Com o 'on_delete=models.SET_NULL, null=True' conseguimos manter 
    #a integridade da referencia dos dados
    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True, help_text='Digite o autor do livro')
    resumo = models.TextField('Resumo', max_length=1000, help_text='Digite o resumo do livro')
    isbn = models.CharField('ISBN', max_length=13, help_text='Número ISBN do livro')
    #um genero pode ter mais de um livro
    #um livro pode ter mais de um genero
    genero = models.ManyToManyField(Genero, help_text='Digite o gênero do livro')
    def display_genero(self):
        return ', '.join(genero.nome for genero in self.genero.all()[:3])
    display_genero.short_descrition = "Gênero"

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        """Retorna a url para acessar os detalhes gravados na instancia da classe Book"""
        return reverse('detalhe-do-livro', args=[str(self.id)])

class BookInstance(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    id = ShortUUIDField(
        length=5,
        max_length=8,
        prefix="id_",
        alphabet="abcdefg1234",
        primary_key=True,
    )
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, help_text='')
    dataDeDevolucao = models.DateField(null=False, blank=True)

    imprint = models.CharField(max_length=300, null=True)

    LOAN_STATUS=(
        ('m', 'Em manutenção'),
        ('e', 'Emprestado'),
        ('d', 'Disponível'),
        ('r', 'Reservado'), 
    )

    status = models.CharField(
        max_length=1,
        choices = LOAN_STATUS,
        blank=True,
        default='m',
        help_text = 'Disponibilidade do livro', 
    )

    class Meta:
        ordering = ['dataDeDevolucao']

    def __str__(self):
        #string que representa uma instancia do modelo
        return f'{self.id} ({self.book.titulo})'

class Autor(models.Model):
    nome = models.CharField('Nome', max_length=100)
    sobrenome = models.CharField('Sobrenome', max_length=100)
    #blank=True indica que o campo pode ficar em branco
    dataDeNascimento = models.DateField('Data de Nascimento',null=True, blank=True)
    dataDeMorte = models.DateField('Data de Morte',null=True, blank=True)
    # outros campos e métodos
    class Meta:
        ordering = ['sobrenome', 'nome'] #ordenação dos dados por sobrenome e nome do autor

    def get_absolute_url(self):
        """Retorna a url para acessar os detalhes gravados na instancia da classe Book"""
        return reverse('informações-do-autor', args=[str(self.id)])

    def __str__(self):
        return '{}, {}'.format(self.sobrenome, self.nome)


