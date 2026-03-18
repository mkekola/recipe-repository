from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import connection
from django.http import Http404
from django.utils import timezone
from .forms import RecipeForm, UserRegistrationForm
from .models import Recipe, LoginAttempt
from datetime import timedelta



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
    recipe = get_object_or_404(Recipe, id=recipe_id) #FLAW 1: No access control check for private recipes

    #Fix: private recipes should only be visible to their owner
    #if recipe.is_private and recipe.owner != request.user:
        #raise Http404("Recipe not found")
    
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id) #FLAW 1: No access control check for editing another user's recipe

    #Fix: only allow editing if the current user is the owner
    #if recipe.owner != request.user:
        #raise Http404("Recipe not found")

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
    recipe = get_object_or_404(Recipe, id=recipe_id) #FLAW 1: No access control check for deleting another user's recipe

    #Fix: only allow deletion if the current user is the owner
    #if recipe.owner != request.user:
        #raise Http404("Recipe not found")

    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})

def search(request):
    q = request.GET.get('q', '')
    results = []

    if q:
        # FLAW 2: SQL query is built directly from user input
        query = f"SELECT * FROM recipes_recipe WHERE title LIKE '%{q}%' AND is_private = 0"

        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        for row in rows:
            row_dict = dict(zip(columns, row))
            results.append(Recipe(**row_dict))

        # FIX: use Django ORM instead of dynamic raw SQL
        # results = Recipe.objects.filter(title__icontains=q, is_private=False)

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

# FLAW 3: This view is intentionally designed to crash for testing purposes. In production, it should be removed or protected to prevent abuse.
def crash_test(request):
    return 1 / 0 

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #FLAW 4: No rate limiting or account lockout mechanism, making it vulnerable to brute-force attacks.
        user = authenticate(request, username=username, password=password)

        #FIX: block login attempts after too many failures
        #ip_address = request.META.get('REMOTE_ADDR')
        #attempt, _ = LoginAttempt.objects.get_or_create(username=username, ip_address=ip_address, defaults={'failed_attempts': 0})
        #if attempt.locked_until and attempt.locked_until > timezone.now():
            #messages.error(request, 'Account locked due to too many failed login attempts. Try again later.')
            #return render(request, 'registration/login.html')

        if user is not None:
            login(request, user)

            #FIX: reset failed login attempts on successful login
            #if 'attempt' in locals():
                #attempt.failed_attempts = 0
                #attempt.locked_until = None
                #attempt.save()

            return redirect('recipe_list')
        else:
            messages.error(request, 'Invalid username or password')

            #FIX: increment failed login attempts
            #if 'attempt' in locals():
                #attempt.failed_attempts += 1
                #if attempt.failed_attempts >= 4:
                    #attempt.locked_until = timezone.now() + timedelta(minutes=5)
                #attempt.save()

    return render(request, 'registration/login.html')

def custom_logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('recipe_list')
