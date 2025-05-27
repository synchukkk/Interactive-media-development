let isAnimationPaused = false;
let soundEnabled = true;
let currentYear = 2020;

// Дані для різних років
const yearData = {
    2020: { solar: 35, wind: 40, other: 25 },
    2021: { solar: 40, wind: 38, other: 22 },
    2022: { solar: 42, wind: 36, other: 22 },
    2023: { solar: 44, wind: 36, other: 20 },
    2024: { solar: 45, wind: 35, other: 20 }
};

// Ініціалізація при завантаженні сторінки
document.addEventListener('DOMContentLoaded', function() {
    initScrollAnimation();
    initTooltips();
    animateNumbers();
    updateProgressBar();
    initTouchGestures();
    initKeyboardControls();
});

// Анімація чисел при появі елементів
function animateNumbers() {
    const numbers = document.querySelectorAll('.stat-number');
    numbers.forEach(number => {
        const target = parseFloat(number.getAttribute('data-target'));
        const increment = target / 100;
        let current = 0;
        
        const timer = setInterval(() => {
            if (isAnimationPaused) return;
            
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            number.textContent = current.toFixed(1);
        }, 30);
    });
}

// Скролл-анімація для секцій
function initScrollAnimation() {
    const sections = document.querySelectorAll('.section');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.3 });

    sections.forEach(section => observer.observe(section));
}

// Система підказок
function initTooltips() {
    const tooltip = Utils.DOM.$('#tooltip');
    const elements = Utils.DOM.$('[data-tooltip]');

    elements.forEach(element => {
        element.addEventListener('mouseenter', (e) => {
            tooltip.textContent = e.target.getAttribute('data-tooltip');
            Utils.Animation.fadeIn(tooltip, 200);
        });

        element.addEventListener('mousemove', Utils.Time.throttle((e) => {
            tooltip.style.left = e.pageX + 15 + 'px';
            tooltip.style.top = e.pageY - 10 + 'px';
        }, 16));

        element.addEventListener('mouseleave', () => {
            Utils.Animation.fadeOut(tooltip, 200);
        });
    });
}

// Індикатор прогресу з debounce для оптимізації
function updateProgressBar() {
    const updateProgress = Utils.Time.throttle(() => {
        const scrolled = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
        const clampedProgress = Utils.Math.clamp(scrolled, 0, 100);
        Utils.DOM.$('#progressBar').style.width = clampedProgress + '%';
    }, 16);
    
    window.addEventListener('scroll', updateProgress);
}

// Управління анімацією
function toggleAnimation() {
    isAnimationPaused = !isAnimationPaused;
    const elements = document.querySelectorAll('*');
    elements.forEach(el => {
        if (isAnimationPaused) {
            el.classList.add('paused');
        } else {
            el.classList.remove('paused');
        }
    });
    
    if (soundEnabled) playSound('click');
}

function resetAnimation() {
    location.reload();
}

function toggleSound() {
    soundEnabled = !soundEnabled;
    if (soundEnabled) playSound('enable');
}

// Фільтрація за роками з використанням утиліт
function filterByYear(year) {
    currentYear = year;
    
    // Збереження вибраного року
    Utils.Storage.set('selectedYear', year);
    
    // Оновлення активної кнопки
    Utils.DOM.$('.year-btn').forEach(btn => Utils.DOM.removeClass(btn, 'active'));
    event.target.classList.add('active');

    // Оновлення даних діаграми
    const data = yearData[year];
    const circles = Utils.DOM.$('.interactive-circle');
    
    // Анімована зміна значень
    animateCircleUpdate(circles[0], data.solar, '☀️', 'Сонячна');
    animateCircleUpdate(circles[1], data.wind, '💨', 'Вітрова');
    animateCircleUpdate(circles[2], data.other, '🌿', 'Інші');

    if (soundEnabled) playSound('filter');
}

// Анімація оновлення кругових діаграм
function animateCircleUpdate(circle, targetValue, icon, label) {
    const currentValue = parseInt(circle.style.getPropertyValue('--percentage')) || 0;
    const startTime = performance.now();
    const duration = 500;
    
    function animate(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Utils.Math.clamp(elapsed / duration, 0, 1);
        
        const currentAnimValue = Utils.Math.lerp(currentValue, targetValue, progress);
        const roundedValue = Utils.Math.round(currentAnimValue, 0);
        
        circle.style.setProperty('--percentage', roundedValue + '%');
        circle.querySelector('.circle-text').innerHTML = `${icon}<br>${roundedValue}%<br>${label}`;
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    }
    
    requestAnimationFrame(animate);
}

// Поділитися результатами
function shareResults() {
    if (navigator.share) {
        navigator.share({
            title: 'Відновлювана енергія в Україні',
            text: 'Подивіться на розвиток зеленої енергетики в Україні!',
            url: window.location.href
        });
    } else {
        // Fallback для браузерів без підтримки Web Share API
        navigator.clipboard.writeText(window.location.href);
        alert('Посилання скопійовано в буфер обміну!');
    }
    if (soundEnabled) playSound('success');
}

// Завантаження даних
function downloadData() {
    const data = {
        overview: {
            installedCapacity: '12.5 ГВт',
            shareInTotal: '15.2%',
            activeProjects: 450,
            co2Reduction: '2.8 млн тонн'
        },
        distribution: yearData[currentYear],
        timeline: yearData
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'renewable_energy_data.json';
    a.click();
    URL.revokeObjectURL(url);

    if (soundEnabled) playSound('download');
}

// Обробка клавіатурних команд
function initKeyboardControls() {
    document.addEventListener('keydown', (e) => {
        switch(e.key) {
            case ' ':
                e.preventDefault();
                toggleAnimation();
                break;
            case 'r':
            case 'R':
                resetAnimation();
                break;
            case 's':
            case 'S':
                toggleSound();
                break;
            case 'ArrowLeft':
                if (currentYear > 2020) {
                    changeYear(currentYear - 1);
                }
                break;
            case 'ArrowRight':
                if (currentYear < 2024) {
                    changeYear(currentYear + 1);
                }
                break;
        }
    });
}

// Допоміжна функція для зміни року програмно
function changeYear(year) {
    const yearButton = document.querySelector(`[onclick="filterByYear(${year})"]`);
    if (yearButton) {
        yearButton.click();
    }
}

// Підтримка сенсорних жестів для мобільних пристроїв
function initTouchGestures() {
    let touchStartX = 0;
    let touchStartY = 0;

    document.addEventListener('touchstart', (e) => {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    });

    document.addEventListener('touchend', (e) => {
        const touchEndX = e.changedTouches[0].clientX;
        const touchEndY = e.changedTouches[0].clientY;
        
        const deltaX = touchEndX - touchStartX;
        const deltaY = touchEndY - touchStartY;

        // Свайп вліво/вправо для зміни років
        if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 50) {
            if (deltaX > 0 && currentYear > 2020) {
                changeYear(currentYear - 1);
            } else if (deltaX < 0 && currentYear < 2024) {
                changeYear(currentYear + 1);
            }
        }
    });
}