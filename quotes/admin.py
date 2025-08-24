from django.contrib import admin
from .models import Source, Quote, ViewEvent, Vote

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'created_at')
    search_fields = ('name',)
    list_filter = ('type',)

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'source', 'weight', 'views', 'likes', 'dislikes', 'is_active', 'created_at')
    search_fields = ('text', 'source__name')
    list_filter = ('source__type', 'is_active')
    autocomplete_fields = ('source',)
    readonly_fields = ('views', 'likes', 'dislikes', 'text_normalized')

    def short_text(self, obj):
        return (obj.text[:70] + '…') if len(obj.text) > 70 else obj.text

admin.site.register(ViewEvent)
admin.site.register(Vote)
