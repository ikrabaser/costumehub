"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "",
        include("products.urls"),
    ),
    path(
        "hesap/",
        include("accounts.urls"),
    ),
    path(
        "kiralamalar/",
        include("rentals.urls"),
    ),
    path(
        "mesajlar/",
        include("conversations.urls"),
    ),
    path(
        "degerlendirmeler/",
        include("reviews.urls"),
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )