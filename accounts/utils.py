from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verification_url = request.build_absolute_uri(
        f'/accounts/verify-email/{uid}/{token}/'
    )

    subject = 'Verify your AI Study Hub account'
    message = render_to_string('accounts/email/verification_email.txt', {
        'user': user,
        'verification_url': verification_url,
    })
    html_message = render_to_string('accounts/email/verification_email.html', {
        'user': user,
        'verification_url': verification_url,
    })

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )
