from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from expenses.tasks import send_daily_spending_report

class Command(BaseCommand):
    help = "Start the scheduler for sending daily spending reports."

    def handle(self, *args, **kwargs):
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_daily_spending_report, 'cron', hour=20, minute=0)  # 매일 20시 실행
        scheduler.start()

        self.stdout.write(self.style.SUCCESS("Scheduler started..."))

        try:
            # 스케줄러를 무기한 실행 상태로 유지
            scheduler._thread.join()
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()