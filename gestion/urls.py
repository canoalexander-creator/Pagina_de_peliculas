from django.urls import path
from . import views


urlpatterns = [
    # Inicio y Autenticación
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', views.cerrar_sesion, name='logout'),


    # CRUD Películas
    path('peliculas/', views.lista_peliculas, name='lista_peliculas'),
    path('peliculas/crear/', views.crear_pelicula, name='crear_pelicula'),
    path('peliculas/editar/<int:pk>/', views.editar_pelicula, name='editar_pelicula'),
    path('peliculas/eliminar/<int:pk>/', views.eliminar_pelicula, name='eliminar_pelicula'),


    # CRUD Categorías
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),


    # CRUD Reseñas y Detalle de Película (Tarea 2)
    path('peliculas/<int:pk>/', views.detalle_pelicula, name='detalle_pelicula'),
    path('resenas/editar/<int:pk>/', views.editar_resena, name='editar_resena'),
    path('resenas/eliminar/<int:pk>/', views.eliminar_resena, name='eliminar_resena'),
]