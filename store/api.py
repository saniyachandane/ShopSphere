from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .models import Category, Product, Order
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Public, read-only category endpoint."""
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "id"]

class ProductViewSet(viewsets.ModelViewSet):
    """Anyone can browse products; only staff can create/update/delete them."""
    queryset = Product.objects.select_related("category").all().order_by("-created_at")
    serializer_class = ProductSerializer
    search_fields = ["name", "description", "category__name"]
    ordering_fields = ["name", "price", "created_at", "stock"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]

class OrderViewSet(viewsets.ReadOnlyModelViewSet):
    """Authenticated users can view only their own orders; staff can view all."""
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.prefetch_related("items__product").order_by("-created_at")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(customer=self.request.user)
