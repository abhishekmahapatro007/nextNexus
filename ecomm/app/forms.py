from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User
from .models import Customer


class LoginForm(AuthenticationForm):
      username=UsernameField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
      password=forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))


     

class CustomerRegistrationForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
         model = User
         fields=['username','email','password1','password2']
class MyPasswordChangeForm (PasswordChangeForm):

    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs=
    {'autofocus':'True','autocomplete': 'current-password', 'class': 'form-control'}))
    new_password1 = forms.CharField(label='New Password', widget= forms.PasswordInput(attrs=
    {'autocomplete': 'current-password', 'class':'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget =forms.PasswordInput (attrs={'autocomplete':'current-password', 'class':'form-control'}))


class MyPasswordResetForm(PasswordResetForm):
     email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
     new_password1 = forms.CharField(label='New Password', widget= forms.PasswordInput(attrs=
     {'autocomplete': 'current-password', 'class':'form-control'}))
     new_password2 = forms.CharField(label='Confirm Password', widget =forms.PasswordInput (attrs={'autocomplete':'current-password', 'class':'form-control'}))


class CustomerProfileForm(forms.ModelForm):
     class Meta:
          model = Customer
          fields=['name', 'locality', 'city','mobile', 'state', 'zipcode']
          widgets={
               'name': forms.TextInput(attrs={'class':'form-control'}),
               'locality': forms.TextInput(attrs={'class':'form-control'}),
               'city': forms.TextInput(attrs={'class':'form-control'}),
               'mobile':forms.NumberInput(attrs={'class':'form-control'}),
               'state': forms.Select(attrs={'class':'form-control'}),
               'zipcode': forms.NumberInput(attrs={'class':'form-control'}),
               }
          



# forms.py
from django import forms
from .models import Animal

class StrayAnimalRescueForm(forms.ModelForm):
    animal_type_choices = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('cow', 'Cow'),
        ('bird', 'Bird'),
    ]

    name=forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    location = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}) )
    animal_type = forms.ChoiceField(choices=animal_type_choices,widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    mobile_number = forms.CharField(max_length=15,widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    email_address=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    animal_health_description = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    injury_description = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))

    class Meta:
        model = Animal
        fields = '__all__'







