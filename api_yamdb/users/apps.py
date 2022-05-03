from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals
        if False:
            print(users.signals.post_save.__doc__)
