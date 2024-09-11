from django.core import mail
from django.test import TestCase
from django.core.management import call_command
from datetime import date, timedelta
from shifts.models import Shift, ShiftDetails
from django.contrib.auth import get_user_model

class EmailTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username="testuser")

    def test_send_email_with_data(self):
        # Create some test data
        yesterday = date.today() - timedelta(days=1)
        shift = Shift.objects.create(
            shift_no=1,
            activity="Loading",
            date=yesterday,
            supplier="Supplier A",
            shift_type="Type1",
            coffee_type="Coffee1",
            output_batchno=1001,
            location_of_batch="Location A",
            status=False,
            created_by=self.user
        )
        ShiftDetails.objects.create(
            shift=shift,
            entry_type="In",
            grade="A",
            total_bags=100,
            total_kgs=1000.0,
            batchno_grn="B001",
            cell="C1"
        )

        # Call your management command
        call_command('send_daily_report')

        # Test that one message has been sent
        self.assertEqual(len(mail.outbox), 1)

        # Verify the email content
        email = mail.outbox[0]
        self.assertIn('Please find attached the daily shift report', email.body)
        self.assertEqual(len(email.attachments), 1)

    def test_send_email_without_data(self):
        # Call your management command (no data in the database)
        call_command('send_daily_report')

        # Test that one message has been sent
        self.assertEqual(len(mail.outbox), 1)

        # Verify the email content
        email = mail.outbox[0]
        self.assertIn('No data available for the daily report', email.body)
        self.assertEqual(len(email.attachments), 0)

    def tearDown(self):
        # Clear the outbox after each test
        mail.outbox = []