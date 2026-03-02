import schedule
import time
from datetime import datetime
import os
import subprocess

DAILY_LOOP_SCRIPT = "do_daily_loop.py"

def job():
    print(f"\n[{datetime.now()}] ⏰ Scheduler triggered job!")
    if os.path.exists(DAILY_LOOP_SCRIPT):
        # Run the script in a subprocess so crashes don't kill the scheduler
        subprocess.run(["python", DAILY_LOOP_SCRIPT])
    else:
        print(f"❌ Could not find {DAILY_LOOP_SCRIPT}!")

def main():
    print(f"[{datetime.now()}] 🚀 YouTube Viral Notes Scheduler Started.")
    print("⏳ The script is now running in the background.")
    
    # Configure the exact time you want this to run daily
    # For testing purposes, we also run it immediately once
    print("🔄 Running initial immediate loop...")
    job()
    
    print("\n📅 Scheduling daily runs for 10:00 AM (local time)...")
    schedule.every().day.at("10:00").do(job)
    
    # If the user wants to test frequency, they can uncomment this:
    # schedule.every(2).hours.do(job) 

    while True:
        schedule.run_pending()
        time.sleep(60) # Wake up every minute to check the schedule

if __name__ == "__main__":
    main()
