from django import forms
from hello.models import User, VinylRecord, Artist, Category, Manufacturer

class ProductForm(forms.ModelForm):
    class Meta:
        model = VinylRecord
        fields = ['title', 'artist', 'category', 'manufacturer', 'price', 'image_url']
        labels = {
            'title': 'Название',
            'artist': 'Исполнитель',
            'category': 'Категория',
            'manufacturer': 'Производитель',
            'price': 'Цена',
            'image_url': 'Ссылка на изображение',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите название пластинки'}),
            'image_url': forms.URLInput(attrs={'placeholder': 'Введите URL изображения'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artist'].queryset = Artist.objects.order_by('name')
        self.fields['category'].queryset = Category.objects.order_by('name')
        self.fields['manufacturer'].queryset = Manufacturer.objects.order_by('name')

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Подтвердите пароль")

    class Meta:
        model = User
        fields = ['login', 'name', 'surname', 'middle_name']
        labels = {
            'login': 'Логин',
            'name': 'Имя',
            'surname': 'Фамилия',
            'middle_name': 'Отчество',
        }
        widgets = {
            'login': forms.TextInput(attrs={'placeholder': 'Введите логин'}),
            'name': forms.TextInput(attrs={'placeholder': 'Введите имя'}),
            'surname': forms.TextInput(attrs={'placeholder': 'Введите фамилию'}),
            'middle_name': forms.TextInput(attrs={'placeholder': 'Введите отчество'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    login = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'placeholder': 'Введите логин'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))