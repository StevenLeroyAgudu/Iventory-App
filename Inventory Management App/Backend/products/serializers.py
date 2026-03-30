from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "quantity",
            "min_threshold",
            "max_threshold",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at"]

    def validate(self, data):
        min_t = data.get("min_threshold", getattr(self.instance, "min_threshold", None))
        max_t = data.get("max_threshold", getattr(self.instance, "max_threshold", None))

        if min_t is not None and max_t is not None and min_t >= max_t:
            raise serializers.ValidationError(
                "min_threshold must be strictly less than max_threshold."
            )

        quantity = data.get("quantity", getattr(self.instance, "quantity", None))
        if quantity is not None and quantity < 0:
            raise serializers.ValidationError("quantity cannot be negative.")

        return data


class DashboardSerializer(serializers.Serializer):
    total_products = serializers.IntegerField()
    low_stock = serializers.IntegerField()
    overstock = serializers.IntegerField()
    normal_stock = serializers.IntegerField()
