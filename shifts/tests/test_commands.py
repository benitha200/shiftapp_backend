from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.core import mail
from unittest.mock import patch, Mock
from io import StringIO
from datetime import date, timedelta
from shifts.models import Shift, ShiftDetails
from datetime import datetime

class SendDailyReportTest(TestCase):
    def setUp(self):
        # Create a CustomUser instance
        User = get_user_model()
        self.user = User.objects.create(
            id=1,
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        
        # Create Shift and ShiftDetails instances
        self.shift = Shift.objects.create(
            shift_no=1,
            activity="Loading",
            date=date.today() - timedelta(days=1),
            supplier="Supplier A",
            shift_type="Type1",
            coffee_type="Coffee1",
            output_batchno=1001,
            location_of_batch="Location A",
            status=False,
            created_by=self.user
        )
        self.shift_detail = ShiftDetails.objects.create(
            shift=self.shift,
            entry_type="In",
            grade="A",
            total_bags=100,
            total_kgs=1000.0,
            batchno_grn="B001",
            cell="C1"
        )

    @patch('shifts.management.commands.send_daily_report.EmailMessage')
    def test_command_output(self, mock_email_message):
        out = StringIO()
        call_command('send_daily_report', stdout=out)
        self.assertIn('Daily report sent successfully', out.getvalue())

    @patch('shifts.management.commands.send_daily_report.EmailMessage')
    def test_email_sent(self, mock_email_message):
        # Create a mock instance
        mock_instance = Mock()
        mock_email_message.return_value = mock_instance
        
        call_command('send_daily_report')
        
        # Check that EmailMessage was called
        self.assertTrue(mock_email_message.called)
        
        # Get the args and kwargs of the call
        args, kwargs = mock_email_message.call_args
        
        # Check the 'to' field
        self.assertEqual(['benithaiyuyisenga2002@gmail.com'], kwargs.get('to', []))
        
        # Check the 'cc' field
        self.assertEqual(['benithalouange@gmail.com'], kwargs.get('cc', []))
        
        # Check if send method was called
        self.assertTrue(mock_instance.send.called)
        
        # Check the attachment name
        attachment_name = f'shift_report_{datetime.now().date() - timedelta(days=1)}_{datetime.now().date()}.csv'
        attachments = mock_instance.attach.call_args_list
        self.assertTrue(any(call[0][0] == attachment_name for call in attachments))