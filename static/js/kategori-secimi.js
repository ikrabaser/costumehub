document.addEventListener("DOMContentLoaded", function () {
    const kategoriAlani = document.getElementById(
        "kategori-secim-alani"
    );

    const gizliKategoriInput = document.getElementById(
        "id_kategori"
    );

    if (!kategoriAlani || !gizliKategoriInput) {
        return;
    }

    const anaKategoriler =
        window.anaKategoriler || [];

    const seciliKategoriYolu =
        window.seciliKategoriYolu || [];

    const altKategoriUrlSablonu =
        window.altKategoriUrlSablonu || "";

    /*
        "ilan" modunda yalnızca en alt kategori seçildiğinde
        gizli input doldurulur.

        "filtre" modunda ana kategori veya herhangi bir
        alt kategori seçildiğinde gizli input doldurulur.
    */
    const kategoriSecimModu =
        window.kategoriSecimModu || "ilan";

    const filtreModuMu =
        kategoriSecimModu === "filtre";


    function kategoriUrlOlustur(kategoriId) {
        return altKategoriUrlSablonu.replace(
            "/0/",
            `/${kategoriId}/`
        );
    }


    function enSonSeciliKategoriyiBul() {
        const selectler =
            kategoriAlani.querySelectorAll(
                ".kategori-seviye select"
            );

        let enSonKategoriId = "";

        selectler.forEach(function (select) {
            if (select.value) {
                enSonKategoriId = select.value;
            }
        });

        return enSonKategoriId;
    }


    function secimKutusuOlustur(
        kategoriler,
        seviye,
        seciliId = null
    ) {
        const kapsayici =
            document.createElement("div");

        kapsayici.className =
            "kategori-seviye";

        const etiket =
            document.createElement("label");

        etiket.className =
            "form-label fw-semibold";

        etiket.textContent =
            seviye === 0
                ? "Ana kategori"
                : `${seviye}. alt kategori`;

        const select =
            document.createElement("select");

        select.className =
            "form-select";

        select.dataset.seviye =
            seviye;

        const varsayilanSecenek =
            document.createElement("option");

        varsayilanSecenek.value = "";

        varsayilanSecenek.textContent =
            seviye === 0
                ? "Ana kategori seçin"
                : "Alt kategori seçin";

        select.appendChild(
            varsayilanSecenek
        );

        kategoriler.forEach(function (kategori) {
            const secenek =
                document.createElement("option");

            secenek.value =
                kategori.id;

            secenek.textContent =
                kategori.ad;

            if (
                String(kategori.id) ===
                String(seciliId)
            ) {
                secenek.selected = true;
            }

            select.appendChild(
                secenek
            );
        });

        select.addEventListener(
            "change",
            async function () {
                const secilenKategoriId =
                    this.value;

                const mevcutSeviye =
                    Number(
                        this.dataset.seviye
                    );

                sonrakiSeviyeleriSil(
                    mevcutSeviye
                );

                if (!secilenKategoriId) {
                    if (filtreModuMu) {
                        gizliKategoriInput.value =
                            enSonSeciliKategoriyiBul();
                    } else {
                        gizliKategoriInput.value = "";
                    }

                    return;
                }

                if (filtreModuMu) {
                    /*
                        Filtreleme sayfasında ana kategori
                        seçimi de geçerli kabul edilir.
                    */
                    gizliKategoriInput.value =
                        secilenKategoriId;
                } else {
                    /*
                        İlan oluşturma sayfasında önce alt
                        kategori olup olmadığı kontrol edilir.
                    */
                    gizliKategoriInput.value = "";
                }

                await altKategorileriGetir(
                    secilenKategoriId,
                    mevcutSeviye + 1
                );
            }
        );

        kapsayici.appendChild(
            etiket
        );

        kapsayici.appendChild(
            select
        );

        kategoriAlani.appendChild(
            kapsayici
        );
    }


    function sonrakiSeviyeleriSil(seviye) {
        const seviyeler =
            kategoriAlani.querySelectorAll(
                ".kategori-seviye"
            );

        seviyeler.forEach(function (alan) {
            const select =
                alan.querySelector("select");

            const alanSeviyesi =
                Number(
                    select.dataset.seviye
                );

            if (alanSeviyesi > seviye) {
                alan.remove();
            }
        });
    }


    async function kategoriVerisiniGetir(
        kategoriId
    ) {
        const url =
            kategoriUrlOlustur(
                kategoriId
            );

        const cevap =
            await fetch(url, {
                headers: {
                    "X-Requested-With":
                        "XMLHttpRequest",
                },
            });

        if (!cevap.ok) {
            throw new Error(
                "Alt kategoriler alınamadı."
            );
        }

        return await cevap.json();
    }


    async function altKategorileriGetir(
        kategoriId,
        sonrakiSeviye
    ) {
        try {
            const veri =
                await kategoriVerisiniGetir(
                    kategoriId
                );

            if (veri.alt_kategori_var_mi) {
                secimKutusuOlustur(
                    veri.alt_kategoriler,
                    sonrakiSeviye
                );

                /*
                    İlan oluşturma ekranında kullanıcıdan
                    daha alt kategoriyi seçmesini bekliyoruz.
                */
                if (!filtreModuMu) {
                    gizliKategoriInput.value = "";
                }
            } else {
                gizliKategoriInput.value =
                    kategoriId;
            }
        } catch (hata) {
            console.error(hata);

            alert(
                "Kategori bilgileri yüklenirken " +
                "bir hata oluştu."
            );
        }
    }


    async function seciliYoluKur() {
        if (
            seciliKategoriYolu.length === 0
        ) {
            secimKutusuOlustur(
                anaKategoriler,
                0
            );

            return;
        }

        secimKutusuOlustur(
            anaKategoriler,
            0,
            seciliKategoriYolu[0].id
        );

        for (
            let index = 0;
            index <
            seciliKategoriYolu.length - 1;
            index++
        ) {
            const mevcutKategori =
                seciliKategoriYolu[index];

            const sonrakiKategori =
                seciliKategoriYolu[
                    index + 1
                ];

            try {
                const veri =
                    await kategoriVerisiniGetir(
                        mevcutKategori.id
                    );

                secimKutusuOlustur(
                    veri.alt_kategoriler,
                    index + 1,
                    sonrakiKategori.id
                );
            } catch (hata) {
                console.error(hata);
                return;
            }
        }

        const sonKategori =
            seciliKategoriYolu[
                seciliKategoriYolu.length - 1
            ];

        try {
            const veri =
                await kategoriVerisiniGetir(
                    sonKategori.id
                );

            if (veri.alt_kategori_var_mi) {
                secimKutusuOlustur(
                    veri.alt_kategoriler,
                    seciliKategoriYolu.length
                );

                if (filtreModuMu) {
                    gizliKategoriInput.value =
                        sonKategori.id;
                } else {
                    gizliKategoriInput.value = "";
                }
            } else {
                gizliKategoriInput.value =
                    sonKategori.id;
            }
        } catch (hata) {
            console.error(hata);
        }
    }


    seciliYoluKur();
});