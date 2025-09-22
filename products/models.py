# products/models.py
from django.db import models

class TrendingProductManager(models.Manager):
    def enforce_limit(self, limit=1000):
        count = self.count()
        if count > limit:
            # delete oldest rows
            to_delete = count - limit
            oldest = self.order_by("updated_at")[:to_delete]
            self.filter(id__in=[p.id for p in oldest]).delete()


class TrendingProduct(models.Model):
    product_id = models.CharField(max_length=50, unique=True)
    title = models.TextField()
    category = models.CharField(max_length=255)
    marketplace = models.CharField(max_length=50)  # amazon / flipkart
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    previous_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    price_drop = models.DecimalField(max_digits=12, decimal_places=2)
    url = models.URLField(max_length=2000)
    image = models.URLField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    objects = TrendingProductManager()

    def __str__(self):
        return f"{self.marketplace} - {self.title[:30]}"
