# products/serializers.py
from rest_framework import serializers
from .models import TrendingProduct

class TrendingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendingProduct
        fields = [
            "product_id",
            "title",
            "category",
            "marketplace",
            "current_price",
            "previous_price",
            "price_drop",
            "url",
            "image",
        ]

    def create(self, validated_data):
        # Update if product_id already exists
        obj, _ = TrendingProduct.objects.update_or_create(
            product_id=validated_data["product_id"],
            defaults=validated_data
        )
        return obj
