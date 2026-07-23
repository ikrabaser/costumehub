console.log("CostumeHub JavaScript dosyası çalışıyor.");
const chartCanvas = document.getElementById("ilanChart");
const chartLabelsElement = document.getElementById(
    "ilan-chart-labels"
);
const chartDataElement = document.getElementById(
    "ilan-chart-data"
);

if (
    chartCanvas
    && chartLabelsElement
    && chartDataElement
    && typeof Chart !== "undefined"
) {
    const chartLabels = JSON.parse(
        chartLabelsElement.textContent
    );

    const chartData = JSON.parse(
        chartDataElement.textContent
    );

    new Chart(chartCanvas, {
        type: "line",

        data: {
            labels: chartLabels,

            datasets: [
                {
                    label: "Yeni İlan",
                    data: chartData,
                    borderColor: "#6f4cff",
                    backgroundColor: "rgba(111, 76, 255, 0.14)",
                    borderWidth: 3,
                    pointRadius: 4,
                    pointHoverRadius: 6,
                    tension: 0.35,
                    fill: true,
                },
            ],
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            interaction: {
                intersect: false,
                mode: "index",
            },

            plugins: {
                legend: {
                    display: false,
                },

                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return (
                                context.parsed.y
                                + " yeni ilan"
                            );
                        },
                    },
                },
            },

            scales: {
                y: {
                    beginAtZero: true,

                    ticks: {
                        precision: 0,
                        stepSize: 1,
                    },
                },

                x: {
                    grid: {
                        display: false,
                    },
                },
            },
        },
    });
}
const talepChartCanvas = document.getElementById(
    "talepDurumChart"
);

const talepLabelsElement = document.getElementById(
    "talep-chart-labels"
);

const talepDataElement = document.getElementById(
    "talep-chart-data"
);

if (
    talepChartCanvas
    && talepLabelsElement
    && talepDataElement
    && typeof Chart !== "undefined"
) {
    const talepLabels = JSON.parse(
        talepLabelsElement.textContent
    );

    const talepData = JSON.parse(
        talepDataElement.textContent
    );

    const toplamTalep = talepData.reduce(
        (toplam, sayi) => toplam + sayi,
        0
    );

    const gosterilenEtiketler = toplamTalep > 0
        ? talepLabels
        : ["Henüz talep yok"];

    const gosterilenVeriler = toplamTalep > 0
        ? talepData
        : [1];

    const grafikRenkleri = toplamTalep > 0
        ? [
            "#f6c453",
            "#6f4cff",
            "#4f7cff",
            "#34a0a4",
            "#3bb273",
            "#ef6f6c",
            "#9aa0aa",
        ]
        : ["#e7e7ee"];

    new Chart(talepChartCanvas, {
        type: "doughnut",

        data: {
            labels: gosterilenEtiketler,

            datasets: [
                {
                    data: gosterilenVeriler,
                    backgroundColor: grafikRenkleri,
                    borderWidth: 0,
                    hoverOffset: 6,
                },
            ],
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "68%",

            plugins: {
                legend: {
                    position: "bottom",

                    labels: {
                        usePointStyle: true,
                        boxWidth: 8,
                        padding: 14,
                    },
                },

                tooltip: {
                    enabled: toplamTalep > 0,

                    callbacks: {
                        label: function (context) {
                            return (
                                context.label
                                + ": "
                                + context.parsed
                                + " talep"
                            );
                        },
                    },
                },
            },
        },
    });
}


const kategoriChartCanvas = document.getElementById(
    "kategoriChart"
);

const kategoriLabelsElement = document.getElementById(
    "kategori-chart-labels"
);

const kategoriDataElement = document.getElementById(
    "kategori-chart-data"
);

if (
    kategoriChartCanvas
    && kategoriLabelsElement
    && kategoriDataElement
    && typeof Chart !== "undefined"
) {
    const kategoriLabels = JSON.parse(
        kategoriLabelsElement.textContent
    );

    const kategoriData = JSON.parse(
        kategoriDataElement.textContent
    );

    const veriVarMi = kategoriData.length > 0;

    new Chart(kategoriChartCanvas, {
        type: "bar",

        data: {
            labels: veriVarMi
                ? kategoriLabels
                : ["Henüz ilan yok"],

            datasets: [
                {
                    label: "İlan Sayısı",

                    data: veriVarMi
                        ? kategoriData
                        : [0],

                    backgroundColor: "rgba(111, 76, 255, 0.72)",
                    borderColor: "#6f4cff",
                    borderWidth: 1,
                    borderRadius: 8,
                    maxBarThickness: 52,
                },
            ],
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                legend: {
                    display: false,
                },

                tooltip: {
                    enabled: veriVarMi,

                    callbacks: {
                        label: function (context) {
                            return (
                                context.parsed.y
                                + " ilan"
                            );
                        },
                    },
                },
            },

            scales: {
                y: {
                    beginAtZero: true,

                    ticks: {
                        precision: 0,
                        stepSize: 1,
                    },
                },

                x: {
                    grid: {
                        display: false,
                    },

                    ticks: {
                        maxRotation: 30,
                        minRotation: 0,
                    },
                },
            },
        },
    });
}
