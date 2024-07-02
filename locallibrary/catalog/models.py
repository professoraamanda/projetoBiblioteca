from django.db import models
from django.urls import reverse
import uuid

# Create your models here.
class MyModelName(models.Model):
    myFieldName = models.CharField(max_length=20, help_text='Primeiro Nome')

class Meta:
    ordering = ['-myFieldName'] #ordenação dos dados por nome

    def get_absolute_url(self):
        """Retorna a url para acessar uma instancia específica de MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String para representar o objeto MyModelName (no site Admin)."""
        return self.myFieldName

class Genre(models.Model):
    """Modelo que representa o genero do livro."""
    name = models.CharField(max_length=200, help_text='Digite o genero do livro (Ex: Ficção Científica)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
class Book(models.Model):
    titulo = models.TextField('Titulo', max_length=200, help_text='Digite o título do livro')
    #tipo primitivo que permite estar vinculado a vários objetos
    autor = models.ForeignKey('Autor', null=False, help_text='Digite o autor do livro')
    resumo = models.TextField('Resumo', max_length=1000, help_text='Digite o resumo do livro')
    isbn = models.CharField('ISBN', max_length=13, help_text='Número ISBN do livro')
    #um genero pode ter mais de um livro
    #um livro pode ter mais de um genero
    genero = models.ManyToManyField(Genre, help_text='Digite o gênero do livro')

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        """Retorna a url para acessar os detalhes gravados na instancia da classe Book"""
        return reverse('detalhe-do-livro', args=[str(self.id)])

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    book = models.ForeignKey('Book', null=False, help_text='')
    dataDeDevolucao = models.DateField(null=False, blank=True)

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
        ordering = ['-dataDeDevolucao']

    def __str__(self):
        #string que representa uma instancia do modelo
        return f'{self.id} ({self.book.titulo})'



