fetch('/get_actividades_por_dia')
    .then(response => response.json())
    .then(data => {
        const fechas = data.fechas; // Fechas del JSON
        const cantidades = data.cantidades; // Cantidades del JSON

        Highcharts.chart('container', {
            title: {
                text: 'Cantidad de actividades por día.'
            },
            xAxis: {
                categories: fechas.map(fecha => new Date(fecha).toLocaleDateString()) // Formatear la fecha
            },
            yAxis: {
                title: {
                    text: 'Cantidad de Actividades'
                }
            },
            series: [{
                name: 'Actividades',
                data: cantidades,
                color: '#715331'
            }]
        });
    })
    .catch(error => console.error('Error al obtener los datos:', error));

    fetch('/get_n_actividades_por_tipo')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        const temas = data.temas; // Temas del JSON
        const cantidades = data.cantidades; // Cantidades del JSON

        Highcharts.chart('container-torta', {
            colors: ['#715331','#7f6446','#8d755a','#9c876f','#aa9883','#b8a998','#c6baad','#d4cbc1','#e3ddd6','#664b2c'],
            chart: {
                type: 'pie'
            },
            title: {
                text: 'Cantidad total de actividades por tipo.'
            },
            series: [{
                name: 'Actividades',
                data: temas.map((tema, index) => ({
                    name: tema,
                    y: cantidades[index]
                })),
                showInLegend: true,
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.percentage:.1f} %'
                }
            }],
            tooltip: {
                pointFormat: '{series.name}: <b>{point.y}</b> ({point.percentage:.1f} %)'
            }
        });
    })
    .catch(error => console.error('Error al obtener los datos:', error));

