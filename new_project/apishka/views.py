from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from hello.models import User, Category, Manufacturer, Artist, VinylRecord, Order, Cart, CartItem, OrderDetail
from .serializers import (
    UserSerializer, CategorySerializer, ManufacturerSerializer, ArtistSerializer,
    VinylRecordSerializer, OrderSerializer, CartSerializer, CartItemSerializer,
    OrderDetailSerializer, CartItemAddSerializer, UserRegistrationSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = [AllowAny]

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [AllowAny]

class VinylRecordViewSet(viewsets.ModelViewSet):
    queryset = VinylRecord.objects.all()
    serializer_class = VinylRecordSerializer
    permission_classes = [AllowAny]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        cart = self.get_object()
        serializer = CartItemAddSerializer(data=request.data)
        if serializer.is_valid():
            vinyl_id = serializer.validated_data['vinyl_id']
            quantity = serializer.validated_data['quantity']
            vinyl = get_object_or_404(VinylRecord, id=vinyl_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, vinyl=vinyl)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_item(self, request, pk=None):
        cart = self.get_object()
        vinyl_id = request.data.get('vinyl_id')
        if not vinyl_id:
            return Response({"error": "vinyl_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            cart_item = CartItem.objects.get(cart=cart, vinyl_id=vinyl_id)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({"error": "CartItem not found"}, status=status.HTTP_404_NOT_FOUND)

class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderDetail.objects.filter(order__user=self.request.user)