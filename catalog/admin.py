from django.contrib import admin
from .models import Autor, Genero, Book, BookInstance

# Register your models here.
#admin.site.register(Autor)
#admin.site.register(Genre)
#admin.site.register(Book)
#admin.site.register(BookInstance)

class AutorAdmin(admin.ModelAdmin):
    list_display = ('sobrenome', 'nome', 'dataDeNascimento', 'dataDeMorte')
    fields = ['nome', 'sobrenome', ('dataDeNascimento', 'dataDeMorte')]

#registrar o modelo admin com a classe associada
admin.site.register(Autor, AutorAdmin)

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    pass

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'display_genero')
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'dataDeDevolucao')
    fieldsets = ( (None, {
        'fields': ('book', 'imprint', 'id')}),
    ('Disponível', {
        'fields': ('status', 'dataDeDevolucao')}), 
    )