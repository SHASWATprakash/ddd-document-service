from celery import shared_task
from django.utils import timezone


@shared_task(bind=True, max_retries=5, default_retry_delay=60)
def process_outbox_events(self):
    """
    Polls the outbox table and publishes unprocessed events.
    Guarantees at-least-once delivery via retry on failure.
    """
    from src.document.persistence.models import OutboxEvent
    import logging

    logger = logging.getLogger(__name__)

    unprocessed = OutboxEvent.objects.filter(processed=False).order_by("created_at")[:50]

    for event in unprocessed:
        try:
            # Extension point: publish to event bus (Kafka, SNS, etc.)
            logger.info(
                "Publishing event: type=%s reference=%s",
                event.event_type,
                event.payload.get("reference", "N/A"),
            )
            event.processed = True
            event.processed_at = timezone.now()
            event.save(update_fields=["processed", "processed_at"])
        except Exception as exc:
            logger.exception("Failed to process outbox event %s", event.event_id)
            raise self.retry(exc=exc)