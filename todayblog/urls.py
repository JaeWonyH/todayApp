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
    # http://localhost:8000/todayblog/freepost/5/edit
    path('freepost/<int:pk>/edit/', views.post_edit, name='free_post_edit'),
    # http://localhost:8000/todayblog/freepost/5/remove
    path('freepost/<int:pk>/remove/', views.post_remove, name='free_post_remove'),
    # http://localhost:8000/todayblog/freepost/5/comment
    path('freepost/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    # http://localhost:8000/todayblog/freepost/5/comment/3/approve
    path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    # http://localhost:8000/todayblog/freepost/5/comment/3/approve
    path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
    #http://localhost:8000/todayblog/covid_check
    path('covid_check/',views.covid_post_list, name = 'covid_post_list' ),


]