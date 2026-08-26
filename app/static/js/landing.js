/* ============================================
   EMPLOYEEHUB — LANDING PAGE JS
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    // Navbar scroll effect
    const nav = document.getElementById('mainNav');
    if (nav) {
        window.addEventListener('scroll', () => {
            nav.classList.toggle('scrolled', window.scrollY > 50);
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = 80;
                const position = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top: position, behavior: 'smooth' });
            }
        });
    });

    // Counter animation
    const counters = document.querySelectorAll('.metric-number');
    let countersAnimated = false;

    function animateCounters() {
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target'));
            const duration = 2000;
            const start = 0;
            const startTime = performance.now();

            function updateCounter(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const eased = 1 - Math.pow(1 - progress, 3); // easeOutCubic
                const current = Math.round(start + (target - start) * eased);
                counter.textContent = current.toLocaleString();
                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                }
            }
            requestAnimationFrame(updateCounter);
        });
    }

    // Intersection Observer for counters
    if (counters.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !countersAnimated) {
                    countersAnimated = true;
                    animateCounters();
                }
            });
        }, { threshold: 0.5 });

        const metricStrip = document.querySelector('.metric-strip');
        if (metricStrip) observer.observe(metricStrip);
    }

    // Scroll reveal animations
    const revealElements = document.querySelectorAll('.scroll-reveal');
    if (revealElements.length > 0) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.classList.add('visible');
                    }, index * 100);
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        revealElements.forEach(el => revealObserver.observe(el));
    }

    // Demo score animation
    const demoScore = document.getElementById('demoScore');
    if (demoScore) {
        const scoreObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    let current = 0;
                    const target = 93.4;
                    const increment = target / 60;
                    const timer = setInterval(() => {
                        current += increment;
                        if (current >= target) {
                            current = target;
                            clearInterval(timer);
                        }
                        demoScore.textContent = current.toFixed(1) + '%';
                    }, 30);
                    scoreObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        scoreObserver.observe(demoScore);
    }

    // Landing page showcase charts
    initShowcaseCharts();
    initAnalyticsPreviewCharts();
});

function initShowcaseCharts() {
    const showcaseCtx = document.getElementById('showcaseChart');
    if (showcaseCtx) {
        new Chart(showcaseCtx, {
            type: 'line',
            data: {
                labels: ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
                datasets: [{
                    label: 'Performance',
                    data: [82, 85, 83, 87, 89, 91],
                    borderColor: '#6366F1',
                    backgroundColor: 'rgba(99,102,241,0.1)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 3,
                    pointBackgroundColor: '#6366F1',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: false, min: 75, max: 95, grid: { color: 'rgba(0,0,0,0.05)' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    const pieCtx = document.getElementById('showcasePie');
    if (pieCtx) {
        new Chart(pieCtx, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'In Progress', 'To Do', 'Overdue'],
                datasets: [{
                    data: [65, 20, 10, 5],
                    backgroundColor: ['#10B981', '#6366F1', '#F59E0B', '#EF4444'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                cutout: '65%',
                plugins: { legend: { display: false } }
            }
        });
    }
}

function initAnalyticsPreviewCharts() {
    // Performance Trend
    const perfCtx = document.getElementById('analyticsPerfTrend');
    if (perfCtx) {
        new Chart(perfCtx, {
            type: 'line',
            data: {
                labels: ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
                datasets: [{
                    label: 'Avg Performance',
                    data: [81, 83, 82, 86, 88, 90],
                    borderColor: '#6366F1',
                    backgroundColor: 'rgba(99,102,241,0.1)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 2
                }]
            },
            options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { min: 75, max: 95 } } }
        });
    }

    // Task Distribution
    const taskCtx = document.getElementById('analyticsTaskDist');
    if (taskCtx) {
        new Chart(taskCtx, {
            type: 'doughnut',
            data: {
                labels: ['Completed', 'In Progress', 'To Do', 'Under Review', 'Overdue'],
                datasets: [{
                    data: [60, 18, 10, 7, 5],
                    backgroundColor: ['#10B981', '#6366F1', '#6B7280', '#F59E0B', '#EF4444'],
                    borderWidth: 0
                }]
            },
            options: { responsive: true, cutout: '60%', plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 10 } } } } }
        });
    }

    // Department Performance
    const deptCtx = document.getElementById('analyticsDeptPerf');
    if (deptCtx) {
        new Chart(deptCtx, {
            type: 'bar',
            data: {
                labels: ['IT', 'HR', 'Finance', 'Marketing', 'Operations'],
                datasets: [{
                    label: 'Avg Score',
                    data: [88, 85, 82, 86, 84],
                    backgroundColor: ['#6366F1', '#8B5CF6', '#10B981', '#F59E0B', '#3B82F6'],
                    borderRadius: 8,
                    maxBarThickness: 40
                }]
            },
            options: { responsive: true, plugins: { legend: { display: false } }, scales: { y: { min: 70, max: 95 } } }
        });
    }
}
