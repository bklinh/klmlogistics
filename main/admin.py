from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    
    def has_add_permission(self, request):
        return False

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content', 'content_en', 'content_zh_hans')
    list_display = ['title', 'is_published', 'is_featured', 'created_at']
    list_filter = ['is_published', 'is_featured', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['is_published', 'is_featured']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'slug', 'featured_image')
        }),
        ('Nội dung', {
            'fields': ('content',)
        }),
        ('English Translation', {
            'fields': ('title_en', 'content_en'),
            'classes': ('collapse',)
        }),
        ('Chinese Translation', {
            'fields': ('title_zh_hans', 'content_zh_hans'),
            'classes': ('collapse',)
        }),
        ('Cài đặt', {
            'fields': ('is_published', 'is_featured'),
            'classes': ('collapse',)
        })
    )
    
    class Media:
        js = ('admin/js/vietnamese_slug.js',)
        
