from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, initial='')
    password = forms.CharField(max_length=32, widget=forms.PasswordInput, initial='')

class CreateForm(forms.Form):
    new_username = forms.CharField(max_length=30)
    new_password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    
class AddBookForm(forms.Form):
    ISBN = forms.CharField(max_length=10)