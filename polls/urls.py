from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:poll_id>', views.detail, name='polls_detail')
]
