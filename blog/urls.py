from django.urls import path
from .views import (
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('custom/', views.custom_order, name='item-custom'),
    path('home/', views.land_home, name='land-home'),
    path('tag/<str:tagname>/', views.home_filter, name='blog-home-filter'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('item/<int:pk>/buy/', views.buy_page, name='item-buy'),
    path('item/mine', views.my_items, name='items-bought'),
]
