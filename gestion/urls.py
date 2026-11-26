from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),

    # CRUD Películas
    path('peliculas/', views.lista_peliculas, name='lista_peliculas'),
    path('peliculas/nueva/', views.crear_pelicula, name='crear_pelicula'),
    path('peliculas/editar/<int:pk>/', views.editar_pelicula, name='editar_pelicula'),
    path('peliculas/eliminar/<int:pk>/', views.eliminar_pelicula, name='eliminar_pelicula'),

    # CRUD Categorías
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),
]