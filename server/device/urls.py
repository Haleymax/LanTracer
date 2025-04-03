from django.urls import path

from device import views

urlpatterns = [
    path('get_devices', views.get_device),
    path('add_device', views.add_device),
    path('get_menory', views.get_memory_info),
    path('del_device', views.delete_device),
    path('upd_device', views.update_device),
]