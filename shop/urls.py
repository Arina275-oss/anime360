# shop/urls.py
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('new/', views.new_arrivals, name='new_arrivals'),
    path('special-offers/', views.special_offers, name='special_offers'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail_alt'),
    path('promotions/', views.promotion_list, name='promotion_list'),
    path('promotions/<slug:slug>/', views.promotion_detail, name='promotion_detail'),
]