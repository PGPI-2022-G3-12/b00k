from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
#Aquí va todo lo que requiera un formulario

class ClientCreationForm(UserCreationForm):
    username = forms.CharField(
		max_length= 127,
		min_length=4,
		required=True,
		label="Usuario",
		widget=forms.TextInput(
				attrs={
					"placeholder": "Usuario",
					"class": "form-control"
				}
			)
	)

    first_name = forms.CharField(
		max_length=10,
		min_length=4,
		required=True,
		label="Nombre",
		widget=forms.TextInput(
				attrs={
					"placeholder": "Nombre",
					"class": "form-control"
				}
			)
		)
    last_name = forms.CharField(
		max_length=30,
		required=True,
		label="Apellidos",
		widget=forms.TextInput(
				attrs={
					"placeholder": "Apellidos",
					"class": "form-control"
				}
			)
		)
    email = forms.EmailField(
		max_length=254,
		widget=forms.EmailInput(
			attrs={
				"placeholder": "Email",
				"class": "form-control"
			}
		)
	)
    address = forms.CharField(
        max_length=254,
		label="Dirección",
        widget=forms.TextInput(
            attrs={
				"placeholder": "Dirección",
				"class": "form-control"
			}
        )
    )
    password1 = forms.CharField(
		label = "Contraseña",
		widget = forms.PasswordInput(
			attrs={
				"placeholder": "Contraseña",
				"class": "form-control"
			}
		)
	)
    password2 = forms.CharField(
		label = "Confirmación Contraseña",
		widget = forms.PasswordInput(
			attrs={
				"placeholder": "Contraseña",
				"class": "form-control"
			}
		)
	)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

class ClientLoginForm(AuthenticationForm):
	username = forms.CharField(
		max_length= 127,
		min_length=4,
		required=True,
		label="Usuario",
		widget=forms.TextInput(
				attrs={
					"placeholder": "Usuario",
					"class": "form-control"
				}
			)
	)
	password= forms.CharField(
		label = "Contraseña",
		widget = forms.PasswordInput(
			attrs={
				"placeholder": "Contraseña",
				"class": "form-control"
			}
		)
	)
	class Meta:
		model = User
		fields = ('username','password',)