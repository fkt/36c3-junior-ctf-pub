from django.contrib import admin
from .models import Challenge

def make_published(modeladmin, request, queryset):
        queryset.update(is_published=True)
        make_published.short_description = "Publish challenges"
        
def make_unpublished(modeladmin, request, queryset):
        queryset.update(is_published=False)
        make_published.short_description = "Unpublish challenges"

class ChallengeAdmin(admin.ModelAdmin):
        list_display = ['name', 'is_published']
        ordering = ['stage', 'name']
        actions = [make_published, make_unpublished]

admin.site.register(Challenge, ChallengeAdmin)
