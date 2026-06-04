

import time

from django.shortcuts import redirect


class PerformanceLogMiddleware:
    """
    Loga o tempo de processamento de cada requisição no terminal.

    ⚠️ ATENÇÃO: o print aparece no CONSOLE DO DOCKER (docker compose logs),
    NÃO no navegador. Útil para identificar rotas lentas em desenvolvimento.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ─── CÓDIGO ANTES DA VIEW (entrada da requisição) ─────────────
        tempo_inicio = time.time()

        # Passa a request para o próximo middleware ou para a view
        response = self.get_response(request)

        # ─── CÓDIGO DEPOIS DA VIEW (saída da resposta) ───────────────
        tempo_total = time.time() - tempo_inicio
        print(f'⏱️ [PERFORMANCE] Rota: {request.path} | Tempo: {tempo_total:.4f}s')

        return response


class UnauthorizedUserAccessMiddleware:
    """
    Redireciona usuários não-autorizados (não-staff) que tentam
    acessar /admin para a página inicial (products_list).

    ⚠️ NÃO ATIVO POR PADRÃO. Para ativar, adicione em settings.py:
        'core.middlewares.UnauthorizedUserAccessMiddleware',

    ⚠️ CUIDADO: Este middleware deve vir DEPOIS de AuthenticationMiddleware
    no settings.py, porque ele depende de request.user estar disponível.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # hasattr check: garante que o AuthenticationMiddleware já rodou
        if hasattr(request, 'user'):
            is_unauthorized = not request.user.is_staff
            is_protected_route = request.path.startswith('/admin')

            if is_unauthorized and is_protected_route:
                return redirect('products_list')

        return self.get_response(request)
