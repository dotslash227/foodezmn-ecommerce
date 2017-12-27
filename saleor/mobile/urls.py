from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^signup/$', views.signup),
    url(r'^all-categories/$', views.AllCategories),
    url(r'^category/$', views.get_category),
]
