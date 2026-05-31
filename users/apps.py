from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    # ─── Futuro: se precisar de signals no User (ex: enviar email de
    # boas-vindas no post_save), descomente o método ready():
    #
    # def ready(self):
    #     from . import signals as _signals
