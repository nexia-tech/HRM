from django.apps import AppConfig


class HrmAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hrm_app'

    def ready(self):
        import hrm_app.signals