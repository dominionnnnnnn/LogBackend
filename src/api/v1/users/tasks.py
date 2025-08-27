from celery import shared_task
import requests
from django.conf import settings

from django.core.mail import send_mail

@shared_task
def send_verification_email(to_email, code):
    send_mail(
        subject="Verify Your Email",
        message=f"Your verification code is: {code}. It will expire in 3 minutes",
        from_email=f"App Team <noreply@myapp.com>",
        recipient_list=[to_email],
        fail_silently=False,
    )
    # try:
    #     response = requests.post(
    #         f"https://api.mailgun.net/v3/{settings.MAILGUN_DOMAIN}/messages",
    #         auth=("api", settings.MAILGUN_API_KEY),
    #         data={
    #             "from": f"App Team <noreply@{settings.MAILGUN_DOMAIN}>",
    #             "to": [to_email],
    #             "subject": "Verify Your Email",
    #             "text": f"Your verification code is: {code}. It will expire in 10 minutes.",
    #         }
    #     )

    #     return {
    #         "status_code": response.status_code,
    #         "success": response.status_code == 200
    #     }

    # except Exception as e:
    #     return {"error": str(e)}
