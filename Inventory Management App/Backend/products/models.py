from django.db import models


class StockStatus(models.TextChoices):
    LOW = "LOW", "Low Stock"
    NORMAL = "NORMAL", "Normal"
    HIGH = "HIGH", "Overstock"


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)
    min_threshold = models.IntegerField(default=0)
    max_threshold = models.IntegerField(default=100)
    status = models.CharField(
        max_length=10,
        choices=StockStatus.choices,
        default=StockStatus.NORMAL,
        editable=False,  # Computed automatically, never set manually
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.product_name} (Qty: {self.quantity}, Status: {self.status})"

    def compute_status(self) -> str:
        """Determine stock status based on quantity vs thresholds."""
        if self.quantity < self.min_threshold:
            return StockStatus.LOW
        elif self.quantity > self.max_threshold:
            return StockStatus.HIGH
        return StockStatus.NORMAL
