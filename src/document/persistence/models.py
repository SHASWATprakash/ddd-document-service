from django.db import models


class DocumentModel(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ("invoice", "Invoice"),
        ("receipt", "Receipt"),
    ]

    reference = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.CharField(max_length=30)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    line_item_limit = models.PositiveIntegerField()
    line_item_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
       
        db_table = "documents"

    def __str__(self) -> str:
        return f"Document({self.reference})"


class OutboxEvent(models.Model):
    event_id = models.UUIDField(unique=True)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        app_label = "document"
        db_table = "outbox_events"
        indexes = [
            models.Index(fields=["processed", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"OutboxEvent({self.event_type}, processed={self.processed})"