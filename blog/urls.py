from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('qaiqai/', views.qaiqai, name='qaiqai'),
    path('beyonce/', views.beyonce, name='beyonce'),
    path('launch/', views.launch, name='launch'),
]
