from django.db import models

class Package(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    tier = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_recommended = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    cta_label = models.CharField(max_length=100)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.name
    
class PackageFeature(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='features')
    feature_text = models.CharField(max_length=255)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f'{self.package.name} - {self.feature_text}'
