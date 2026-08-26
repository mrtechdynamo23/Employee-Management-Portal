/* ============================================
   EMPLOYEEHUB — DASHBOARD JS
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    // Load dashboard charts if we're on the dashboard page
    const perfTrendChart = document.getElementById('perfTrendChart');
    if (perfTrendChart) {
        loadDashboardCharts();
    }
});

function loadDashboardCharts() {
    fetch('/dashboard/charts')
        .then(response => response.json())
        .then(data => {
            createPerformanceTrendChart(data.performance_trend);
            createTaskDistributionChart(data.task_distribution);
            createDepartmentPerformanceChart(data.department_performance);
            createAttendanceTrendChart(data.attendance_trend);
        })
        .catch(err => console.log('Chart data loading...', err));
}

function createPerformanceTrendChart(data) {
    const ctx = document.getElementById('perfTrendChart');
    if (!ctx || !data) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Avg Performance Score',
                data: data.data,
                borderColor: '#6366F1',
                backgroundColor: createGradient(ctx, '#6366F1'),
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: '#6366F1',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                borderWidth: 2.5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1E293B',
                    titleFont: { family: 'Inter' },
                    bodyFont: { family: 'Inter' },
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: (context) => `Performance: ${context.parsed.y}%`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: 60,
                    grid: { color: 'rgba(0,0,0,0.04)' },
                    ticks: { font: { family: 'Inter', size: 11 }, callback: v => v + '%' }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { family: 'Inter', size: 11 } }
                }
            }
        }
    });
}

function createTaskDistributionChart(data) {
    const ctx = document.getElementById('taskDistChart');
    if (!ctx || !data) return;

    const colors = {
        'To Do': '#6B7280',
        'In Progress': '#6366F1',
        'Under Review': '#F59E0B',
        'Completed': '#10B981',
        'Overdue': '#EF4444'
    };

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.labels,
            datasets: [{
                data: data.data,
                backgroundColor: data.labels.map(l => colors[l] || '#6B7280'),
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        boxWidth: 12,
                        padding: 15,
                        font: { family: 'Inter', size: 11 },
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: '#1E293B',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: (context) => `${context.label}: ${context.parsed} tasks`
                    }
                }
            }
        }
    });
}

function createDepartmentPerformanceChart(data) {
    const ctx = document.getElementById('deptPerfChart');
    if (!ctx || !data) return;

    const deptColors = ['#6366F1', '#8B5CF6', '#10B981', '#F59E0B', '#3B82F6'];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Avg Performance',
                data: data.data,
                backgroundColor: deptColors.slice(0, data.labels.length),
                borderRadius: 8,
                maxBarThickness: 50
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1E293B',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: (context) => `Avg: ${context.parsed.y}%`
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    min: 60,
                    grid: { color: 'rgba(0,0,0,0.04)' },
                    ticks: { font: { family: 'Inter', size: 11 }, callback: v => v + '%' }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { family: 'Inter', size: 10 } }
                }
            }
        }
    });
}

function createAttendanceTrendChart(data) {
    const ctx = document.getElementById('attTrendChart');
    if (!ctx || !data) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Attendance Rate',
                data: data.data,
                borderColor: '#10B981',
                backgroundColor: createGradient(ctx, '#10B981'),
                fill: true,
                tension: 0.4,
                pointRadius: 4,
                pointBackgroundColor: '#10B981',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                borderWidth: 2.5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1E293B',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: (context) => `Attendance: ${context.parsed.y}%`
                    }
                }
            },
            scales: {
                y: {
                    min: 80,
                    max: 100,
                    grid: { color: 'rgba(0,0,0,0.04)' },
                    ticks: { font: { family: 'Inter', size: 11 }, callback: v => v + '%' }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { family: 'Inter', size: 11 } }
                }
            }
        }
    });
}

function createGradient(ctx, color) {
    const canvas = ctx.getContext ? ctx : ctx.canvas || ctx;
    const context = canvas.getContext ? canvas.getContext('2d') : null;
    if (!context) return color + '20';

    try {
        const gradient = context.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, color + '30');
        gradient.addColorStop(1, color + '05');
        return gradient;
    } catch {
        return color + '20';
    }
}

// Global search
const globalSearch = document.getElementById('globalSearch');
if (globalSearch) {
    let searchTimeout;
    globalSearch.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const query = e.target.value.trim();
            if (query.length >= 2) {
                window.location.href = `/employees?search=${encodeURIComponent(query)}`;
            }
        }, 500);
    });
}
