$(document).ready(function(){
    $.get('static/data/rides_by_date.csv', function(csv){
        $('#chart1').highcharts({
            chart: {
                type: 'line',
                showAxes: true
            },
            data: {
                csv: csv
            },
            title: {
                text: 'Rides Over Time'
            },
            legend: {
                enabled: false
            },
            credits: {
                enabled: false
            },
            yAxis: {
                title: {
                    text: 'Rides'
                }
            },
            tooltip: {
                crosshairs: true,
                shared: true
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: false
                    },
                }
            }
        });
    });
    $.get('static/data/rides_by_month.csv', function(csv){
        $('#chart2').highcharts({
            chart: {
                type: 'line',
                showAxes: true
            },
            data: {
                csv: csv
            },
            title: {
                text: "Rides by Month"
            },
            legend: {
                enabled: false
            },
            credits: {
                enabled: false
            },
            yAxis: {
                title: {
                    text: 'Rides'
                }
            },
            tooltip: {
                crosshairs: true,
                shared: true
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: false
                    },
                }
            }
        });
    });
    $.get('static/data/rides_by_weekday.csv', function(csv){
        $('#chart3').highcharts({
            chart: {
                type: 'line',
                showAxes: true
            },
            data: {
                csv: csv
            },
            title: {
                text: "Rides by Weekday"
            },
            legend: {
                enabled: false
            },
            credits: {
                enabled: false
            },
            yAxis: {
                title: {
                    text: 'Rides'
                }
            },
            tooltip: {
                crosshairs: true,
                shared: true
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: false
                    },
                }
            }
        });
    });
    $.get('static/data/rides_by_hour.csv', function(csv){
        $('#chart4').highcharts({
            chart: {
                type: 'line',
                showAxes: true
            },
            data: {
                csv: csv
            },
            title: {
                text: "Rides by Hour"
            },
            legend: {
                enabled: false
            },
            credits: {
                enabled: false
            },
            yAxis: {
                title: {
                    text: 'Rides'
                }
            },
            xAxis: {
                labels: {
                    format: '{value}:00'
                }
            },
            tooltip: {
                crosshairs: true,
                shared: true
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: false
                    },
                }
            }
        });
    });

    Papa.parse($SCRIPT_ROOT + "/static/data/rides_by_neighborhood.csv", {
        download: true,
        header: true,
        skipEmptyLines: true,
        dynamicTyping: true,
        complete: function(results) {
            var data = results.data;

            $.getJSON('static/data/nycneighborhoods.geojson', function(map){
                $('#chart5').highcharts('Map', {
                    chart: {
                        type: 'map'
                    },
                    title: {
                        text: "Lyft Rides by Neighborhood"
                    },
                    mapNavigation: {
                        enabled: true,
                        buttonOptions: {
                            verticalAlign: 'bottom'
                        }
                    },
                    colorAxis: {
                        min: 0,
                        max: 6000
                    },
                    series: [{
                        data: (function (columnToBeUsed) {
                            var len = data.length,
                                tab = [];
                            for (var i = 0; i < len; i++) {
                                data[i].value = data[i][columnToBeUsed];
                            }
                            return data;
                        })('Lyft'),
                        mapData: map,
                        joinBy: ['neighborhood', 'Neighborhood'],
                        name: 'Rides',
                        tooltip: {
                            headerFormat: '',
                            pointFormat: '{point.Neighborhood}: <b>{point.value}</b>'
                        }
                    }],
                    credits: {
                        enabled: false
                    }
                });
            });

            $.getJSON('static/data/nycneighborhoods.geojson', function(map){
                $('#chart6').highcharts('Map', {
                    chart: {
                        type: 'map'
                    },
                    title: {
                        text: "Uber Rides by Neighborhood"
                    },
                    mapNavigation: {
                        enabled: true,
                        buttonOptions: {
                            verticalAlign: 'bottom'
                        }
                    },
                    colorAxis: {
                        min: 0,
                        max: 6000
                    },
                    series: [{
                        data: (function (columnToBeUsed) {
                            var len = data.length,
                                tab = [];
                            for (var i = 0; i < len; i++) {
                                data[i].value = data[i][columnToBeUsed];
                            }
                            return data;
                        })('Uber'),
                        mapData: map,
                        joinBy: ['neighborhood', 'Neighborhood'],
                        name: 'Rides',
                        tooltip: {
                            headerFormat: '',
                            pointFormat: '{point.Neighborhood}: <b>{point.value}</b>'
                        }
                    }],
                    credits: {
                        enabled: false
                    }
                });
            });
        }
    });

    Papa.parse($SCRIPT_ROOT + "/static/data/rides_by_borough.csv", {
        download: true,
        header: true,
        skipEmptyLines: true,
        dynamicTyping: true,
        complete: function(results) {
            var data = results.data;
            // console.log(data);
            $.getJSON('static/data/nycboroughs.geojson', function(map){
                $('#chart7').highcharts('Map', {
                    chart: {
                        type: 'map'
                    },
                    title: {
                        text: "Lyft Rides by Borough"
                    },
                    mapNavigation: {
                        enabled: true,
                        buttonOptions: {
                            verticalAlign: 'bottom'
                        }
                    },
                    colorAxis: {
                        min: 0,
                        max: 15000
                    },
                    series: [{
                        data: (function (columnToBeUsed) {
                            var len = data.length,
                                tab = [];
                            for (var i = 0; i < len; i++) {
                                data[i].value = data[i][columnToBeUsed];
                            }
                            return data;
                        })('Lyft'),
                        mapData: map,
                        joinBy: ['BoroName', 'Borough'],
                        name: 'Rides',
                        tooltip: {
                            headerFormat: '',
                            pointFormat: '{point.Borough}: <b>{point.value}</b>'
                        }
                    }],
                    credits: {
                        enabled: false
                    }
                });
            });

            $.getJSON('static/data/nycboroughs.geojson', function(map){
                $('#chart8').highcharts('Map', {
                    chart: {
                        type: 'map'
                    },
                    title: {
                        text: "Uber Rides by Borough"
                    },
                    mapNavigation: {
                        enabled: true,
                        buttonOptions: {
                            verticalAlign: 'bottom'
                        }
                    },
                    colorAxis: {
                        min: 0,
                        max: 15000
                    },
                    series: [{
                        data: (function (columnToBeUsed) {
                            var len = data.length,
                                tab = [];
                            for (var i = 0; i < len; i++) {
                                data[i].value = data[i][columnToBeUsed];
                            }
                            return data;
                        })('Uber'),
                        mapData: map,
                        joinBy: ['BoroName', 'Borough'],
                        name: 'Rides',
                        tooltip: {
                            headerFormat: '',
                            pointFormat: '{point.Borough}: <b>{point.value}</b>'
                        }
                    }],
                    credits: {
                        enabled: false
                    }
                });
            });
        }
    });
});