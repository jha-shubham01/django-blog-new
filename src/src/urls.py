from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views

urlpatterns = [
    path("", include("blog.urls")),
    path("admin/", admin.site.urls),
    path("accounts/login/", views.LoginView.as_view(), name="login"),
    path("accounts/logout/", views.LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
