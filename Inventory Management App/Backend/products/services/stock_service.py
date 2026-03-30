import logging
from products.models import Product
from products.services.alert_service import send_stock_alert

logger = logging.getLogger("products")


def process_stock_status(product: Product) -> Product:
    """
    Compute and save the stock status for a product.
    Triggers an SNS alert if status is LOW or HIGH.
    Returns the updated product instance.
    """
    new_status = product.compute_status()
    product.status = new_status
    product.save()

    logger.info(
        f"Product '{product.product_name}' (id={product.id}) status set to '{new_status}'."
    )

    if new_status == "LOW":
        send_stock_alert(
            product_name=product.product_name,
            quantity=product.quantity,
            status=new_status,
            threshold=product.min_threshold,
        )
    elif new_status == "HIGH":
        send_stock_alert(
            product_name=product.product_name,
            quantity=product.quantity,
            status=new_status,
            threshold=product.max_threshold,
        )

    return product
