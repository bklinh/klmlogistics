import schedule
import time
import os
import sys
import django
from django.core.management import call_command

# Setup Django environment
# Ensure we are in the correct directory or add it to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'klm_logistics.settings')
django.setup()

def job():
    print(f"Starting news fetch job at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    try:
        call_command('fetch_news')
    except Exception as e:
        print(f"Job failed: {e}")

# Schedule 3 times a day
# You can adjust these times as needed
schedule.every().day.at("08:00").do(job)
schedule.every().day.at("13:00").do(job)
schedule.every().day.at("18:00").do(job)

print("Scheduler started. Will fetch news at 08:00, 13:00, and 18:00.")
print("Press Ctrl+C to exit.")

# Run once on startup to ensure data is fresh
job()

while True:
    schedule.run_pending()
    time.sleep(60)
