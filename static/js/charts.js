/**
 * EcoTrack — Chart.js Visualizations
 * Provides responsive doughnut and bar charts for waste categories and status distribution.
 */

// Category Palette matching our CSS badges
const CATEGORY_COLORS = {
    'Wet': '#16a34a',       // Forest Green
    'Dry': '#0284c7',       // Sky Blue
    'Plastic': '#d97706',   // Amber
    'E-waste': '#9333ea',   // Purple
    'Mixed': '#64748b',     // Slate
    'Other': '#0d9488'      // Teal
};

// Status Palette
const STATUS_COLORS = {
    'Reported': '#f59e0b',     // Amber
    'In Progress': '#3b82f6',  // Blue
    'Resolved': '#10b981',     // Emerald
    'Rejected': '#6b7280'      // Gray
};

function renderCategoryDoughnut(canvasId, labels, dataValues) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || !window.Chart) return;

    const backgroundColors = labels.map(label => CATEGORY_COLORS[label] || '#94a3b8');

    return new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: dataValues,
                backgroundColor: backgroundColors,
                borderWidth: 2,
                borderColor: '#ffffff',
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        padding: 14,
                        font: { family: 'Inter', size: 12 }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const val = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const pct = total > 0 ? ((val / total) * 100).toFixed(1) : 0;
                            return ` ${context.label}: ${val} (${pct}%)`;
                        }
                    }
                }
            },
            cutout: '65%'
        }
    });
}

function renderStatusBarChart(canvasId, labels, dataValues) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || !window.Chart) return;

    const backgroundColors = labels.map(label => STATUS_COLORS[label] || '#94a3b8');

    return new Chart(canvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Reports',
                data: dataValues,
                backgroundColor: backgroundColors,
                borderRadius: 6,
                maxBarThickness: 45
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
                    ticks: {
                        stepSize: 1,
                        font: { family: 'Inter', size: 11 }
                    },
                    grid: { color: '#f1f5f9' }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { family: 'Inter', size: 12 } }
                }
            }
        }
    });
}

