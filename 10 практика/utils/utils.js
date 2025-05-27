// Допоміжні утиліти для проекту

// Утиліти для роботи з DOM
const DOMUtils = {
    // Знайти елемент за селектором
    $(selector) {
        return document.querySelector(selector);
    },
    
    // Знайти всі елементи за селектором
    $$(selector) {
        return document.querySelectorAll(selector);
    },
    
    // Додати клас до елемента
    addClass(element, className) {
        if (element) element.classList.add(className);
    },
    
    // Видалити клас з елемента
    removeClass(element, className) {
        if (element) element.classList.remove(className);
    },
    
    // Перемкнути клас
    toggleClass(element, className) {
        if (element) element.classList.toggle(className);
    },
    
    // Перевірити наявність класу
    hasClass(element, className) {
        return element ? element.classList.contains(className) : false;
    },
    
    // Створити елемент
    createElement(tag, attributes = {}, textContent = '') {
        const element = document.createElement(tag);
        
        Object.keys(attributes).forEach(key => {
            element.setAttribute(key, attributes[key]);
        });
        
        if (textContent) {
            element.textContent = textContent;
        }
        
        return element;
    },
    
    // Показати елемент
    show(element) {
        if (element) element.style.display = 'block';
    },
    
    // Сховати елемент
    hide(element) {
        if (element) element.style.display = 'none';
    }
};

// Утиліти для роботи з анімаціями
const AnimationUtils = {
    // Плавна поява елемента
    fadeIn(element, duration = 300) {
        if (!element) return;
        
        element.style.opacity = '0';
        element.style.display = 'block';
        
        const start = performance.now();
        
        function animate(currentTime) {
            const elapsed = currentTime - start;
            const progress = Math.min(elapsed / duration, 1);
            
            element.style.opacity = progress;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        }
        
        requestAnimationFrame(animate);
    },
    
    // Плавне зникнення елемента
    fadeOut(element, duration = 300) {
        if (!element) return;
        
        const start = performance.now();
        
        function animate(currentTime) {
            const elapsed = currentTime - start;
            const progress = Math.min(elapsed / duration, 1);
            
            element.style.opacity = 1 - progress;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            } else {
                element.style.display = 'none';
            }
        }
        
        requestAnimationFrame(animate);
    },
    
    // Анімація руху
    slideIn(element, direction = 'left', duration = 400) {
        if (!element) return;
        
        const directions = {
            left: 'translateX(-100%)',
            right: 'translateX(100%)',
            up: 'translateY(-100%)',
            down: 'translateY(100%)'
        };
        
        element.style.transform = directions[direction];
        element.style.transition = `transform ${duration}ms ease-out`;
        
        setTimeout(() => {
            element.style.transform = 'translate(0, 0)';
        }, 10);
    }
};

// Утиліти для роботи з числами та математикою
const MathUtils = {
    // Округлення до певної кількості знаків після коми
    round(number, decimals = 2) {
        return Math.round(number * Math.pow(10, decimals)) / Math.pow(10, decimals);
    },
    
    // Лінійна інтерполяція
    lerp(start, end, progress) {
        return start + (end - start) * progress;
    },
    
    // Обмеження числа в діапазоні
    clamp(value, min, max) {
        return Math.min(Math.max(value, min), max);
    },
    
    // Генерація випадкового числа в діапазоні
    random(min, max) {
        return Math.random() * (max - min) + min;
    },
    
    // Генерація випадкового цілого числа
    randomInt(min, max) {
        return Math.floor(this.random(min, max + 1));
    },
    
    // Конвертація відсотків
    percentToDecimal(percent) {
        return percent / 100;
    },
    
    decimalToPercent(decimal) {
        return decimal * 100;
    }
};

// Утиліти для роботи з даними
const DataUtils = {
    // Групування масиву об'єктів за ключем
    groupBy(array, key) {
        return array.reduce((groups, item) => {
            const value = item[key];
            if (!groups[value]) {
                groups[value] = [];
            }
            groups[value].push(item);
            return groups;
        }, {});
    },
    
    // Сортування масиву об'єктів
    sortBy(array, key, descending = false) {
        return array.sort((a, b) => {
            const aValue = a[key];
            const bValue = b[key];
            
            if (aValue < bValue) return descending ? 1 : -1;
            if (aValue > bValue) return descending ? -1 : 1;
            return 0;
        });
    },
    
    // Фільтрація унікальних значень
    unique(array) {
        return [...new Set(array)];
    },
    
    // Знаходження максимального значення в масиві об'єктів
    maxBy(array, key) {
        return array.reduce((max, item) => 
            item[key] > max[key] ? item : max
        );
    },
    
    // Знаходження мінімального значення в масиві об'єктів
    minBy(array, key) {
        return array.reduce((min, item) => 
            item[key] < min[key] ? item : min
        );
    },
    
    // Сума значень в масиві об'єктів
    sumBy(array, key) {
        return array.reduce((sum, item) => sum + item[key], 0);
    },
    
    // Середнє значення
    averageBy(array, key) {
        return this.sumBy(array, key) / array.length;
    }
};

