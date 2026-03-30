from django.urls import path
from products import views

urlpatterns = [
    # Product CRUD
    path("products/", views.product_list, name="product-list"),
    path("products/<int:pk>/", views.product_detail, name="product-detail"),

    # Stock alerts
    path("products/low-stock/", views.low_stock, name="low-stock"),
    path("products/high-stock/", views.high_stock, name="high-stock"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
]
