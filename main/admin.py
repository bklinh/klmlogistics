from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Post

@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
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
        ('Cài đặt', {
            'fields': ('is_published', 'is_featured'),
            'classes': ('collapse',)
        })
    )
    
    class Media:
        js = ('admin/js/vietnamese_slug.js',)
        
