from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.user_login_view, name='login'),
    path('dashboard/', views.user_dashboard, name='dashboard'), 
    path('logout/', views.logout_view, name='logout'),
    path('generate_qr/', views.generate_ration_qr, name='generate_qr'),

    #shops-USER AUTH VIEWS
    path('shop_login/', views.shop_login_view, name='shop_login'),
    path('shop_dashboard/', views.shop_dashboard, name='shop_dashboard'),
]