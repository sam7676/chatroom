from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat, name='chat'),
    path('chat/sendmsg/',views.sendmsg,name='sendmsg'),
    path('chat/sendcmd/',views.sendcmd,name='sendcmd'),
    path('chat/getchats/',views.getchats,name='getchats'),
    path('chat/getusers/',views.getusers,name='getusers'),
]