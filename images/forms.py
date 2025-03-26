from .models import Image, Comment, Category, Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django import forms


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'نام کاربری'}),
        error_messages={
            'required': 'لطفاً نام کاربری را وارد کنید.',
        }
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور'}),
        error_messages={
            'required': 'لطفاً رمز عبور را وارد کنید.',
        }
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                _("حساب کاربری شما غیرفعال است."),
                code='inactive',
            )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=200,
        help_text='الزامی است.',
        error_messages={
            'required': 'لطفاً ایمیل خود را وارد کنید.',
            'invalid': 'لطفاً یک ایمیل معتبر وارد کنید.',
        }
    )
    username = forms.CharField(
        error_messages={
            'required': 'لطفاً نام کاربری را وارد کنید.',
        }
    )
    password1 = forms.CharField(
        error_messages={
            'required': 'لطفاً رمز عبور را وارد کنید.',
        }
    )
    password2 = forms.CharField(
        error_messages={
            'required': 'لطفاً تکرار رمز عبور را وارد کنید.',
        }
    )

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

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise forms.ValidationError("وارد کردن عنوان اجباری است.")
        return title

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