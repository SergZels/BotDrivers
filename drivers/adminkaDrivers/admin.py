from django.contrib import admin
from .models import Cod, Publications, Driver
# Register your models here.

class PublicationsAdmin(admin.ModelAdmin):
    list_display = ('driver', 'data', 'text','PublicationsAllowed')
    actions = ['approve_selected']

    def approve_selected(self, request, queryset):
        queryset.update(PublicationsAllowed=True)
    approve_selected.short_description = 'Одобрити вибрані статті'


admin.site.register(Cod)
admin.site.register(Publications, PublicationsAdmin)
admin.site.register(Driver)

from django.contrib.auth.models import User, Group
admin.site.unregister(User)
admin.site.unregister(Group)