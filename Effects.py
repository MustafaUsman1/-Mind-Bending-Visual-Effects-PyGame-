#!/usr/bin/env python3
"""
🌟 MIND-BENDING VISUAL EFFECTS - PYGAME VERSION 🌟
Smooth, full-screen window with beautiful effects
Press 1-6 to switch effects, ESC to quit, F to toggle fullscreen
"""

import pygame
import math
import random
from collections import deque
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Create window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("🌟 Mind-Bending Effects Collection")
clock = pygame.time.Clock()

# Font for UI
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# ============= EFFECT 1: MATRIX DIGITAL RAIN =============
class MatrixRain:
    def __init__(self):
        self.name = "Matrix Digital Rain"
        self.drops = []
        self.column_width = 20
        self.reset_drops()
    
    def reset_drops(self):
        self.drops = []
        num_columns = WINDOW_WIDTH // self.column_width
        for i in range(num_columns):
            self.drops.append({
                'x': i * self.column_width,
                'y': random.randint(-500, 0),
                'speed': random.uniform(3, 8),
                'chars': deque(maxlen=random.randint(15, 30)),
                'font_size': random.randint(16, 24)
            })
    
    def update(self, surface):
        surface.fill((0, 0, 0))
        
        for drop in self.drops:
            drop['y'] += drop['speed']
            
            if drop['y'] > WINDOW_HEIGHT + 100:
                drop['y'] = random.randint(-200, -50)
                drop['speed'] = random.uniform(3, 8)
                drop['chars'].clear()
            
            # Add new character
            if random.random() > 0.3:
                drop['chars'].append(random.choice('ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ01234567889ABCZ:・.'))
            
            # Draw the drop
            char_font = pygame.font.Font(None, drop['font_size'])
            for i, char in enumerate(drop['chars']):
                y_pos = int(drop['y'] - i * 20)
                if -30 <= y_pos <= WINDOW_HEIGHT:
                    intensity = (len(drop['chars']) - i) / len(drop['chars'])
                    
                    if i == 0:
                        color = (255, 255, 255)  # Bright white
                    elif intensity > 0.7:
                        color = (150, 255, 150)  # Bright green
                    elif intensity > 0.4:
                        color = (0, 255, 0)      # Green
                    else:
                        color = (0, 150, 0)      # Dim green
                    
                    text = char_font.render(char, True, color)
                    surface.blit(text, (drop['x'], y_pos))

# ============= EFFECT 2: PLASMA WAVE =============
class PlasmaWave:
    def __init__(self):
        self.name = "Plasma Wave"
        self.t = 0
    
    def update(self, surface):
        surface.fill((0, 0, 0))
        pixel_size = 4
        
        for y in range(0, WINDOW_HEIGHT, pixel_size):
            for x in range(0, WINDOW_WIDTH, pixel_size):
                # Multiple sine waves combined
                v = math.sin(x * 0.01 + self.t)
                v += math.sin(y * 0.01 + self.t * 1.3)
                v += math.sin((x + y) * 0.008 + self.t * 0.7)
                v += math.sin(math.sqrt((x-WINDOW_WIDTH/2)**2 + (y-WINDOW_HEIGHT/2)**2) * 0.01 + self.t * 2)
                
                # Normalize
                v = (v + 4) / 8
                
                # Create color gradient
                r = int(255 * math.sin(v * math.pi * 2) ** 2)
                g = int(255 * math.sin(v * math.pi * 2 + 2) ** 2)
                b = int(255 * math.sin(v * math.pi * 2 + 4) ** 2)
                
                pygame.draw.rect(surface, (r, g, b), (x, y, pixel_size, pixel_size))
        
        self.t += 0.03

