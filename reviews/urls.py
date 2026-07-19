from django.urls import path

from . import views


app_name = "reviews"


urlpatterns = [
    path(
        "olustur/<int:talep_id>/",
        views.degerlendirme_olustur,
        name="degerlendirme_olustur",
    ),
]