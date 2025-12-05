from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Đường dẫn")
    content = models.TextField(verbose_name="Nội dung")
    featured_image = models.ImageField(upload_to='posts/', blank=True, null=True, verbose_name="Ảnh bìa")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Ngày đăng")
    is_published = models.BooleanField(default=True, verbose_name="Đã xuất bản")
    is_featured = models.BooleanField(default=False, verbose_name="Tin nổi bật")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Tin công ty"
        verbose_name_plural = "Tin công ty"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

class ExternalNews(models.Model):
    SOURCE_CHOICES = [
        ('customs', 'Tổng cục Hải quan'),
        ('logistics', 'Cục Logistics Việt Nam'),
    ]
    
    title = models.CharField(max_length=300, verbose_name="Tiêu đề")
    summary = models.TextField(blank=True, verbose_name="Tóm tắt")
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, verbose_name="Nguồn")
    source_url = models.URLField(verbose_name="Liên kết gốc")
    published_date = models.DateTimeField(verbose_name="Ngày xuất bản")
    fetched_at = models.DateTimeField(default=timezone.now, verbose_name="Ngày lấy tin")
    is_active = models.BooleanField(default=True, verbose_name="Hiển thị")
    
    class Meta:
        ordering = ['-published_date']
        verbose_name = "Tin chuyên ngành"
        verbose_name_plural = "Tin chuyên ngành"
        unique_together = ['source_url', 'source']
    
    def __str__(self):
        return f"[{self.get_source_display()}] {self.title[:50]}..."
    
    @property 
    def default_image_title(self):
        """Generate title for default news image"""
        source_names = {
            'customs': 'Tin tức Hải quan',
            'logistics': 'Tin tức Logistics'
        }
        return source_names.get(self.source, 'Tin tức chuyên ngành')
