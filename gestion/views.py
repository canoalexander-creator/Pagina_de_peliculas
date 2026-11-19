from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pelicula, Categoria

# Vista protegida: solo usuarios autenticados pueden entrar
@login_required(login_url='login')
def inicio(request):
    peliculas = Pelicula.objects.select_related('categoria').all()
    categorias = Categoria.objects.all()
    return render(request, 'inicio.html', {
        'peliculas': peliculas,
        'categorias': categorias
    })

# 1. Registro de nuevos usuarios
def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'¡Cuenta creada con éxito para {usuario.username}! Ahora inicia sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registro.html', {'form': form})

# 2. Inicio de sesión
def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# 3. Cerrar sesión
def logout_usuario(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')