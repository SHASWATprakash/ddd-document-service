from rest_framework import serializers


class CreateDocumentSerializer(serializers.Serializer):
    reference = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=30)
    document_type = serializers.ChoiceField(choices=["invoice", "receipt"])
    line_item_limit = serializers.IntegerField(min_value=1)


class UpdateDocumentSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=30)
    line_item_limit = serializers.IntegerField(min_value=1)


class DeleteDocumentSerializer(serializers.Serializer):
    force_delete = serializers.BooleanField(default=False)


class LineItemSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1)


class DocumentResponseSerializer(serializers.Serializer):
    reference = serializers.CharField()
    description = serializers.CharField()
    document_type = serializers.CharField()
    line_item_count = serializers.IntegerField()
    line_item_limit = serializers.IntegerField()
    created_at = serializers.DateTimeField()