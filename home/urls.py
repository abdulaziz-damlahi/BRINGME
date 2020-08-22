from django.urls import path
from . import views

urlpatterns = [
    path('home', views.index, name='index'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),

]
