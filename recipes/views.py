from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Recipe
from .forms import RecipeForm, UserRegistrationForm

def home(request):
    return redirect('recipe_list')

def recipe_list(request):
    recipes = Recipe.objects.filter(is_private=False).order_by('-created_at')
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'recipes/my_recipes.html', {'recipes': recipes})

@login_required
def recipe_create(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.owner = request.user
            recipe.save()
            return redirect('recipe_detail', recipe.id)
    else:
        form = RecipeForm()

    return render(request, 'recipes/recipe_form.html', {'form': form})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', recipe.id)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {'form': form})

@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})

def search(request):
    q = request.GET.get('q', '')
    results = Recipe.objects.filter(title__icontains=q, is_private=False)
    return render(request, 'recipes/search.html', {'results': results, 'q': q})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('recipe_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
