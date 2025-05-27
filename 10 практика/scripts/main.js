class GameSystem {
    constructor() {
        this.score = 0;
        this.level = 1;
        this.clickCount = 0;
        this.achievements = {
            'first-click': false,
            'energy-explorer': false,
            'stats-master': false,
            'eco-warrior': false,
            'green-champion': false
        };
        this.init();
    }

    init() {
        this.updateUI();
        this.bindEvents();
    }

    bindEvents() {
        document.querySelectorAll('.stat-card').forEach(card => {
            card.addEventListener('click', (e) => this.handleStatClick(e));
            card.addEventListener('mouseenter', () => card.classList.add('hovered'));
            card.addEventListener('mouseleave', () => card.classList.remove('hovered'));
        });

        document.querySelectorAll('.energy-circle').forEach(circle => {
            circle.addEventListener('click', (e) => this.handleEnergyClick(e));
            circle.addEventListener('mouseenter', (e) => this.showHaloEffect(e.currentTarget));
            circle.addEventListener('mouseleave', (e) => this.removeHaloEffect(e.currentTarget));
            circle.addEventListener('mouseenter', () => circle.classList.add('hovered'));
            circle.addEventListener('mouseleave', () => circle.classList.remove('hovered'));
        });

        document.querySelectorAll('.section').forEach(section => {
            section.addEventListener('click', (e) => this.handleSectionClick(e));
        });

        // Підсвічування досягнень при наведенні
        document.querySelectorAll('.achievement').forEach(ach => {
            ach.addEventListener('mouseenter', () => ach.classList.add('hovered'));
            ach.addEventListener('mouseleave', () => ach.classList.remove('hovered'));
        });
    }

    showHaloEffect(target) {
        if (target.querySelector('.halo-effect')) return;
        const halo = document.createElement('div');
        halo.className = 'halo-effect';
        target.appendChild(halo);
        setTimeout(() => {
            halo.style.opacity = '1';
            halo.style.transform = 'scale(1.2)';
        }, 10);
    }

    removeHaloEffect(target) {
        const halo = target.querySelector('.halo-effect');
        if (halo) {
            halo.style.opacity = '0';
            halo.style.transform = 'scale(0.8)';
            setTimeout(() => {
                if (halo.parentNode) halo.parentNode.removeChild(halo);
            }, 300);
        }
    }

    handleStatClick(e) {
        const card = e.currentTarget;
        if (typeof playInteractionSound === 'function') playInteractionSound();
        this.addScore(10);
        this.clickCount++;
        
        card.classList.add('clicked');
        setTimeout(() => card.classList.remove('clicked'), 500);
        
        this.createParticles(e.clientX, e.clientY, '#4CAF50');
        this.checkAchievements();
    }

    handleEnergyClick(e) {
        const circle = e.currentTarget;
        const energyType = circle.dataset.energy;
        if (typeof playInteractionSound === 'function') playInteractionSound();
        let points = 15;
        if (energyType === 'solar') points = 20;
        if (energyType === 'wind') points = 18;
        
        this.addScore(points);
        this.clickCount++;
        
        circle.classList.add('clicked');
        // Додаємо хвилю при кліку
        this.createRippleEffect(circle, e);
        setTimeout(() => circle.classList.remove('clicked'), 600);
        
        this.createParticles(e.clientX, e.clientY, '#FFD700');
        this.checkAchievements();
    }

    createRippleEffect(target, event) {
        const rect = target.getBoundingClientRect();
        const ripple = document.createElement('div');
        ripple.className = 'ripple-effect';
        const size = Math.max(rect.width, rect.height);
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = (event.clientX - rect.left - size / 2) + 'px';
        ripple.style.top = (event.clientY - rect.top - size / 2) + 'px';
        target.appendChild(ripple);
        setTimeout(() => {
            ripple.style.opacity = '0';
            ripple.style.transform = 'scale(2)';
        }, 10);
        setTimeout(() => {
            if (ripple.parentNode) ripple.parentNode.removeChild(ripple);
        }, 500);
    }

    handleSectionClick(e) {
        if (e.target.closest('.stat-card') || e.target.closest('.energy-circle')) {
            return;
        }
        if (typeof playNavigationSound === 'function') playNavigationSound();
        this.addScore(5);
        this.clickCount++;
        
        const section = e.currentTarget;
        section.style.transform = 'translateY(-5px) scale(1.02)';
        setTimeout(() => {
            section.style.transform = '';
        }, 200);
        
        this.checkAchievements();
    }

    addScore(points) {
        this.score += points;
        this.updateLevel();
        this.updateUI();
    }

    updateLevel() {
        const newLevel = Math.floor(this.score / 100) + 1;
        if (newLevel > this.level) {
            this.level = newLevel;
            this.showLevelUp();
        }
    }

    updateUI() {
        document.getElementById('scoreValue').textContent = this.score;
        document.getElementById('levelValue').textContent = this.level;
        
        const progress = (this.score % 100);
        document.getElementById('levelBar').style.width = progress + '%';
    }

    checkAchievements() {
        if (this.clickCount >= 1 && !this.achievements['first-click']) {
            this.unlockAchievement('first-click', 'Перший клік!');
        }
        
        if (this.clickCount >= 5 && !this.achievements['energy-explorer']) {
            this.unlockAchievement('energy-explorer', 'Дослідник енергії!');
        }
        
        if (this.score >= 200 && !this.achievements['stats-master']) {
            this.unlockAchievement('stats-master', 'Майстер статистики!');
        }
        
        if (this.level >= 3 && !this.achievements['eco-warrior']) {
            this.unlockAchievement('eco-warrior', 'Еко-воїн!');
        }
        
        if (this.level >= 5 && !this.achievements['green-champion']) {
            this.unlockAchievement('green-champion', 'Зелений чемпіон!');
        }
    }

    unlockAchievement(id, name) {
        this.achievements[id] = true;
        const achievementEl = document.querySelector(`[data-achievement="${id}"]`);
        achievementEl.classList.add('unlocked');
        if (typeof playCompletionSound === 'function') playCompletionSound();
        this.showAchievementPopup(name);
        this.addScore(50);
    }

    showAchievementPopup(name) {
        const popup = document.getElementById('achievementPopup');
        const text = document.getElementById('achievementText');
        text.textContent = name;
        
        popup.classList.add('show');
        setTimeout(() => {
            popup.classList.remove('show');
        }, 3000);
    }

    showLevelUp() {
        if (typeof SoundManager !== 'undefined' && SoundManager.playAnimationSound) SoundManager.playAnimationSound();
        this.createParticles(window.innerWidth / 2, window.innerHeight / 2, '#FFD700', 20);
    }

    createParticles(x, y, color, count = 8) {
        for (let i = 0; i < count; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.background = color;
            particle.style.left = x + 'px';
            particle.style.top = y + 'px';
            
            const angle = (i / count) * 2 * Math.PI;
            const velocity = 100 + Math.random() * 100;
            const vx = Math.cos(angle) * velocity;
            const vy = Math.sin(angle) * velocity;
            
            document.body.appendChild(particle);
            
            let posX = x;
            let posY = y;
            let opacity = 1;
            
            const animate = () => {
                posX += vx * 0.02;
                posY += vy * 0.02;
                opacity -= 0.02;
                
                particle.style.left = posX + 'px';
                particle.style.top = posY + 'px';
                particle.style.opacity = opacity;
                
                if (opacity > 0) {
                    requestAnimationFrame(animate);
                } else {
                    document.body.removeChild(particle);
                }
            };
            
            requestAnimationFrame(animate);
        }
    }
}

// Ініціалізація гри
document.addEventListener('DOMContentLoaded', () => {
    new GameSystem();
});