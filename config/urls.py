from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.views.decorators.csrf import csrf_exempt


schema_view = get_schema_view(
    openapi.Info(
        title='Kale API',
        description="Documentation of API endpoints of Kale",
        default_version='v2',
        contact=openapi.Contact(email="baxtikdev@gmail.com"),
        license=openapi.License(name='Kale License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
                  path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
                  path("about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
                  # Django Admin, use {% url 'admin:index' %}
                  path(settings.ADMIN_URL, admin.site.urls),
                  # User management
                  path("accounts/", include("allauth.urls")),
                  # Your stuff: custom urls includes go here
                  path('favicon.ico', lambda request: HttpResponse(status=404)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # AUTHENTICATION
    path('auth/', include("api.auth.urls")),
    # API base url
    path("api/", include("api.api_router")),

    # CHAT
    path("chat/", include("api.chat.chat_urls")),
    # DRF auth token

    # path("auth-token/", obtain_auth_token),
    path(
        'swagger.json',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path("api/schema/", csrf_exempt(SpectacularAPIView.as_view()), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path(
        'docs/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redocs/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
