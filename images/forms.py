from .models import Image, Comment, Category, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']


class ImageForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    new_category = forms.CharField(
        max_length=255,
        required=False,
        label="New Category",
        widget=forms.TextInput(attrs={'placeholder': 'Enter new category'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.all()

    class Meta:
        model = Image
        fields = ['title', 'image', 'description', 'price', 'categories', 'new_category']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'نظر شما',  # متن دلخواه برای لیبل
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple,
        }