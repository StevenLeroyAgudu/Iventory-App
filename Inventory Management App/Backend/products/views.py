import logging
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product, StockStatus
from products.serializers import ProductSerializer, DashboardSerializer
from products.services.stock_service import process_stock_status

logger = logging.getLogger("products")


# ──────────────────────────────────────────────
# PRODUCT LIST & CREATE
# ──────────────────────────────────────────────

@api_view(["GET", "POST"])
def product_list(request):
    """
    GET  /api/products/  → List all products
    POST /api/products/  → Create a new product
    """
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            product = process_stock_status(product)
            return Response(
                ProductSerializer(product).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ──────────────────────────────────────────────
# PRODUCT DETAIL, UPDATE, DELETE
# ──────────────────────────────────────────────

@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, pk):
    """
    GET    /api/products/{id}/  → Get single product
    PUT    /api/products/{id}/  → Update product
    DELETE /api/products/{id}/  → Delete product
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            {"error": f"Product with id={pk} not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        return Response(ProductSerializer(product).data)

    if request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            product = serializer.save()
            product = process_stock_status(product)
            return Response(ProductSerializer(product).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        product_name = product.product_name
        product.delete()
        logger.info(f"Product '{product_name}' (id={pk}) deleted.")
        return Response(
            {"message": f"Product '{product_name}' deleted successfully."},
            status=status.HTTP_200_OK,
        )


# ──────────────────────────────────────────────
# STOCK ALERT ENDPOINTS
# ──────────────────────────────────────────────

@api_view(["GET"])
def low_stock(request):
    """GET /api/products/low-stock/ → Products below min_threshold"""
    products = Product.objects.filter(status=StockStatus.LOW)
    serializer = ProductSerializer(products, many=True)
    return Response({
        "count": products.count(),
        "results": serializer.data,
    })


@api_view(["GET"])
def high_stock(request):
    """GET /api/products/high-stock/ → Products above max_threshold"""
    products = Product.objects.filter(status=StockStatus.HIGH)
    serializer = ProductSerializer(products, many=True)
    return Response({
        "count": products.count(),
        "results": serializer.data,
    })


# ──────────────────────────────────────────────
# DASHBOARD
# ──────────────────────────────────────────────

@api_view(["GET"])
def dashboard(request):
    """GET /api/dashboard/ → Summary statistics"""
    total = Product.objects.count()
    low = Product.objects.filter(status=StockStatus.LOW).count()
    high = Product.objects.filter(status=StockStatus.HIGH).count()
    normal = Product.objects.filter(status=StockStatus.NORMAL).count()

    data = {
        "total_products": total,
        "low_stock": low,
        "overstock": high,
        "normal_stock": normal,
    }
    serializer = DashboardSerializer(data)
    return Response(serializer.data)
