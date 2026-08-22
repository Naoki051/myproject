# apps/home/forms.py
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import transaction, models
from apps.core.models import Pessoa


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='E-mail ou CPF',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu E-mail ou CPF'
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sua senha'
        })
    )

    def clean(self):
        identificador = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if identificador and password:
            # Limpa formatação caso o usuário digite CPF com pontos/traço
            identificador_limpo = identificador.strip().replace('.', '').replace('-', '').replace('/', '')

            # Tenta encontrar por documento (CPF/CNPJ) ou pelo e-mail
            pessoa = Pessoa.objects.filter(
                models.Q(documento=identificador_limpo) | 
                models.Q(documento=identificador) | 
                models.Q(email=identificador)
            ).first()

            username_auth = identificador
            if pessoa and pessoa.user:
                username_auth = pessoa.user.username

            # Realiza a autenticação padrão do Django
            self.user_cache = authenticate(
                self.request,
                username=username_auth,
                password=password
            )

            if self.user_cache is None:
                raise forms.ValidationError(
                    'E-mail/CPF ou senha incorretos.',
                    code='invalid_login'
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class SignUpForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
        label='Senha'
    )
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a senha'}),
        label='Confirmar Senha'
    )

    class Meta:
        model = Pessoa
        fields = ['nome_completo', 'documento', 'email', 'telefone', 'senha', 'descricao']
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Completo'}),
            'documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF/CNPJ'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações'}),
        }

    field_order = [
        'nome_completo',
        'documento',
        'email',
        'telefone',
        'senha',
        'confirmar_senha',
        'descricao',
    ]

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')

        if senha and confirmar_senha and senha != confirmar_senha:
            self.add_error('confirmar_senha', 'As senhas não coincidem.')

        return cleaned_data

    def save(self, commit=True):
        with transaction.atomic():
            pessoa = super().save(commit=False)
            raw_password = self.cleaned_data['senha']

            user = User.objects.create_user(
                username=pessoa.email,
                email=pessoa.email,
                password=raw_password,
                first_name=pessoa.nome_completo.split()[0] if pessoa.nome_completo else ''
            )
            pessoa.user = user
            pessoa.senha = make_password(raw_password)

            if commit:
                pessoa.save()
            return pessoa