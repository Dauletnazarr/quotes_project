from django.urls import path
from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.random_quote, name='random'),
    path('add/', views.add_quote, name='add'),
    path('top/', views.top_quotes, name='top'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<int:pk>/like/', views.like_quote, name='like'),
    path('<int:pk>/dislike/', views.dislike_quote, name='dislike'),
]
