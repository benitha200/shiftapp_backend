from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime, timedelta
from reports.views import ShiftDetailsReportView
import csv
from io import StringIO

class Command(BaseCommand):
    help = 'Sends daily shift report'

    def handle(self, *args, **options):
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)

        report_view = ShiftDetailsReportView()
        report_data = report_view.generate_report(yesterday, today)

        subject = f"Daily Shift Report - {yesterday} to {today}"
        
        if report_data:
            # Create CSV file
            csv_file = StringIO()
            csv_writer = csv.DictWriter(csv_file, fieldnames=report_data[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(report_data)
            csv_file.seek(0)  # Important to rewind the StringIO buffer

            body = f"Please find attached the daily shift report for {yesterday} to {today}."

            email = EmailMessage(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,  # Ensure this is set in settings
                to=['benithaiyuyisenga2002@gmail.com'],
                cc=['benithalouange@gmail.com']
            )
            email.attach(f'shift_report_{yesterday}_{today}.csv', csv_file.getvalue(), 'text/csv')
        else:
            body = f"No data available for the daily report for {yesterday} to {today}."
            email = EmailMessage(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                to=['benithaiyuyisenga2002@gmail.com'],
                cc=['benithalouange@gmail.com']
            )

        email.send()
        self.stdout.write(self.style.SUCCESS('Daily report email sent successfully'))