"""
URL configuration for core project.

┌──────────────────────────────────────────────────────────────────────┐
│ JWT ENDPOINTS (Simple JWT)                                          │
│                                                                      │
│ /api/token           POST {email, password} → {access, refresh}    │
│   → Troca credenciais por um par de tokens JWT                     │
│   → access (60min): usado no header Authorization: Bearer <token>  │
│   → refresh (7d): usado para obter NOVOS access tokens sem relogin │
│                                                                      │
│ /api/token/refresh   POST {refresh} → {access} ( + novo refresh )  │
│   → Quando o access expira, o front-end chama este endpoint         │
│   → Com ROTATE_REFRESH_TOKENS=True, UM NOVO refresh é gerado       │
│   → O refresh anterior é invalidado (blacklist) se configurado     │
│                                                                      │
│ ESTRATÉGIA ACCESS vs REFRESH:                                       │
│   Access token CURTO (60min) → minimiza danos se vazar            │
│   Refresh token LONGO (7d) → evita login constante                │
│   Front-end renova silenciosamente via interceptor                  │
└──────────────────────────────────────────────────────────────────────┘
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('produtos.urls')),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
