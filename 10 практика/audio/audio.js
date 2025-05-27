// Модуль для роботи зі звуковими ефектами

// Глобальна змінна для контролю звуку
window.soundEnabled = true;

// Перемикач звуку
function updateSoundToggleIcon() {
    const icon = document.getElementById('soundToggle');
    if (!icon) return;
    icon.textContent = window.soundEnabled ? '🔊' : '🔇';
}
document.addEventListener('DOMContentLoaded', function() {
    const soundToggle = document.getElementById('soundToggle');
    if (soundToggle) {
        soundToggle.addEventListener('click', function() {
            window.soundEnabled = !window.soundEnabled;
            updateSoundToggleIcon();
        });
        updateSoundToggleIcon();
    }
});

// Звукові ефекти через Web Audio API
function playSound(type) {
    if (!soundEnabled) return;
    
    try {
        // Створення простого звукового ефекту через Web Audio API
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        const frequencies = {
            'click': 800,
            'filter': 600,
            'success': 1000,
            'download': 400,
            'enable': 1200
        };

        oscillator.frequency.value = frequencies[type] || 600;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.1);

        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.1);
    } catch (error) {
        console.log('Звукові ефекти недоступні:', error);
    }
}

// Розширені звукові ефекти
const SoundManager = {
    context: null,
    
    init() {
        try {
            this.context = new (window.AudioContext || window.webkitAudioContext)();
        } catch (error) {
            console.log('Web Audio API недоступний:', error);
        }
    },
    
    playTone(frequency, duration, volume = 0.1) {
        if (!this.context || !soundEnabled) return;
        
        const oscillator = this.context.createOscillator();
        const gainNode = this.context.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.context.destination);
        
        oscillator.frequency.value = frequency;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(volume, this.context.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.001, this.context.currentTime + duration);
        
        oscillator.start(this.context.currentTime);
        oscillator.stop(this.context.currentTime + duration);
    },
    
    playChord(frequencies, duration = 0.3) {
        frequencies.forEach(freq => {
            this.playTone(freq, duration, 0.05);
        });
    },
    
    playAnimationSound() {
        // Приємний акорд для анімацій
        this.playChord([261.63, 329.63, 392.00], 0.2); // C-E-G
    },
    
    playErrorSound() {
        this.playTone(200, 0.1, 0.15);
    },
    
    playSuccessSound() {
        // Послідовність тонів для успіху
        setTimeout(() => this.playTone(523.25, 0.1), 0);    // C5
        setTimeout(() => this.playTone(659.25, 0.1), 100);  // E5
        setTimeout(() => this.playTone(783.99, 0.2), 200);  // G5
    }
};

// Ініціалізація звукового менеджера при завантаженні
document.addEventListener('DOMContentLoaded', function() {
    SoundManager.init();
});

// Додаткові звукові функції для конкретних дій
function playInteractionSound() {
    if (soundEnabled) {
        SoundManager.playTone(800, 0.1);
    }
}

function playNavigationSound() {
    if (soundEnabled) {
        SoundManager.playTone(600, 0.15);
    }
}

function playCompletionSound() {
    if (soundEnabled) {
        SoundManager.playSuccessSound();
    }
}