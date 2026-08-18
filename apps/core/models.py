from django.db import models
from django.contrib.auth.models import User

class Pessoa(models.Model):
    class StatusPessoa(models.TextChoices):
        ATIVO = 'ativo', 'Ativo'
        INATIVO = 'inativo', 'Inativo'
        AFASTADO = 'afastado', 'Afastado'
        EXPULSO = 'expulso', 'Expulso'

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, db_column='user_id')
    nome_completo = models.CharField(max_length=150)
    documento = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    senha = models.CharField(max_length=128)
    status = models.CharField(max_length=20, choices=StatusPessoa.choices, default=StatusPessoa.ATIVO)
    descricao = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome_completo

    class Meta:
        db_table = 'pessoa'


class PessoaCalouro(models.Model):
    class StatusCalouro(models.TextChoices):
        EM_PROCESSO = 'em processo', 'Em Processo'
        MEMBRO = 'membro', 'Membro'

    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, db_column='fk_pessoa', related_name='calouros')
    status = models.CharField(max_length=20, choices=StatusCalouro.choices, default=StatusCalouro.EM_PROCESSO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Calouro: {self.pessoa.nome_completo}"

    class Meta:
        db_table = 'pessoa_calouro'


class Departamento(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'departamento'


class GrupoTrabalho(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    abreviacao = models.CharField(max_length=20, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'grupo_trabalho'


class Comissao(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    abreviacao = models.CharField(max_length=20, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'comissao'


class Comite(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    abreviacao = models.CharField(max_length=20, unique=True)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'comite'


class PessoaMembro(models.Model):
    class StatusMembro(models.TextChoices):
        ATIVO = 'ativo', 'Ativo'
        ENCERRADO = 'encerrado', 'Encerrado'

    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, db_column='fk_pessoa', related_name='membros')
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, db_column='fk_departamento', related_name='membros')
    status = models.CharField(max_length=20, choices=StatusMembro.choices, default=StatusMembro.ATIVO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Membro: {self.pessoa.nome_completo} - {self.departamento.nome}"

    class Meta:
        db_table = 'pessoa_membro'


class PessoaComissao(models.Model):
    class StatusPessoaComissao(models.TextChoices):
        ATIVO = 'ativo', 'Ativo'
        ENCERRADO = 'encerrado', 'Encerrado'
        AFASTADO = 'afastado', 'Afastado'

    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, db_column='fk_pessoa', related_name='comissoes_pessoa')
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, db_column='fk_departamento', related_name='comissoes_pessoa')
    comissao = models.ForeignKey(Comissao, on_delete=models.CASCADE, db_column='fk_comissao', related_name='pessoas')
    status = models.CharField(max_length=20, choices=StatusPessoaComissao.choices, default=StatusPessoaComissao.ATIVO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pessoa.nome_completo} - {self.comissao.nome}"

    class Meta:
        db_table = 'pessoa_comissao'


class PessoaComite(models.Model):
    class StatusPessoaComite(models.TextChoices):
        ATIVO = 'ativo', 'Ativo'
        ENCERRADO = 'encerrado', 'Encerrado'

    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, db_column='fk_pessoa', related_name='comites_pessoa')
    comite = models.ForeignKey(Comite, on_delete=models.CASCADE, db_column='fk_comite', related_name='pessoas')
    presidente = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True, db_column='fk_presidente', related_name='comites_presididos')
    status = models.CharField(max_length=20, choices=StatusPessoaComite.choices, default=StatusPessoaComite.ATIVO)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pessoa.nome_completo} - {self.comite.nome}"

    class Meta:
        db_table = 'pessoa_comite'


class PessoaCoordenacao(models.Model):
    presidente = models.ForeignKey(Pessoa, on_delete=models.CASCADE, db_column='fk_presidente', related_name='coordenacoes_presididas')
    vice1 = models.ForeignKey(Pessoa, on_delete=models.CASCADE, db_column='fk_vice1', related_name='coordenacoes_vice1')
    vice2 = models.ForeignKey(Pessoa, on_delete=models.CASCADE, db_column='fk_vice2', related_name='coordenacoes_vice2')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Coordenacao ({self.start_at.year})"

    class Meta:
        db_table = 'pessoa_coordenacao'