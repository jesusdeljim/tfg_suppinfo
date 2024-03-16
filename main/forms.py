from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    email = forms.EmailField()
    nombre = forms.CharField(max_length=255, required=False)
    fecha_nacimiento = forms.DateField(required=False, widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    direccion = forms.CharField(max_length=255, required=False)
    ciudad = forms.CharField(max_length=255, required=False)
    pais = forms.CharField(max_length=255, required=False)
    codigo_postal = forms.CharField(max_length=20, required=False)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'nombre', 'fecha_nacimiento', 'direccion', 'ciudad', 'pais', 'codigo_postal', 'password1', 'password2']

class InicioSesionForm(AuthenticationForm):
    class Meta:
        model = Usuario  # Usa el modelo de usuario personalizado
        fields = ['username', 'password']