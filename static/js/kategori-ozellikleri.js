document.addEventListener("DOMContentLoaded", function () {
    const ozelliklerBolumu =
        document.getElementById(
            "dinamik-ozellikler-bolumu"
        );

    const ozelliklerAlani =
        document.getElementById(
            "dinamik-ozellikler-alani"
        );

    const yukleniyorAlani =
        document.getElementById(
            "dinamik-ozellikler-yukleniyor"
        );

    const hataAlani =
        document.getElementById(
            "dinamik-ozellikler-hata"
        );

    const urlSablonu =
        window.kategoriOzellikleriUrlSablonu || "";

    if (
        !ozelliklerBolumu
        || !ozelliklerAlani
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


    function alanlariTemizle() {
        ozelliklerAlani.innerHTML = "";

        hataAlani.textContent = "";
        hataAlani.classList.add("d-none");

        yukleniyorAlani.classList.add(
            "d-none"
        );

        ozelliklerBolumu.classList.add(
            "d-none"
        );
    }


    function ortakAlanBilgileriniEkle(
        input,
        ozellik
    ) {
        input.classList.add("form-control");

        input.id =
            `ozellik_${ozellik.id}`;

        input.name =
            `ozellik_${ozellik.id}`;

        if (ozellik.zorunlu_mu) {
            input.required = true;
        }
    }


    function secimAlaniOlustur(ozellik) {
        const select =
            document.createElement("select");

        select.className = "form-select";
        select.id =
            `ozellik_${ozellik.id}`;
        select.name =
            `ozellik_${ozellik.id}`;

        if (ozellik.zorunlu_mu) {
            select.required = true;
        }

        const bosSecenek =
            document.createElement("option");

        bosSecenek.value = "";
        bosSecenek.textContent =
            "Seçim yapın";

        select.appendChild(
            bosSecenek
        );

        ozellik.secenekler.forEach(
            function (secenek) {
                const option =
                    document.createElement(
                        "option"
                    );

                option.value = secenek.id;
                option.textContent =
                    secenek.deger;

                select.appendChild(option);
            }
        );

        return select;
    }


    function metinAlaniOlustur(ozellik) {
        const input =
            document.createElement("input");

        input.type = "text";

        ortakAlanBilgileriniEkle(
            input,
            ozellik
        );

        return input;
    }


    function sayiAlaniOlustur(ozellik) {
        const input =
            document.createElement("input");

        input.type = "number";
        input.step = "any";

        ortakAlanBilgileriniEkle(
            input,
            ozellik
        );

        return input;
    }


    function evetHayirAlaniOlustur(
        ozellik
    ) {
        const select =
            document.createElement("select");

        select.className = "form-select";
        select.id =
            `ozellik_${ozellik.id}`;
        select.name =
            `ozellik_${ozellik.id}`;

        if (ozellik.zorunlu_mu) {
            select.required = true;
        }

        const secenekler = [
            {
                deger: "",
                etiket: "Seçim yapın",
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

                select.appendChild(option);
            }
        );

        return select;
    }


    function ozellikAlaniOlustur(ozellik) {
        const kapsayici =
            document.createElement("div");

        kapsayici.className =
            "col-md-6 mb-3";

        const etiket =
            document.createElement("label");

        etiket.className =
            "form-label fw-semibold";

        etiket.htmlFor =
            `ozellik_${ozellik.id}`;

        etiket.textContent =
            ozellik.ad;

        if (ozellik.zorunlu_mu) {
            const zorunluIsareti =
                document.createElement("span");

            zorunluIsareti.className =
                "text-danger ms-1";

            zorunluIsareti.textContent =
                "*";

            etiket.appendChild(
                zorunluIsareti
            );
        }

        let alan;

        if (ozellik.veri_tipi === "SECIM") {
            alan =
                secimAlaniOlustur(
                    ozellik
                );
        } else if (
            ozellik.veri_tipi === "SAYI"
        ) {
            alan =
                sayiAlaniOlustur(
                    ozellik
                );
        } else if (
            ozellik.veri_tipi ===
            "EVET_HAYIR"
        ) {
            alan =
                evetHayirAlaniOlustur(
                    ozellik
                );
        } else {
            alan =
                metinAlaniOlustur(
                    ozellik
                );
        }

        kapsayici.appendChild(etiket);
        kapsayici.appendChild(alan);

        return kapsayici;
    }


    function ozellikleriGoster(ozellikler) {
        ozelliklerAlani.innerHTML = "";

        if (ozellikler.length === 0) {
            ozelliklerBolumu.classList.add(
                "d-none"
            );

            return;
        }

        ozellikler.forEach(
            function (ozellik) {
                const alan =
                    ozellikAlaniOlustur(
                        ozellik
                    );

                ozelliklerAlani.appendChild(
                    alan
                );
            }
        );

        ozelliklerBolumu.classList.remove(
            "d-none"
        );
    }


    async function ozellikleriGetir(
        kategoriId
    ) {
        alanlariTemizle();

        ozelliklerBolumu.classList.remove(
            "d-none"
        );

        yukleniyorAlani.classList.remove(
            "d-none"
        );

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
                    "Kategori özellikleri alınamadı."
                );
            }

            const veri =
                await cevap.json();

            yukleniyorAlani.classList.add(
                "d-none"
            );

            ozellikleriGoster(
                veri.ozellikler || []
            );
        } catch (hata) {
            console.error(hata);

            yukleniyorAlani.classList.add(
                "d-none"
            );

            hataAlani.textContent =
                "Kategori özellikleri yüklenirken " +
                "bir hata oluştu.";

            hataAlani.classList.remove(
                "d-none"
            );
        }
    }


    document.addEventListener(
        "kategoriDegisti",
        function (olay) {
            const kategoriId =
                olay.detail.kategoriId;

            const yaprakKategoriMi =
                olay.detail.yaprakKategoriMi;

            if (
                !kategoriId
                || !yaprakKategoriMi
            ) {
                alanlariTemizle();
                return;
            }

            ozellikleriGetir(
                kategoriId
            );
        }
    );

    const gizliKategoriInput =
    document.getElementById("id_kategori");

if (
    gizliKategoriInput
    && gizliKategoriInput.value
) {
    ozellikleriGetir(
        gizliKategoriInput.value
    );
}
});