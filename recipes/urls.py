from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('recipes/new/', views.recipe_create, name='recipe_create'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/<int:recipe_id>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipes/<int:recipe_id>/delete/', views.recipe_delete, name='recipe_delete'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
]