# ============= EFFECT 3: TUNNEL ZOOM =============
class TunnelZoom:
    def __init__(self):
        self.name = "Tunnel Zoom"
        self.t = 0
    
    def update(self, surface):
        surface.fill((0, 0, 0))
        cx, cy = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        pixel_size = 4
        
        for y in range(0, WINDOW_HEIGHT, pixel_size):
            for x in range(0, WINDOW_WIDTH, pixel_size):
                dx = x - cx
                dy = y - cy
                
                dist = math.sqrt(dx*dx + dy*dy) + 0.001
                angle = math.atan2(dy, dx)
                
                # Tunnel effect
                u = 500.0 / dist + self.t * 5
                v = angle * 5 + self.t * 3
                
                # Pattern
                brightness = (math.sin(u) + math.cos(v) + 2) / 4
                
                # Rainbow colors based on angle
                hue = (angle + math.pi) / (2 * math.pi)
                r = int(255 * abs(math.sin(hue * math.pi * 2)))
                g = int(255 * abs(math.sin(hue * math.pi * 2 + 2)))
                b = int(255 * abs(math.sin(hue * math.pi * 2 + 4)))
                
                # Apply brightness
                r = int(r * brightness)
                g = int(g * brightness)
                b = int(b * brightness)
                
                pygame.draw.rect(surface, (r, g, b), (x, y, pixel_size, pixel_size))
        
        self.t += 0.02

# ============= EFFECT 4: FIRE SIMULATION =============
class Fire:
    def __init__(self):
        self.name = "Fire Simulation"
        self.width = WINDOW_WIDTH // 4
        self.height = WINDOW_HEIGHT // 4
        self.fire = [[0 for _ in range(self.width)] for _ in range(self.height + 2)]
    
    def update(self, surface):
        surface.fill((0, 0, 0))
        
        # Add heat at bottom
        for x in range(self.width):
            self.fire[self.height][x] = random.randint(200, 255)
        
        # Propagate fire upward
        for y in range(self.height):
            for x in range(self.width):
                left = max(0, x - 1)
                right = min(self.width - 1, x + 1)
                
                heat = (self.fire[y+1][left] + 
                       self.fire[y+1][x] + 
                       self.fire[y+1][right] + 
                       self.fire[y+2][x]) / 4.0
                
                self.fire[y][x] = max(0, heat - random.randint(1, 3))
        
        # Render with scaling
        scale_x = WINDOW_WIDTH / self.width
        scale_y = WINDOW_HEIGHT / self.height
        
        for y in range(self.height):
            for x in range(self.width):
                heat = self.fire[y][x]
                
                if heat > 200:
                    color = (255, 255, 200)
                elif heat > 150:
                    color = (255, 255, 0)
                elif heat > 100:
                    color = (255, int(heat * 1.5), 0)
                elif heat > 50:
                    color = (int(heat * 2), 0, 0)
                else:
                    color = (int(heat), 0, 0)
                
                pygame.draw.rect(surface, color, 
                               (int(x * scale_x), int(y * scale_y), 
                                int(scale_x) + 1, int(scale_y) + 1))

# ============= EFFECT 5: DNA HELIX =============
class DNAHelix:
    def __init__(self):
        self.name = "DNA Helix"
        self.t = 0
    
    def update(self, surface):
        surface.fill((0, 10, 20))
        
        cx = WINDOW_WIDTH / 2
        segments = 60
        
        for i in range(segments):
            y = (i / segments) * WINDOW_HEIGHT
            
            # Two helixes
            for strand in range(2):
                phase = math.pi * strand
                x1 = int(cx + 150 * math.sin(i * 0.3 + self.t + phase))
                x2 = int(cx + 150 * math.cos(i * 0.3 + self.t + phase))
                
                color = (255, 50, 50) if strand == 0 else (50, 50, 255)
                pygame.draw.circle(surface, color, (x1, int(y)), 8)
                
                # Connecting lines
                if i % 3 == 0 and strand == 0:
                    x2_other = int(cx + 150 * math.cos(i * 0.3 + self.t + math.pi))
                    pygame.draw.line(surface, (100, 100, 100), (x1, int(y)), (x2_other, int(y)), 2)
        
        self.t += 0.05

