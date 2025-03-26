from django.shortcuts import render, redirect, get_object_or_404
from .models import Image, Like, Comment, Cart, Category, UserProfile, Profile
from .forms import ImageForm, CommentForm, CategoryForm, SignUpForm, UserProfileForm, CustomLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.messages import get_messages
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.db.models import Q
from django.http import HttpResponse
from PIL import Image as PILImage
from images import models
import os


def low_quality_image_view(request, image_id):
    image_obj = Image.objects.get(id=image_id)

    img = PILImage.open(image_obj.image.path)
    img = img.convert("RGB")
    img.thumbnail((300, 300))

    response = HttpResponse(content_type="image/jpeg")
    img.save(response, "JPEG", quality=60)
    return response


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        if "delete_picture" in request.POST:
            if profile.profile_picture:

                if os.path.exists(profile.profile_picture.path):
                    os.remove(profile.profile_picture.path)
                profile.profile_picture = None
                profile.save()
            return redirect('profile')

        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'profile': profile})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "ورود با موفقیت انجام شد.")
            return redirect('image_list')
        else:
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")

    storage = get_messages(request)
    for message in storage:
        print(message)  # پیام‌ها را بررسی کنید

    form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})


def image_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    images = Image.objects.all()

    if query:
        images = images.filter(
            Q(title__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct()

    if category_id:
        images = images.filter(categories__id=category_id)

    categories = Category.objects.all()
    return render(request, 'image_list.html', {'images': images, 'categories': categories})


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


@login_required
def image_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            form.save_m2m()

            new_category_name = form.cleaned_data.get('new_category')
            if new_category_name:
                new_category, created = Category.objects.get_or_create(name=new_category_name)
                image.categories.add(new_category)

            return redirect('success')
    else:
        form = ImageForm()
    return render(request, 'upload.html', {'form': form})


def success_view(request):
    return render(request, 'success.html')


def image_detail(request, id):
    image = get_object_or_404(Image, id=id)
    categories = image.categories.all()
    if request.method == 'POST' and 'like' in request.POST:
        Like.objects.get_or_create(image=image, user=request.user)
        return redirect('image_detail', id=image.id)

    if request.method == 'POST' and 'comment' in request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.image = image
            comment.user = request.user
            comment.save()
            return redirect('image_detail', id=image.id)
    else:
        comment_form = CommentForm()

    return render(request, 'images/image_detail.html', {'image': image, 'comment_form': comment_form, 'categories': categories})


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})


def add_to_cart(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.images.add(image)
    return redirect('cart')


@login_required
def remove_from_cart(request, image_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    image = get_object_or_404(Image, id=image_id)
    cart.images.remove(image)
    return redirect('cart')


def custom_logout_view(request):
    logout(request)
    return redirect('image_list')


def image_like(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    Like.objects.get_or_create(image=image, user=request.user)
    return redirect('image_detail', image_id=image.id)


def help_page(request):
    return render(request, 'help.html')  # این فایل HTML صفحه راهنما است
