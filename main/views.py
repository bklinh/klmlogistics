from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Post, ExternalNews

def home(request):
    # Get latest 6 published news articles for homepage
    latest_news = Post.objects.filter(is_published=True).order_by('-created_at')[:6]
    
    context = {
        'latest_news': latest_news,
    }
    return render(request, 'home.html', context)

def home_en(request):
    return render(request, 'en/home.html')

def home_cn(request):
    return render(request, 'cn/home.html')

def about(request):
    return render(request, 'pages/about.html')

def services(request):
    return render(request, 'pages/services.html')

def air_transport(request):
    return render(request, 'services/air_transport.html')

def sea_transport(request):
    return render(request, 'services/sea_transport.html')

def logistics(request):
    return render(request, 'services/logistics.html')

def company_news(request):
    # Get published posts
    posts = Post.objects.filter(is_published=True)
    
    # Pagination
    paginator = Paginator(posts, 9)  # Show 9 posts per page
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    context = {
        'posts': posts_page,
        'current_category': 'company',
        'page_title': 'Tin công ty'
    }
    return render(request, 'news/company.html', context)

def industry_news(request):
    # Get external news from both sources
    external_news = ExternalNews.objects.filter(is_active=True)
    
    # Pagination
    paginator = Paginator(external_news, 10)  # Show 10 news per page
    page_number = request.GET.get('page')
    news_page = paginator.get_page(page_number)
    
    context = {
        'external_news': news_page,
        'current_category': 'industry',
        'page_title': 'Tin chuyên ngành'
    }
    return render(request, 'news/industry.html', context)

def recruitment(request):
    # Static page for recruitment
    context = {
        'current_category': 'recruitment',
        'page_title': 'Tuyển dụng'
    }
    return render(request, 'news/recruitment.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    related_posts = Post.objects.filter(
        is_published=True
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'current_category': 'company'
    }
    return render(request, 'news/_post_detail.html', context)

def contact(request):
    return render(request, 'pages/contact.html')

def branch_network(request):
    return render(request, 'contact/branches.html')

def projects(request):
    return render(request, 'pages/projects.html')

def feedback(request):
    return render(request, 'pages/feedback.html')

def search(request):
    query = request.GET.get('qr', '')
    # Implement search functionality here
    context = {'query': query, 'results': []}
    return render(request, 'search.html', context)
