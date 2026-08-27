from django.db import models
from hr.models import Staff

class AssetCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Asset(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    purchase_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"

class AssetIssue(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='issues')
    issued_to = models.ForeignKey(Staff, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.quantity}x {self.asset.name} -> {self.issued_to.user.get_full_name()}"
