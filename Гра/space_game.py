import tkinter as tk
from tkinter import messagebox
import random
import math

WIDTH, HEIGHT = 800, 600

class SpaceGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Космический корабль")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)
        
        self.canvas = tk.Canvas(root, bg="black", width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        
        # Generate stars
        self.stars = []
        for _ in range(100):
            star_x = random.randint(0, WIDTH)
            star_y = random.randint(0, HEIGHT)
            star_size = random.randint(1, 2)
            self.stars.append((star_x, star_y, star_size))
        
        # Sun position
        self.sun_x = WIDTH - 80
        self.sun_y = 60
        self.sun_radius = 40
        
        # Player
        self.player_x = WIDTH // 2
        self.player_y = HEIGHT - 50
        self.player_width = 50
        self.player_height = 30
        self.player_speed = 10
        self.lives = 3
        self.score = 0
        
        # Game state
        self.asteroids = []
        self.bullets = []
        self.explosions = []  # Список вибухів
        self.spawn_timer = 0
        self.spawn_interval = 30  # Початковий інтервал спавну
        self.difficulty_timer = 0  # Таймер для збільшення складності кожні 10 сек
        self.game_running = True
        self.keys = {}
        
        # Bind keys
        self.root.bind("<Left>", lambda e: self._key_press("left", True))
        self.root.bind("<Right>", lambda e: self._key_press("right", True))
        self.root.bind("<KeyRelease-Left>", lambda e: self._key_press("left", False))
        self.root.bind("<KeyRelease-Right>", lambda e: self._key_press("right", False))
        self.root.bind("<space>", lambda e: self._shoot())
        
        self.game_loop()
    
    def _key_press(self, key, state):
        self.keys[key] = state
    
    def _shoot(self):
        self.bullets.append({
            'x': self.player_x + self.player_width // 2,
            'y': self.player_y,
            'vy': -7,
            'radius': 2
        })
    
    def draw_player(self):
        self.canvas.create_rectangle(
            self.player_x, self.player_y,
            self.player_x + self.player_width,
            self.player_y + self.player_height,
            fill="white", outline="white"
        )
        self.canvas.create_polygon(
            self.player_x + self.player_width // 2, self.player_y - 15,
            self.player_x + 10, self.player_y,
            self.player_x + self.player_width - 10, self.player_y,
            fill="yellow", outline="white"
        )
    
    def draw_stars(self):
        for star_x, star_y, star_size in self.stars:
            self.canvas.create_oval(
                star_x - star_size, star_y - star_size,
                star_x + star_size, star_y + star_size,
                fill="white", outline="white"
            )
    
    def draw_sun(self):
        # Draw sun
        self.canvas.create_oval(
            self.sun_x - self.sun_radius, self.sun_y - self.sun_radius,
            self.sun_x + self.sun_radius, self.sun_y + self.sun_radius,
            fill="yellow", outline="orange", width=2
        )
        # Add glow effect
        glow_radius = self.sun_radius + 10
        self.canvas.create_oval(
            self.sun_x - glow_radius, self.sun_y - glow_radius,
            self.sun_x + glow_radius, self.sun_y + glow_radius,
            outline="orange", width=1
        )
    
    def spawn_asteroid(self):
        size = random.randint(20, 50)
        return {
            'x': random.randint(0, WIDTH - size),
            'y': -size,
            'size': size,
            'vx': random.uniform(-1, 1),
            'vy': random.uniform(2, 5)
        }
    
    def update_player(self):
        if self.keys.get("left") and self.player_x > 0:
            self.player_x -= self.player_speed
        if self.keys.get("right") and self.player_x < WIDTH - self.player_width:
            self.player_x += self.player_speed
    
    def update_asteroids(self):
        for ast in self.asteroids[:]:
            ast['x'] += ast['vx']
            ast['y'] += ast['vy']
            
            if ast['y'] > HEIGHT:
                self.asteroids.remove(ast)
                self.score += 1
                continue
            
            if (self.player_x < ast['x'] + ast['size'] and
                self.player_x + self.player_width > ast['x'] and
                self.player_y < ast['y'] + ast['size'] and
                self.player_y + self.player_height > ast['y']):
                
                self.lives -= 1
                self.asteroids.remove(ast)
                if self.lives <= 0:
                    self.game_running = False
    
    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet['y'] += bullet['vy']
            
            if bullet['y'] < 0:
                self.bullets.remove(bullet)
                continue
            
            for ast in self.asteroids[:]:
                dist = math.sqrt((bullet['x'] - (ast['x'] + ast['size']//2))**2 + 
                                (bullet['y'] - (ast['y'] + ast['size']//2))**2)
                if dist < ast['size'] // 2 + 2:
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.asteroids.remove(ast)
                    self.score += 5
                    break
    
    def draw_bullets(self):
        for bullet in self.bullets:
            self.canvas.create_oval(
                bullet['x'] - bullet['radius'],
                bullet['y'] - bullet['radius'],
                bullet['x'] + bullet['radius'],
                bullet['y'] + bullet['radius'],
                fill="blue"
            )
    
    def draw_asteroids(self):
        for ast in self.asteroids:
            self.canvas.create_oval(
                ast['x'], ast['y'],
                ast['x'] + ast['size'],
                ast['y'] + ast['size'],
                fill="red", outline="orange", width=2
            )
    
    def game_loop(self):
        if not self.game_running:
            self.end_game()
            return
        
        self.update_player()
        self.update_asteroids()
        self.update_bullets()
        
        # Збільшуємо складність кожні 10 секунд (600 кадрів при 60 FPS)
        self.difficulty_timer += 1
        if self.difficulty_timer >= 600:
            self.difficulty_timer = 0
            # Зменшуємо інтервал спавну (метеориты летять частіше)
            if self.spawn_interval > 10:
                self.spawn_interval -= 3
        
        # Спавн метеоритів з поточним інтервалом
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.asteroids.append(self.spawn_asteroid())
            self.spawn_timer = 0
        
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, WIDTH, HEIGHT, fill="black")
        
        # Draw background
        self.draw_stars()
        self.draw_sun()
        
        self.draw_asteroids()
        self.draw_bullets()
        self.draw_player()
        
        self.canvas.create_text(20, 20, text=f"Score: {self.score}", 
                              fill="white", font=("Arial", 16), anchor="nw")
        self.canvas.create_text(20, 50, text=f"Lives: {self.lives}", 
                              fill="green" if self.lives > 0 else "red", 
                              font=("Arial", 16), anchor="nw")
        
        # Показуємо поточний рівень складності
        difficulty_level = (600 - self.difficulty_timer) // 60  # Показуємо секунди до наступного рівня
        self.canvas.create_text(WIDTH - 150, 20, text=f"Level up in: {difficulty_level}s", 
                              fill="yellow", font=("Arial", 12), anchor="ne")
        
        self.canvas.create_text(WIDTH // 2, HEIGHT - 30, 
                              text="SPACE: Shoot | Arrows: Move", 
                              fill="cyan", font=("Arial", 12))
        
        self.root.after(16, self.game_loop)
    
    def end_game(self):
        messagebox.showinfo("Game Over", f"Your Score: {self.score}\n\nLives: {self.lives}")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = SpaceGame(root)
    root.mainloop()
