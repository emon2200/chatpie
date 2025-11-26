# core/admin.py
from django.contrib import admin
from .models import Tenant

class TenantAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'db_url', 'rest_api')  # শুধুমাত্র বিদ্যমান ফিল্ড

admin.site.register(Tenant, TenantAdmin)
