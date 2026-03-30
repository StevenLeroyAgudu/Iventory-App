import logging
import boto3
from django.conf import settings

logger = logging.getLogger("products")


def get_sns_client():
    return boto3.client(
        "sns",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


def send_stock_alert(product_name: str, quantity: int, status: str, threshold: int):
    """
    Publish a stock alert to the configured SNS topic.
    Silently logs errors so the API response is never blocked by SNS failures.
    """
    topic_arn = settings.SNS_TOPIC_ARN
    if not topic_arn:
        logger.warning("SNS_TOPIC_ARN not configured — skipping alert.")
        return

    if status == "LOW":
        subject = f"⚠️ Low Stock Alert: {product_name}"
        message = (
            f"INVENTORY ALERT - LOW STOCK\n\n"
            f"Product: {product_name}\n"
            f"Current Quantity: {quantity}\n"
            f"Minimum Threshold: {threshold}\n\n"
            f"Please restock this item as soon as possible."
        )
    elif status == "HIGH":
        subject = f"⚠️ Overstock Alert: {product_name}"
        message = (
            f"INVENTORY ALERT - OVERSTOCK\n\n"
            f"Product: {product_name}\n"
            f"Current Quantity: {quantity}\n"
            f"Maximum Threshold: {threshold}\n\n"
            f"Stock levels have exceeded the maximum threshold."
        )
    else:
        return  # No alert needed for NORMAL status

    try:
        client = get_sns_client()
        response = client.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message,
        )
        logger.info(
            f"SNS alert sent for '{product_name}' (status={status}). "
            f"MessageId: {response.get('MessageId')}"
        )
    except Exception as e:
        logger.error(f"Failed to send SNS alert for '{product_name}': {e}")
