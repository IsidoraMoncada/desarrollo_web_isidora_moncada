fetch('/get_actividades_por_dia')
    .then(response => response.json())
    .then(data => {
        const fechas = data.fechas; // Fechas del JSON
        const cantidades = data.cantidades; // Cantidades del JSON

        Highcharts.chart('container', {
            title: {
                text: 'Cantidad de Actividades por Día en el Último Mes'
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
