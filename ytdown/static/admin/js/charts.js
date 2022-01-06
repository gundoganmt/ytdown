const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
"Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

var beginning = new Date(f_dw);
var today = new Date();
var mDate = new Date(new Date().setDate(today.getDate()+30));

var daysOfMonths = [];
for (; beginning <= mDate; beginning.setDate(beginning.getDate() + 1)) {
    dateString = beginning.getDate() + ' ' + monthNames[beginning.getMonth()]
    daysOfMonths.push(dateString);
    if (today > mDate){
      mDate.setDate(mDate.getDate()+1);
    }
}

var options = {
    chart: {
        height: 420,
        type: "area",
        fontFamily: 'Inter',
        foreColor: '#4B5563',
        toolbar: {
            show: true,
            offsetX: 0,
            offsetY: 0,
            tools: {
                download: false,
                selection: false,
                zoom: false,
                zoomin: true,
                zoomout: true,
                pan: false,
                reset: false | '<img src="/static/icons/reset.png" width="20">',
                customIcons: []
            },
            export: {
                csv: {
                    filename: undefined,
                    columnDelimiter: ',',
                    headerCategory: 'category',
                    headerValue: 'value',
                    dateFormatter(timestamp) {
                        return new Date(timestamp).toDateString()
                    }
                }
            },
            autoSelected: 'zoom'
        },
    },
    dataLabels: {
        enabled: false
    },
    tooltip: {
        style: {
            fontSize: '14px',
            fontFamily: 'Inter',
        },
    },
    theme: {
        monochrome: {
            enabled: true,
            color: '#f3c78e',
        }
    },
    grid: {
        show: true,
        borderColor: '#f5e1c5',
        strokeDashArray: 1,
    },
    series: [{
        name: "Sales",
        data: data
    }],
    markers: {
        size: 5,
        strokeColors: '#ffffff',
        hover: {
            size: undefined,
            sizeOffset: 3
        }
    },
    xaxis: {
        categories: daysOfMonths,
        tickAmount: 30,
        labels: {
            style: {
                fontSize: '12px',
                fontWeight: 500,
            },
        },
        axisBorder: {
            color: '#f5e1c5',
        },
        axisTicks: {
            color: '#f5e1c5',
        }
    },
    yaxis: {
        labels: {
            style: {
                colors: ['#4B5563'],
                fontSize: '12px',
                fontWeight: 500,
            },
        },
    },
    responsive: [{
        breakpoint: 768,
        options: {
            yaxis: {
                show: false,
            }
        }
    }]
};

var chart = new ApexCharts(document.querySelector("#chart"), options);
if (document.getElementById('chart')) {
    chart.render();
}

// Total Orders Chart
var optionsAppRankingChart = {
    series: [{
        name: 'Travel & Local',
        data: source_data
    }],
    chart: {
        type: 'bar',
        height: '400px',
        fontFamily: 'Inter',
        foreColor: '#4B5563',
    },
    colors: ['#f0bc74', '#31316A'],
    plotOptions: {
        bar: {
            horizontal: false,
            columnWidth: '40%',
            borderRadius: 10,
            colors: {
                backgroundBarColors: ['#fff'],
                backgroundBarOpacity: .2,
                backgroundBarRadius: 10,
            },
        },
    },
    grid: {
        show: false,
    },
    dataLabels: {
        enabled: false
    },
    legend: {
        show: true,
        fontSize: '14px',
        fontFamily: 'Inter',
        fontWeight: 500,
        height: 40,
        tooltipHoverFormatter: undefined,
        offsetY: 10,
        markers: {
            width: 14,
            height: 14,
            strokeWidth: 1,
            strokeColor: '#ffffff',
            radius: 50,
        },
    },
    stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
    },
    xaxis: {
        categories: ['Youtube', 'Twitter', 'Instagram', 'Vlive', 'Vimeo', 'SoundCloud', 'Izlesene'],
        labels: {
            style: {
                fontSize: '12px',
                fontWeight: 500,
            },
        },
        axisBorder: {
            color: '#EBE3EE',
        },
        axisTicks: {
            color: '#f1f1f1',
        }
    },
    yaxis: {
        show: false,
    },
    fill: {
        opacity: 1
    },
    responsive: [{
        breakpoint: 1499,
        options: {
            chart: {
                height: '400px',
            },
        },
    }]
};

var appRankingChartEl = document.getElementById('chart-app-ranking');
if (appRankingChartEl) {
    var appRankingChart = new ApexCharts(appRankingChartEl, optionsAppRankingChart);
    appRankingChart.render();
}
