document.addEventListener("DOMContentLoaded", function () {
    const dinamikFiltreAlani =
        document.getElementById(
            "dinamik-filtre-alani"
        );

    const hizliFiltreAlani =
        document.getElementById(
            "dinamik-hizli-filtreler"
        );

    const gizliKategoriInput =
        document.getElementById(
            "id_kategori"
        );

    const urlSablonu =
        window.kategoriOzellikleriUrlSablonu
        || "";

    if (
        !dinamikFiltreAlani
        || !hizliFiltreAlani
        || !urlSablonu
    ) {
        return;
    }


    function ozellikUrlOlustur(kategoriId) {
        return urlSablonu.replace(
            "/0/",
            `/${kategoriId}/`
        );
    }


    function seciliDegeriGetir(ozellikId) {
        const parametreler =
            new URLSearchParams(
                window.location.search
            );

        return parametreler.get(
            `ozellik_${ozellikId}`
        ) || "";
    }


    function alanlariTemizle() {
        dinamikFiltreAlani.innerHTML = "";
        hizliFiltreAlani.innerHTML = "";
    }


    function hizliFiltreOlustur(ozellik) {
        const buton =
            document.createElement("button");

        buton.type = "button";
        buton.className =
            "hizli-filtre-butonu";

        if (seciliDegeriGetir(ozellik.id)) {
            buton.classList.add("aktif");
        }

        buton.dataset.bsToggle =
            "collapse";

        buton.dataset.bsTarget =
            "#gelismis-filtreler";

        buton.textContent =
            `${ozellik.ad} ⌄`;

        return buton;
    }


    function etiketOlustur(ozellik) {
        const etiket =
            document.createElement("label");

        etiket.className =
            "form-label fw-semibold";

        etiket.htmlFor =
            `filtre_ozellik_${ozellik.id}`;

        etiket.textContent =
            ozellik.ad;

        return etiket;
    }


    function secimAlaniOlustur(ozellik) {
        const select =
            document.createElement("select");

        select.className = "form-select";
        select.id =
            `filtre_ozellik_${ozellik.id}`;
        select.name =
            `ozellik_${ozellik.id}`;

        const bosSecenek =
            document.createElement("option");

        bosSecenek.value = "";
        bosSecenek.textContent =
            `Tüm ${ozellik.ad.toLocaleLowerCase(
                "tr-TR"
            )} seçenekleri`;

        select.appendChild(bosSecenek);

        const seciliDeger =
            seciliDegeriGetir(ozellik.id);

        ozellik.secenekler.forEach(
            function (secenek) {
                const option =
                    document.createElement(
                        "option"
                    );

                option.value = secenek.id;
                option.textContent =
                    secenek.deger;

                if (
                    String(secenek.id)
                    === seciliDeger
                ) {
                    option.selected = true;
                }

                select.appendChild(option);
            }
        );

        return select;
    }


    function evetHayirAlaniOlustur(
        ozellik
    ) {
        const select =
            document.createElement("select");

        select.className = "form-select";
        select.id =
            `filtre_ozellik_${ozellik.id}`;
        select.name =
            `ozellik_${ozellik.id}`;

        const secenekler = [
            {
                deger: "",
                etiket: "Tümü",
            },
            {
                deger: "EVET",
                etiket: "Evet",
            },
            {
                deger: "HAYIR",
                etiket: "Hayır",
            },
        ];

        const seciliDeger =
            seciliDegeriGetir(ozellik.id);

        secenekler.forEach(
            function (secenek) {
                const option =
                    document.createElement(
                        "option"
                    );

                option.value =
                    secenek.deger;

                option.textContent =
                    secenek.etiket;

                if (
                    secenek.deger
                    === seciliDeger
                ) {
                    option.selected = true;
                }

                select.appendChild(option);
            }
        );

        return select;
    }


    function standartAlanOlustur(ozellik) {
        const input =
            document.createElement("input");

        input.className = "form-control";
        input.id =
            `filtre_ozellik_${ozellik.id}`;
        input.name =
            `ozellik_${ozellik.id}`;

        input.value =
            seciliDegeriGetir(ozellik.id);

        if (ozellik.veri_tipi === "SAYI") {
            input.type = "number";
            input.step = "any";
            input.placeholder =
                `${ozellik.ad} değeri`;
        } else {
            input.type = "text";
            input.placeholder =
                `${ozellik.ad} ara`;
        }

        return input;
    }


    function filtreAlaniOlustur(ozellik) {
        const kapsayici =
            document.createElement("div");

        kapsayici.className =
            "col-md-6 col-lg-3";

        const etiket =
            etiketOlustur(ozellik);

        let alan;

        if (ozellik.veri_tipi === "SECIM") {
            alan =
                secimAlaniOlustur(
                    ozellik
                );
        } else if (
            ozellik.veri_tipi
            === "EVET_HAYIR"
        ) {
            alan =
                evetHayirAlaniOlustur(
                    ozellik
                );
        } else {
            alan =
                standartAlanOlustur(
                    ozellik
                );
        }

        kapsayici.appendChild(etiket);
        kapsayici.appendChild(alan);

        return kapsayici;
    }


    function ozellikleriGoster(ozellikler) {
        alanlariTemizle();

        const filtrelenebilirOzellikler =
            ozellikler.filter(
                function (ozellik) {
                    return (
                        ozellik
                            .filtrelenebilir_mi
                        === true
                    );
                }
            );

        filtrelenebilirOzellikler.forEach(
            function (ozellik) {
                hizliFiltreAlani.appendChild(
                    hizliFiltreOlustur(
                        ozellik
                    )
                );

                dinamikFiltreAlani.appendChild(
                    filtreAlaniOlustur(
                        ozellik
                    )
                );
            }
        );
    }


    async function ozellikleriGetir(
        kategoriId
    ) {
        alanlariTemizle();

        if (!kategoriId) {
            return;
        }

        try {
            const cevap = await fetch(
                ozellikUrlOlustur(
                    kategoriId
                ),
                {
                    headers: {
                        "X-Requested-With":
                            "XMLHttpRequest",
                    },
                }
            );

            if (!cevap.ok) {
                throw new Error(
                    "Filtre özellikleri alınamadı."
                );
            }

            const veri =
                await cevap.json();

            ozellikleriGoster(
                veri.ozellikler || []
            );
        } catch (hata) {
            console.error(hata);
            alanlariTemizle();
        }
    }


    document.addEventListener(
        "kategoriDegisti",
        function (olay) {
            const kategoriId =
                olay.detail.kategoriId;

            if (!kategoriId) {
                alanlariTemizle();
                return;
            }

            ozellikleriGetir(
                kategoriId
            );
        }
    );


    if (
        gizliKategoriInput
        && gizliKategoriInput.value
    ) {
        ozellikleriGetir(
            gizliKategoriInput.value
        );
    }
});