from django.apps import AppConfig


class ProdutosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'produtos'

    def ready(self):
        """
        ready() é chamado quando o Django TERMINA de carregar todos os apps.
        É o local SEGURO para importar signals porque:
          - Todos os models já estão carregados
          - Não há risco de import circular
          - O registro dos signals é feito uma única vez
        """
        from . import signals as _signals  # noqa: F401
