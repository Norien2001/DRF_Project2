
from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('products/',views.ProductListCreateAPIView.as_view()),     # here we combine the both into one
    # path('products/',views.productListView.as_view()),
    # path('products/create',views.productCretaeAPIView.asview()),
    path('products/<int:productId>/',views.productRetrieveView.as_view()),
    # path('orders/',views.orderListView.as_view()),
    path('products/info',views.product_info),
    path('products/stock',views.productFilterView.as_view()),
    # path('user-order/',views.UserOrderListAPIView.as_view()),
]

router = DefaultRouter()
router.register('orders', views.OrderViewSet)
urlpatterns += router.urls