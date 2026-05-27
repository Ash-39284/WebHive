from django.contrib import admin
from .models import Package, PackageFeature

class PackageFeatureInline(admin.TabularInline):
    model = PackageFeature
    extra = 1

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'price', 'is_recommended', 'is_active', 'display_order']
    inlines = [PackageFeatureInline]