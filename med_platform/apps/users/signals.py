from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.contrib.sites.models import Site
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User
import jwt


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            instance.is_email_verified = True
            instance.is_active = True
            instance.save(update_fields=['is_email_verified', 'is_active'])
            return

        if not instance.is_email_verified:
            token = jwt.encode(
                {'user_id': instance.id},
                settings.SECRET_KEY,
                algorithm='HS256'
            )

            current_site = Site.objects.get_current()
            activation_link = f"http://localhost:8000/api/users/activate/{token}/"

            subject = 'Activate your account'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [instance.email]

            text_content = f'Hi {instance.username}, click the link to activate your account: {activation_link}'
            html_content = f"""
                <html>
                    <body>
                        <p>Hi <strong>{instance.username}</strong>,</p>
                        <p>Please click the button below to activate your account:</p>
                        <p>
                            <a href="{activation_link}" style="display:inline-block;padding:10px 20px;background-color:#007bff;color:#ffffff;text-decoration:none;border-radius:5px;">
                                Activate Account
                            </a>
                        </p>
                        <p>If the button doesn’t work, you can also use this link:</p>
                        <p>{activation_link}</p>
                    </body>
                </html>
            """

            email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            email.attach_alternative(html_content, "text/html")
            email.send()

            print(f"📧 Письмо отправлено на {instance.email}")
