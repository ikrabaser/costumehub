from django.db.models import Prefetch

from .models import Kategori


def kategoriler(request):
    aktif_alt_kategoriler = Kategori.objects.filter(
        aktif_mi=True,
    ).order_by(
        "sira",
        "ad",
    )

    navbar_ana_kategoriler = (
        Kategori.objects.filter(
            aktif_mi=True,
            ust_kategori__isnull=True,
        )
        .prefetch_related(
            Prefetch(
                "alt_kategoriler",
                queryset=aktif_alt_kategoriler.prefetch_related(
                    Prefetch(
                        "alt_kategoriler",
                        queryset=aktif_alt_kategoriler,
                    )
                ),
            )
        )
        .order_by(
            "sira",
            "ad",
        )
    )

    return {
        "navbar_ana_kategoriler": navbar_ana_kategoriler,
    }