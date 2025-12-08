from django.core.management.base import BaseCommand
from main.news_fetcher import NewsFetcher

class Command(BaseCommand):
    help = 'Fetch news from external sources (Customs and Logistics)'

    def handle(self, *args, **options):
        self.stdout.write('Starting news fetch...')
        
        fetcher = NewsFetcher()
        count = fetcher.fetch_all_news()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully fetched {count} news items'))
