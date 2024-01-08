import re

from django.conf import settings
from django.core.mail import EmailMessage


def check_email(email, regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'):
    # pass the regular expression
    # and the string into the fullmatch() method
    if (re.fullmatch(regex, email)):
        return True
    else:
        return False



# Email notification for menager
    email_address = "fpiecyk.dev@gmail.com"
    template_text = (f"Otrzymano nową prośbę o rezerwację łodzi {booking.boat_id.name} "
                     f"w terminie {booking.start_date} - {booking.end_date}")


def email_confirmation(email_address,template_text):
    email = EmailMessage(
        'Boatify - informacje o rezerwacji',
        template_text,
        settings.EMAIL_HOST_USER,
        (email_address,)
    )
    email.fail_silently = False
    return email.send()
