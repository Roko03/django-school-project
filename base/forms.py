from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm


from .models import Korisnik, Predmet, Upis

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Korisnik
        fields = ('username', 'email', 'password1','password2', 'role','status')

    ROLES = (('prof', 'profesor'), ('stu', 'student'),('adm', 'admin'))
    STATUS = (('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student'))
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Unesi korisnicko ime',
        'class': 'singup_input'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Unesi email korisnika',
        'class': 'singup_input'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Unesi sifru korisnika',
        'class': 'singup_input'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Potvrdi sifru',
        'class': 'singup_input'
    }))
    role = forms.ChoiceField(choices=ROLES)
    status = forms.ChoiceField(choices=STATUS)

class SignupForm(UserCreationForm):
    class Meta:
        model = Korisnik
        fields = ('username', 'email', 'password1', 'password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your username',
        'class': 'singup_input'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your email',
        'class': 'singup_input'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        'class': 'singup_input'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm your password',
        'class': 'singup_input'
    }))

class LoginForm(AuthenticationForm):
    class Meta:
        model = Korisnik
        fields = ('email','password')
    
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your email',
        'class': 'singup_input'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password',
        'class': 'login_input'
    }))

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Predmet
        fields = ('ime','kod','program','bodovi','sem_redovni','sem_izvanredni','izborni','korisnik_id')


    IZBORNI = (('DA', 'da'), ('NE', 'ne'))

    ime = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Unesi naziv predmeta',
        'class': 'subject_input'
    }))
    kod = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Unesi kod predmeta',
        'class': 'subject_input'
    }))
    program = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Unesi program predmeta',
        'class': 'subject_input'
    }))
    bodovi = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Unesi broj bodova',
        'class': 'subject_input'
    }))
    sem_redovni = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Unesi broj godine za redovne studente',
        'class': 'subject_input'
    }))
    sem_izvanredni = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': 'Unesi broj godine za izvanredne studente',
        'class': 'subject_input'
    }))
    izborni = forms.ChoiceField(choices=IZBORNI)
    korisnik_id = forms.ModelChoiceField(queryset=Korisnik.objects.filter(role='prof'))

class StudentForm(forms.ModelForm):
    class Meta:
        model = Korisnik
        fields = ('username', 'email', 'status')
    
    STATUS = (('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student'))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Unesi ime studenta',
        'class': 'subject_input'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Unesi email studenta',
        'class': 'subject_input'
    }))
    status = forms.ChoiceField(choices=STATUS)


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Korisnik
        fields = ('username', 'email')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Unesi ime profesora',
        'class': 'subject_input'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Unesi email profesora',
        'class': 'subject_input'
    }))

class ProfessorStudentForm(forms.ModelForm):
    class Meta:
        model = Upis
        fields = ('status',)

    STATUS = (('izg', 'Izgubljen potpis'), ('potne', 'Potpisan, nije položen'),('pol', 'Položen'))
    status = forms.ChoiceField(choices=STATUS)
