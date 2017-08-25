from django.conf.urls import url
from . import views

app_name = "ambiente"

urlpatterns = [
    url(r'^novo/$', views.novo_ambiente, name='novo'),
]
