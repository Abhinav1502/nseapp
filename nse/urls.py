from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('get_nsedata',views.get_nsedata,name='get_nsedata')
]
