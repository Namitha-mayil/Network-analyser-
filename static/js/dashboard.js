document.addEventListener("DOMContentLoaded", function() {
    const statsDataElement = document.getElementById('stats-data');
    if (!statsDataElement) return;
    
    const stats = JSON.parse(statsDataElement.textContent);
    
    Chart.defaults.color = '#64748b';
    Chart.defaults.font.family = "'Inter', sans-serif";
    
    const hasData = stats.total_records > 0;
    
    // Traffic Distribution (Doughnut)
    const trafficCtx = document.getElementById('trafficChart');
    if (trafficCtx) {
        new Chart(trafficCtx, {
            type: 'doughnut',
            data: {
                labels: hasData ? ['Normal', 'Attack'] : ['No Data'],
                datasets: [{
                    data: hasData ? [stats.normal_count, stats.attack_count] : [1],
                    backgroundColor: hasData
                        ? ['#16a34a', '#dc2626']
                        : ['#e2e8f0'],
                    borderColor: hasData
                        ? ['#15803d', '#b91c1c']
                        : ['#cbd5e1'],
                    borderWidth: 2,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { padding: 20 }
                    },
                    tooltip: { enabled: hasData }
                },
                cutout: '65%'
            }
        });
    }

    // Attack Breakdown (Bar)
    const attackCtx = document.getElementById('attackChart');
    if (attackCtx) {
        new Chart(attackCtx, {
            type: 'bar',
            data: {
                labels: ['DoS', 'Probe', 'R2L', 'U2R'],
                datasets: [{
                    label: 'Count',
                    data: [stats.dos_count, stats.probe_count, stats.r2l_count, stats.u2r_count],
                    backgroundColor: [
                        '#dc2626',
                        '#d97706',
                        '#2563eb',
                        '#7c3aed'
                    ],
                    borderColor: [
                        '#b91c1c',
                        '#b45309',
                        '#1d4ed8',
                        '#6d28d9'
                    ],
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: { color: '#f1f5f9' },
                        ticks: { precision: 0 }
                    },
                    x: {
                        grid: { display: false }
                    }
                }
            }
        });
    }
});
