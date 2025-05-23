from django.shortcuts import get_object_or_404
from api.serializers import ProsuctSerialzer,OrderSerializer,ProductInfoSerializer,OrderCreateSerializer
from api.models import Product,Order,OrderItem
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.db.models import Max
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    AllowAny
)
from rest_framework.views import APIView
from api.filters import ProductFilter, InStockFilterBackend, OrderFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.decorators import action
# Create your views here.


# class productListView(generics.ListAPIView):
#     queryset=Product.objects.all()
#     serializer_class=ProsuctSerialzer

# class ProductCreateAPIView(generics.CreateAPIView):
#     model=Product
#     serializer_class=ProsuctSerialzer    

class ProductListCreateAPIView(generics.ListCreateAPIView):  # we combine the top both into one get and post
    queryset=Product.objects.all()
    serializer_class=ProsuctSerialzer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter, InStockFilterBackend]
    filterset_fields = ("name", "price")
    pagination_class = PageNumberPagination
    pagination_class.page_size = 3
    pagination_class.page_size_query_param = 'size'
    pagination_class.page_query_param = "pageNum"
    pagination_class.max_page_size = 10

    search_fields = ['=name', 'description']
    ordering_fileds = ['name', 'price', 'stock']

    def get_permissions(self):
        self.permission_classes=[AllowAny]
        if self.request.method=='POST':
            self.permission_classes=[IsAdminUser]
        return super().get_permissions()
    
class productFilterView(generics.ListAPIView):
    queryset=Product.objects.filter(price__lt=20)
    serializer_class=ProsuctSerialzer

# @api_view(['GET'])

# def product_list(request):
#     products=Product.objects.all()
#     serializer=ProsuctSerialzer(products, many=True)
#     # return JsonResponse(serializer.data,safe=False)
#     return Response(serializer.data)

class productRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProsuctSerialzer
    lookup_url_kwarg='productId'

    def get_permissions(self):
        self.permission_classes=[AllowAny]
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes=[IsAdminUser]
        return super().get_permissions()

# @api_view(['GET'])

# def product_detail(request, pk):
#     product=get_object_or_404(Product, pk=pk)
#     serializer=ProsuctSerialzer(product)
#     return Response(serializer.data)

class orderListView(generics.ListAPIView):
    queryset=Order.objects.prefetch_related('items__product')
    serializer_class=OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs               

    # @action(
    #     detail = False,
    #     methods = ['get'],
    #     url_path = 'user-orders',
    # )

    # def user_orders(self, respect):
    #     orders = self.get_queryset().filter(user = request.user)
    #     serializer = self.get_serializer(orders, many=True)
    #     return Response(serializer.data)

# class UserOrderListAPIView(generics.ListAPIView):
#     queryset=Order.objects.prefetch_related('items__product')
#     serializer_class=OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         user=self.request.user
#         qs=super().get_queryset()
#         return qs.filter(user=user)

# @api_view(['GET'])

# def order_list(request):
#     orders=Order.objects.prefetch_related('items__product')
#     serializer=OrderSerializer(orders,many=True)
#     return Response(serializer.data)


@api_view(['GET'])

def product_info(request):
    products=Product.objects.all()
    serializer=ProductInfoSerializer({
        'products':products,
        'count':len(products),
        'max_price':products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)
