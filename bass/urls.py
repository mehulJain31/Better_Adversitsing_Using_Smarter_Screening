from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='bass-home'),
    path('about/', views.about, name='bass-about'),
    path('recommend/',views.recommend,name='bass-recommend')
]