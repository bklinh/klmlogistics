from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import get_language

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Đường dẫn")
    content = models.TextField(verbose_name="Nội dung")
    # Translation Fields
    title_en = models.CharField(max_length=200, verbose_name="Tiêu đề (English)", blank=True, null=True)
    content_en = models.TextField(verbose_name="Nội dung (English)", blank=True, null=True)
    title_zh_hans = models.CharField(max_length=200, verbose_name="Tiêu đề (Chinese)", blank=True, null=True)
    content_zh_hans = models.TextField(verbose_name="Nội dung (Chinese)", blank=True, null=True)

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
    
    @property
    def translated_title(self):
        """Returns title based on current active language"""
        lang = get_language()
        if lang == 'en' and self.title_en:
            return self.title_en
        elif lang == 'zh-hans' and self.title_zh_hans:
            return self.title_zh_hans
        return self.title

    @property
    def translated_content(self):
        """Returns content based on current active language"""
        lang = get_language()
        if lang == 'en' and self.content_en:
            return self.content_en
        elif lang == 'zh-hans' and self.content_zh_hans:
            return self.content_zh_hans
        return self.content
    
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

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Họ tên")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Điện thoại", blank=True, null=True)
    subject = models.CharField(max_length=200, verbose_name="Chủ đề", blank=True, null=True)
    message = models.TextField(verbose_name="Nội dung")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày gửi")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Liên hệ"
        verbose_name_plural = "Liên hệ"

    def __str__(self):
        return f"{self.name} - {self.subject}"
