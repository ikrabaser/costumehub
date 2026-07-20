document.addEventListener("DOMContentLoaded", function () {
    const form =
        document.getElementById("ilan-filtre-formu");

    const dinamikFiltreAlani =
        document.getElementById("dinamik-filtre-alani");

    const hizliFiltreAlani =
        document.getElementById("dinamik-hizli-filtreler");

    const hizliFiltreListesi =
        document.querySelector(".hizli-filtre-listesi");

    const gizliKategoriInput =
        document.getElementById("id_kategori");

    const urlSablonu =
        window.kategoriOzellikleriUrlSablonu || "";

    if (
        !form
        || !dinamikFiltreAlani
        || !hizliFiltreAlani
        || !hizliFiltreListesi
        || !urlSablonu
    ) {
        return;
    }


    /* ----------------------------------------
       Hızlı filtre açılır paneli
    ---------------------------------------- */

    const panel =
        document.createElement("div");

    panel.id = "hizli-filtre-acilir-panel";
    panel.className = "hizli-filtre-acilir-panel d-none";

    const aramaAlani =
        document.querySelector(".ilan-arama-alani");

    aramaAlani.appendChild(panel);


    const stil =
        document.createElement("style");

    stil.textContent = `
        .ilan-arama-alani {
            position: relative;
        }

        .hizli-filtre-acilir-panel {
            position: absolute;
            z-index: 1050;
            top: calc(100% - 12px);
            left: 20px;
            width: min(420px, calc(100% - 40px));
            padding: 18px;
            border: 1px solid #e3e6e8;
            border-radius: 18px;
            background: #ffffff;
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.16);
        }

        .hizli-filtre-panel-baslik {
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .hizli-filtre-panel-aciklama {
            margin-bottom: 16px;
            color: #6c757d;
            font-size: 0.86rem;
        }

        .hizli-filtre-secenekleri {
            display: flex;
            flex-wrap: wrap;
            gap: 9px;
            max-height: 245px;
            overflow-y: auto;
        }

        .hizli-filtre-secenegi {
            padding: 9px 14px;
            border: 1px solid #dee2e6;
            border-radius: 999px;
            background: #ffffff;
            color: #212529;
            font-size: 0.9rem;
            font-weight: 600;
            transition: 0.15s;
        }

        .hizli-filtre-secenegi:hover {
            border-color: #212529;
        }

        .hizli-filtre-secenegi.secili {
            border-color: #ffc107;
            background: #fff3cd;
        }

        .hizli-filtre-panel-alt {
            display: flex;
            justify-content: flex-end;
            gap: 9px;
            margin-top: 18px;
            padding-top: 14px;
            border-top: 1px solid #eceff1;
        }

        .hizli-filtre-panel-girdi {
            min-height: 46px;
            border-radius: 12px;
        }

        @media (max-width: 767.98px) {
            .hizli-filtre-acilir-panel {
                position: fixed;
                top: auto;
                right: 0;
                bottom: 0;
                left: 0;
                width: 100%;
                max-height: 72vh;
                overflow-y: auto;
                border-radius: 22px 22px 0 0;
                padding: 22px 18px;
            }
        }
    `;

    document.head.appendChild(stil);


    function paneliKapat() {
        panel.classList.add("d-none");
        panel.innerHTML = "";
    }


    function panelIskeletiOlustur(
        baslik,
        aciklama
    ) {
        panel.innerHTML = "";

        const baslikAlani =
            document.createElement("div");

        baslikAlani.className =
            "hizli-filtre-panel-baslik";

        baslikAlani.textContent = baslik;

        const aciklamaAlani =
            document.createElement("div");

        aciklamaAlani.className =
            "hizli-filtre-panel-aciklama";

        aciklamaAlani.textContent = aciklama;

        panel.appendChild(baslikAlani);
        panel.appendChild(aciklamaAlani);

        panel.classList.remove("d-none");
    }


    function panelAltButonlariniEkle(
        temizleIslemi
    ) {
        const altAlan =
            document.createElement("div");

        altAlan.className =
            "hizli-filtre-panel-alt";

        const temizleButonu =
            document.createElement("button");

        temizleButonu.type = "button";
        temizleButonu.className =
            "btn btn-outline-secondary";

        temizleButonu.textContent = "Temizle";

        temizleButonu.addEventListener(
            "click",
            function () {
                temizleIslemi();
            }
        );

        const uygulaButonu =
            document.createElement("button");

        uygulaButonu.type = "button";
        uygulaButonu.className =
            "btn btn-dark px-4";

        uygulaButonu.textContent = "Uygula";

        uygulaButonu.addEventListener(
            "click",
            function () {
                form.submit();
            }
        );

        altAlan.appendChild(temizleButonu);
        altAlan.appendChild(uygulaButonu);
        panel.appendChild(altAlan);
    }


    function secenekPaneliAc(
        baslik,
        aciklama,
        select
    ) {
        panelIskeletiOlustur(
            baslik,
            aciklama
        );

        const secenekAlani =
            document.createElement("div");

        secenekAlani.className =
            "hizli-filtre-secenekleri";

        Array.from(select.options).forEach(
            function (option) {
                if (!option.value) {
                    return;
                }

                const secenekButonu =
                    document.createElement("button");

                secenekButonu.type = "button";
                secenekButonu.className =
                    "hizli-filtre-secenegi";

                secenekButonu.textContent =
                    option.textContent;

                if (
                    String(select.value)
                    === String(option.value)
                ) {
                    secenekButonu.classList.add(
                        "secili"
                    );
                }

                secenekButonu.addEventListener(
                    "click",
                    function () {
                        select.value = option.value;

                        secenekAlani
                            .querySelectorAll(
                                ".hizli-filtre-secenegi"
                            )
                            .forEach(
                                function (buton) {
                                    buton.classList.remove(
                                        "secili"
                                    );
                                }
                            );

                        secenekButonu.classList.add(
                            "secili"
                        );
                    }
                );

                secenekAlani.appendChild(
                    secenekButonu
                );
            }
        );

        panel.appendChild(secenekAlani);

        panelAltButonlariniEkle(
            function () {
                select.value = "";
                secenekAlani
                    .querySelectorAll(
                        ".hizli-filtre-secenegi"
                    )
                    .forEach(
                        function (buton) {
                            buton.classList.remove(
                                "secili"
                            );
                        }
                    );
            }
        );
    }


    function girdiPaneliAc(
        baslik,
        aciklama,
        asilInput,
        tip,
        placeholder
    ) {
        panelIskeletiOlustur(
            baslik,
            aciklama
        );

        const input =
            document.createElement("input");

        input.type = tip;
        input.className =
            "form-control hizli-filtre-panel-girdi";

        input.placeholder = placeholder;
        input.value = asilInput.value;

        if (tip === "number") {
            input.min = "0";
            input.step = "0.01";
        }

        input.addEventListener(
            "input",
            function () {
                asilInput.value = input.value;
            }
        );

        panel.appendChild(input);

        window.setTimeout(
            function () {
                input.focus();
            },
            50
        );

        panelAltButonlariniEkle(
            function () {
                input.value = "";
                asilInput.value = "";
            }
        );
    }


    /* ----------------------------------------
       Dinamik kategori özellikleri
    ---------------------------------------- */

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
        paneliKapat();
    }


    function etiketOlustur(ozellik) {
        const etiket =
            document.createElement("label");

        etiket.className =
            "form-label fw-semibold";

        etiket.htmlFor =
            `filtre_ozellik_${ozellik.id}`;

        etiket.textContent = ozellik.ad;

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
                    document.createElement("option");

                option.value = secenek.id;
                option.textContent = secenek.deger;

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
            ["", "Tümü"],
            ["EVET", "Evet"],
            ["HAYIR", "Hayır"],
        ];

        const seciliDeger =
            seciliDegeriGetir(ozellik.id);

        secenekler.forEach(
            function (secenek) {
                const option =
                    document.createElement("option");

                option.value = secenek[0];
                option.textContent = secenek[1];

                if (
                    option.value === seciliDeger
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


    function dinamikHizliButonOlustur(
        ozellik,
        alan
    ) {
        const buton =
            document.createElement("button");

        buton.type = "button";
        buton.className =
            "hizli-filtre-butonu";

        if (alan.value) {
            buton.classList.add("aktif");
        }

        const seciliMetin =
            alan.tagName === "SELECT"
            && alan.value
                ? alan.options[
                    alan.selectedIndex
                ].textContent
                : "";

        buton.textContent =
            seciliMetin
                ? `${ozellik.ad}: ${seciliMetin}`
                : `${ozellik.ad} ⌄`;

        buton.addEventListener(
            "click",
            function (olay) {
                olay.stopPropagation();

                if (alan.tagName === "SELECT") {
                    secenekPaneliAc(
                        ozellik.ad,
                        `${ozellik.ad} seçeneğini belirle.`,
                        alan
                    );
                } else {
                    girdiPaneliAc(
                        ozellik.ad,
                        `${ozellik.ad} değerini gir.`,
                        alan,
                        alan.type,
                        alan.placeholder
                    );
                }
            }
        );

        return buton;
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
            alan = secimAlaniOlustur(ozellik);
        } else if (
            ozellik.veri_tipi === "EVET_HAYIR"
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

        return {
            kapsayici: kapsayici,
            alan: alan,
        };
    }


    function ozellikleriGoster(ozellikler) {
        alanlariTemizle();

        const filtrelenebilirOzellikler =
            ozellikler.filter(
                function (ozellik) {
                    return (
                        ozellik.filtrelenebilir_mi
                        === true
                    );
                }
            );

        filtrelenebilirOzellikler.forEach(
            function (ozellik) {
                const filtreBilgisi =
                    filtreAlaniOlustur(
                        ozellik
                    );

                dinamikFiltreAlani.appendChild(
                    filtreBilgisi.kapsayici
                );

                hizliFiltreAlani.appendChild(
                    dinamikHizliButonOlustur(
                        ozellik,
                        filtreBilgisi.alan
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

            const veri = await cevap.json();

            ozellikleriGoster(
                veri.ozellikler || []
            );
        } catch (hata) {
            console.error(hata);
            alanlariTemizle();
        }
    }


    /* ----------------------------------------
       Sabit hızlı filtre butonları
    ---------------------------------------- */

    function butonuMetneGoreBul(metin) {
        return Array.from(
            document.querySelectorAll(
                ".hizli-filtre-butonu"
            )
        ).find(
            function (buton) {
                return buton.textContent
                    .trim()
                    .startsWith(metin);
            }
        );
    }


    const filtreleButonu =
        butonuMetneGoreBul("⚙")
        || butonuMetneGoreBul("Filtrele");

    const kategoriButonu =
        butonuMetneGoreBul("Kategori");

    const bedenButonu =
        butonuMetneGoreBul("Beden");

    const sehirButonu =
        butonuMetneGoreBul("Şehir");

    const fiyatButonu =
        butonuMetneGoreBul("Fiyat");

    const bedenSelect =
        document.getElementById("beden");

    const sehirInput =
        document.getElementById("sehir");

    const fiyatInput =
        document.getElementById(
            "maksimum_fiyat"
        );
        if (fiyatButonu && fiyatInput.value) {
            fiyatButonu.innerHTML =
                `Fiyat: ${fiyatInput.value} TL <span>⌄</span>`;
        
            fiyatButonu.classList.add("aktif");
        }
        if (
            bedenButonu &&
            bedenSelect &&
            bedenSelect.value
        ) {
            bedenButonu.innerHTML =
                `Beden: ${
                    bedenSelect.options[
                        bedenSelect.selectedIndex
                    ].text
                } <span>⌄</span>`;
        
            bedenButonu.classList.add("aktif");
        }
        if (
            sehirButonu &&
            sehirInput &&
            sehirInput.value
        ) {
            sehirButonu.innerHTML =
                `Şehir: ${sehirInput.value} <span>⌄</span>`;
        
            sehirButonu.classList.add("aktif");
        }


    if (bedenButonu && bedenSelect) {
        bedenButonu.removeAttribute(
            "data-bs-toggle"
        );

        bedenButonu.removeAttribute(
            "data-bs-target"
        );

        bedenButonu.addEventListener(
            "click",
            function (olay) {
                olay.stopPropagation();

                secenekPaneliAc(
                    "Beden",
                    "Aradığın kostümün bedenini seç.",
                    bedenSelect
                );
            }
        );
    }


    if (sehirButonu && sehirInput) {
        sehirButonu.removeAttribute(
            "data-bs-toggle"
        );

        sehirButonu.removeAttribute(
            "data-bs-target"
        );

        sehirButonu.addEventListener(
            "click",
            function (olay) {
                olay.stopPropagation();

                girdiPaneliAc(
                    "Şehir",
                    "İlanların bulunduğu şehri yaz.",
                    sehirInput,
                    "text",
                    "Örn. Ankara"
                );
            }
        );
    }


    if (fiyatButonu && fiyatInput) {
        fiyatButonu.removeAttribute(
            "data-bs-toggle"
        );

        fiyatButonu.removeAttribute(
            "data-bs-target"
        );

        fiyatButonu.addEventListener(
            "click",
            function (olay) {
                olay.stopPropagation();

                girdiPaneliAc(
                    "En yüksek fiyat",
                    "Günlük ödemek istediğin en yüksek tutarı gir.",
                    fiyatInput,
                    "number",
                    "Örn. 500"
                );
            }
        );
    }


    /*
       Kategori hiyerarşik olduğu için Kategori butonu
       gelişmiş paneli açmaya devam eder.
    */

    [filtreleButonu, kategoriButonu]
        .filter(Boolean)
        .forEach(
            function (buton) {
                buton.addEventListener(
                    "click",
                    function () {
                        paneliKapat();
                    }
                );
            }
        );


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


    document.addEventListener(
        "click",
        function (olay) {
            if (
                !panel.contains(olay.target)
                && !olay.target.closest(
                    ".hizli-filtre-butonu"
                )
            ) {
                paneliKapat();
            }
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