// Утиліти для роботи з часом та датами
const TimeUtils = {
    // Форматування дати
    formatDate(date, format = 'DD.MM.YYYY') {
        const d = new Date(date);
        const day = String(d.getDate()).padStart(2, '0');
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const year = d.getFullYear();
        
        return format
            .replace('DD', day)
            .replace('MM', month)
            .replace('YYYY', year);
    },
    
    // Затримка (Promise-based)
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },
    
    // Debounce функція
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Throttle функція
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// Утиліти для роботи з локальним сховищем (адаптовано для браузера)
const StorageUtils = {
    // Збереження даних (в пам'яті для цього проекту)
    data: {},
    
    set(key, value) {
        try {
            this.data[key] = JSON.stringify(value);
            return true;
        } catch (error) {
            console.error('Помилка збереження даних:', error);
            return false;
        }
    },
    
    get(key, defaultValue = null) {
        try {
            const value = this.data[key];
            return value ? JSON.parse(value) : defaultValue;
        } catch (error) {
            console.error('Помилка отримання даних:', error);
            return defaultValue;
        }
    },
    
    remove(key) {
        delete this.data[key];
    },
    
    clear() {
        this.data = {};
    },
    
    has(key) {
        return key in this.data;
    }
};

// Утиліти для роботи з кольорами
const ColorUtils = {
    // Конвертація HEX в RGB
    hexToRgb(hex) {
        const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
        return result ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16)
        } : null;
    },
    
    // Конвертація RGB в HEX
    rgbToHex(r, g, b) {
        return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
    },
    
    // Генерація випадкового кольору
    randomColor() {
        return '#' + Math.floor(Math.random()*16777215).toString(16);
    },
    
    // Інтерполяція між двома кольорами
    interpolateColor(color1, color2, factor) {
        const rgb1 = this.hexToRgb(color1);
        const rgb2 = this.hexToRgb(color2);
        
        if (!rgb1 || !rgb2) return color1;
        
        const r = Math.round(rgb1.r + factor * (rgb2.r - rgb1.r));
        const g = Math.round(rgb1.g + factor * (rgb2.g - rgb1.g));
        const b = Math.round(rgb1.b + factor * (rgb2.b - rgb1.b));
        
        return this.rgbToHex(r, g, b);
    }
};

// Утиліти для валідації
const ValidationUtils = {
    // Перевірка електронної пошти
    isEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    },
    
    // Перевірка числа
    isNumber(value) {
        return !isNaN(value) && !isNaN(parseFloat(value));
    },
    
    // Перевірка URL
    isUrl(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    },
    
    // Перевірка на порожність
    isEmpty(value) {
        return value === null || 
               value === undefined || 
               value === '' || 
               (Array.isArray(value) && value.length === 0) ||
               (typeof value === 'object' && Object.keys(value).length === 0);
    },
    
    // Перевірка діапазону
    inRange(value, min, max) {
        return value >= min && value <= max;
    }
};

// Утиліти для роботи з URL та навігацією
const UrlUtils = {
    // Отримання параметрів з URL
    getParams() {
        const params = new URLSearchParams(window.location.search);
        const result = {};
        for (const [key, value] of params) {
            result[key] = value;
        }
        return result;
    },
    
    // Отримання конкретного параметра
    getParam(name) {
        const params = new URLSearchParams(window.location.search);
        return params.get(name);
    },
    
    // Оновлення URL без перезавантаження сторінки
    updateUrl(params) {
        const url = new URL(window.location);
        Object.keys(params).forEach(key => {
            if (params[key] !== null && params[key] !== undefined) {
                url.searchParams.set(key, params[key]);
            } else {
                url.searchParams.delete(key);
            }
        });
        window.history.pushState({}, '', url);
    }
};

// Експорт утиліт (для використання в інших файлах)
window.Utils = {
    DOM: DOMUtils,
    Animation: AnimationUtils,
    Math: MathUtils,
    Data: DataUtils,
    Time: TimeUtils,
    Storage: StorageUtils,
    Color: ColorUtils,
    Validation: ValidationUtils,
    Url: UrlUtils
};