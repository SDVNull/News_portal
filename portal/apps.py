from django.apps import AppConfig




class PortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portal'
    verbose_name = 'Портал новостей'

    def ready(self):
        from portal.tasks import send_emails_weekly
        send_emails_weekly.apply_async()
        # from . import signals