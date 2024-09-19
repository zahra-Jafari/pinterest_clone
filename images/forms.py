from .models import Image, Comment, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile


class ImageForm(forms.ModelForm):
    new_category = forms.CharField(max_length=100, required=False, label='Add new category')
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Image
        fields = ['title', 'image', 'description', 'categories']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'image', 'categories']  # افزودن 'categories' به لیست فیلدها
        widgets = {
            'categories': forms.CheckboxSelectMultiple,  # نمایش دسته‌بندی‌ها به صورت چندگانه
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']
