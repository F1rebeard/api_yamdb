from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals
        #  Мера борьбы с линтером
        if False:
            print(users.signals.post_save.__doc__)
