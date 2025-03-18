from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.contrib import admin
from . import views
from .views import custom_logout_view, login_view, profile_view, add_to_cart, view_cart, remove_from_cart, low_quality_image_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.image_list, name='image_list'),
    path('upload/', views.image_upload, name='image_upload'),
    path('success/', views.success_view, name='success'),
    path('<int:image_id>/', views.image_detail, name='image_detail'),
    path('<int:image_id>/like/', views.image_like, name='image_like'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', views.SignUpView.as_view(template_name='registration/signup.html'), name='signup'),
    path('logout/', custom_logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('image/<int:id>/', views.image_detail, name='image_detail'),
    path('cart/', view_cart, name='cart'),
    path('add_to_cart/<int:image_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:image_id>/', remove_from_cart, name='remove_from_cart'),
    path('low_quality/<int:image_id>/', low_quality_image_view, name='low_quality_image'),
]

