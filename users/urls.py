from django.urls import path
from .views import user_detail

urlpatterns = [
    path('<int:pk>/', user_detail, name='user-profile'),
]
