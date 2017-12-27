from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^signup/$', views.signup),
    url(r'^all-categories/$', views.AllCategories),
    url(r'^category/$', views.get_category),
    url(r'^recent-orders/$', views.recent_orders),
    url(r'^get-product-category-wise/$', views.get_product_category_wise),
    url(r'^get-product/$', views.get_product),
]
