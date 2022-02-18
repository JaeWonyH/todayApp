from django.urls import path
from . import views

urlpatterns = [
    #http://localhost:8000/todayblog
    path('', views.post_list, name='post_list_home'),
    #http://localhost:8000/todayblog/freepost
    path('freepost/',views.free_post_list, name = 'free_post_list' ),
    # http://localhost:8000/todayblog/freepost/5
    path('freepost/<int:pk>', views.free_post_detail, name='free_post_detail'),
    # http://localhost:8000/todayblog/freepost/new
    path('freepost/new/', views.post_new, name='free_post_new'),


]