import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.text import slugify
from .models import ExternalNews
import logging
import time
import urllib3
from playwright.sync_api import sync_playwright

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

class NewsFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
        })
    
    def fetch_customs_news(self, limit=10):
        """Fetch news from customs.gov.vn using Playwright"""
        try:
            url = 'https://www.customs.gov.vn/index.jsp?pageId=4&cid=25'
            
            news_items = []
            
            # Use Playwright to handle dynamic content
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                try:
                    page.goto(url, timeout=60000)
                    # Wait for the news links to appear
                    try:
                        page.wait_for_selector('a[href*="aid="]', timeout=30000)
                    except:
                        logger.warning("Timeout waiting for aid= selector, trying to parse whatever is there")

                    # Get all links
                    links = page.query_selector_all('a')
                    
                    for link in links:
                        href = link.get_attribute('href')
                        text = link.inner_text().strip()
                        
                        if not href:
                            continue
                            
                        # Look for the specific article pattern: index.jsp?pageId=2&aid=...&cid=25
                        if 'aid=' in href and 'cid=25' in href:
                            news_items.append({'href': href, 'text': text})
                        # Also keep the generic check just in case
                        elif len(text) > 20 and 'index.jsp' in href and ('id=' in href or 'newsId=' in href):
                            news_items.append({'href': href, 'text': text})
                            
                        if len(news_items) >= limit * 2:
                            break
                            
                except Exception as e:
                    logger.error(f"Playwright error: {e}")
                finally:
                    browser.close()
            
            fetched_count = 0
            processed_urls = set()
            
            for item in news_items:
                try:
                    title = item['text']
                    link = item['href']
                    
                    if not title or len(title) < 10:
                        continue
                        
                    # Make link absolute
                    if link and not link.startswith('http'):
                        if link.startswith('/'):
                            link = 'https://www.customs.gov.vn' + link
                        else:
                            link = 'https://www.customs.gov.vn/' + link
                            
                    if link in processed_urls:
                        continue
                    processed_urls.add(link)
                    
                    # Create or update news item
                    news_obj, created = ExternalNews.objects.get_or_create(
                        source='customs',
                        source_url=link,
                        defaults={
                            'title': title[:300],
                            'summary': f"Tin tức từ Tổng cục Hải quan Việt Nam: {title}",
                            'published_date': timezone.now() - timedelta(hours=fetched_count),
                        }
                    )
                    
                    if created:
                        fetched_count += 1
                        logger.info(f"Fetched customs news: {title[:50]}...")
                    
                    if fetched_count >= limit:
                        break
                    
                except Exception as e:
                    logger.error(f"Error processing customs news item: {e}")
                    continue
            
            return fetched_count
            
        except Exception as e:
            logger.error(f"Error fetching customs news: {e}")
            return 0
    
    def fetch_logistics_news(self, limit=10):
        """Fetch news from logistics.gov.vn using Playwright"""
        try:
            # Fetch from the Activity News section which contains the latest updates
            url = 'https://logistics.gov.vn/tin-hoat-dong/'
            
            news_items = []
            
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                try:
                    page.goto(url, timeout=60000)
                    
                    # Get all links
                    links = page.query_selector_all('a')
                    
                    for link in links:
                        href = link.get_attribute('href')
                        text = link.inner_text().strip()
                        
                        if not href:
                            continue
                            
                        # Check if link belongs to the news category and is not a pagination link
                        if '/tin-hoat-dong/' in href and len(text) > 20 and 'page=' not in href:
                            news_items.append({'href': href, 'text': text})
                
                        if len(news_items) >= limit * 2:
                            break
                            
                except Exception as e:
                    logger.error(f"Playwright error for logistics: {e}")
                finally:
                    browser.close()
            
            fetched_count = 0
            processed_urls = set()
            
            for item in news_items:
                try:
                    title = item['text']
                    link = item['href']
                    
                    if not title or len(title) < 10:
                        continue
                        
                    # Make link absolute
                    if link and not link.startswith('http'):
                        if link.startswith('/'):
                            link = 'https://logistics.gov.vn' + link
                        else:
                            link = 'https://logistics.gov.vn/' + link
                            
                    if link in processed_urls:
                        continue
                    processed_urls.add(link)
                    
                    # Create or update news item
                    news_obj, created = ExternalNews.objects.get_or_create(
                        source='logistics',
                        source_url=link,
                        defaults={
                            'title': title[:300],
                            'summary': f"Tin tức từ Cục Logistics Việt Nam: {title}",
                            'published_date': timezone.now() - timedelta(hours=fetched_count),
                        }
                    )
                    
                    if created:
                        fetched_count += 1
                        logger.info(f"Fetched logistics news: {title[:50]}...")
                        
                    if fetched_count >= limit:
                        break
                    
                except Exception as e:
                    logger.error(f"Error processing logistics news item: {e}")
                    continue
            
            return fetched_count
            
        except Exception as e:
            logger.error(f"Error fetching logistics news: {e}")
            return 0
    
    def cleanup_old_news(self, limit=10):
        """Keep only the latest `limit` news items for each source"""
        try:
            for source in ['customs', 'logistics']:
                # Get IDs of the latest `limit` items
                latest_ids = ExternalNews.objects.filter(source=source).order_by('-published_date').values_list('id', flat=True)[:limit]
                
                # Delete items not in the latest list
                deleted_count, _ = ExternalNews.objects.filter(source=source).exclude(id__in=latest_ids).delete()
                
                if deleted_count > 0:
                    logger.info(f"Deleted {deleted_count} old {source} news items")
                    
        except Exception as e:
            logger.error(f"Error cleaning up old news: {e}")

    def fetch_all_news(self):
        """Fetch news from all sources"""
        total_fetched = 0
        
        logger.info("Starting news fetching...")
        
        # Fetch customs news
        customs_count = self.fetch_customs_news()
        total_fetched += customs_count
        logger.info(f"Fetched {customs_count} customs news items")
        
        # Fetch logistics news  
        logistics_count = self.fetch_logistics_news()
        total_fetched += logistics_count
        logger.info(f"Fetched {logistics_count} logistics news items")
        
        # Cleanup old news
        self.cleanup_old_news(limit=10)
        
        logger.info(f"Total news items fetched: {total_fetched}")
        return total_fetched