# ============= EFFECT 6: STARFIELD =============
class Starfield:
    def __init__(self):
        self.name = "Starfield Warp"
        self.stars = []
        for _ in range(500):
            self.stars.append({
                'x': random.uniform(-1, 1),
                'y': random.uniform(-1, 1),
                'z': random.uniform(0.1, 2)
            })
    
    def update(self, surface):
        surface.fill((0, 0, 10))
        
        cx, cy = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
        
        for star in self.stars:
            star['z'] -= 0.02
            
            if star['z'] <= 0:
                star['x'] = random.uniform(-1, 1)
                star['y'] = random.uniform(-1, 1)
                star['z'] = 2
            
            # Project to screen
            sx = int((star['x'] / star['z']) * 400 + cx)
            sy = int((star['y'] / star['z']) * 400 + cy)
            
            if 0 <= sx < WINDOW_WIDTH and 0 <= sy < WINDOW_HEIGHT:
                speed = 1 - star['z'] / 2
                size = int(3 * speed) + 1
                brightness = int(255 * speed)
                
                pygame.draw.circle(surface, (brightness, brightness, brightness), 
                                 (sx, sy), size)
                
                # Trail effect
                if speed > 0.5:
                    trail_len = int(20 * speed)
                    tx = int(sx - (star['x'] / star['z']) * trail_len)
                    ty = int(sy - (star['y'] / star['z']) * trail_len)
                    pygame.draw.line(surface, (brightness//2, brightness//2, brightness//2),
                                   (sx, sy), (tx, ty), 1)

# ============= MAIN LOOP =============
def main():
    global WINDOW_WIDTH, WINDOW_HEIGHT, screen
    
    effects = [
        MatrixRain(),
        PlasmaWave(),
        TunnelZoom(),
        Fire(),
        DNAHelix(),
        Starfield()
    ]
    
    current = 0
    fullscreen = False
    show_ui = True
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_1:
                    current = 0
                    effects[0].reset_drops()
                elif event.key == pygame.K_2:
                    current = 1
                elif event.key == pygame.K_3:
                    current = 2
                elif event.key == pygame.K_4:
                    current = 3
                elif event.key == pygame.K_5:
                    current = 4
                elif event.key == pygame.K_6:
                    current = 5
                elif event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        WINDOW_WIDTH, WINDOW_HEIGHT = screen.get_size()
                    else:
                        screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
                        WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 800
                    effects[0].reset_drops()
                elif event.key == pygame.K_h:
                    show_ui = not show_ui
            
            elif event.type == pygame.VIDEORESIZE:
                WINDOW_WIDTH, WINDOW_HEIGHT = event.w, event.h
                effects[0].reset_drops()
        
        # Update current effect
        effects[current].update(screen)
        
        # Draw UI
        if show_ui:
            # Semi-transparent background for text
            ui_surface = pygame.Surface((400, 120))
            ui_surface.set_alpha(180)
            ui_surface.fill((0, 0, 0))
            screen.blit(ui_surface, (10, 10))
            
            # Effect name
            title = font.render(f"{current + 1}. {effects[current].name}", True, (0, 255, 255))
            screen.blit(title, (20, 20))
            
            # Instructions
            instructions = [
                "Press 1-6: Switch effects",
                "Press F: Toggle fullscreen",
                "Press H: Hide/show UI",
                "Press ESC: Quit"
            ]
            
            for i, text in enumerate(instructions):
                inst = small_font.render(text, True, (200, 200, 200))
                screen.blit(inst, (20, 60 + i * 20))
        
        # FPS counter
        fps_text = small_font.render(f"FPS: {int(clock.get_fps())}", True, (0, 255, 0))
        screen.blit(fps_text, (WINDOW_WIDTH - 100, 10))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
