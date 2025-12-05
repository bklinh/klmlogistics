import time
import schedule
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone

class Command(BaseCommand):
    help = 'Runs the news fetcher scheduler (3 times a day)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting scheduler...'))
        
        def job():
            self.stdout.write(self.style.SUCCESS(f'[{timezone.now()}] Starting scheduled news fetch...'))
            try:
                call_command('fetch_news')
                self.stdout.write(self.style.SUCCESS(f'[{timezone.now()}] News fetch completed successfully.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'[{timezone.now()}] Error fetching news: {e}'))

        # Schedule the job to run every 8 hours (3 times a day)
        schedule.every(8).hours.do(job)
        
        # Also run immediately on startup so we don't have to wait 8 hours
        job()

        self.stdout.write(self.style.SUCCESS('Scheduler started. Press Ctrl+C to exit.'))
        
        while True:
            schedule.run_pending()
            time.sleep(60)
