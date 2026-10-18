import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (120, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 200)

# Player settings
player_width = 50
player_height = 30
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 5

# Alien settings
alien_width = 40
alien_height = 30
alien_speed = 5
alien_direction = 1  # 1 for right, -1 for left
aliens = []

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 30
bullets = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Create aliens
def create_aliens():
    for row in range(3):
        for col in range(12):
            alien_x = col * (alien_width + 10) + 50
            alien_y = row * (alien_height + 10) + 50
            aliens.append(pygame.Rect(alien_x, alien_y, alien_width, alien_height))

create_aliens()

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:        
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        if len(bullets) < 5:  # Limit the number of bullets on screen
            bullet = pygame.Rect(player_x + player_width // 2 - bullet_width // 2, player_y, bullet_width, bullet_height)
            bullets.append(bullet)
    
    # Move aliens
    for alien in aliens:
        alien.x += alien_speed * alien_direction
        if alien.right >= SCREEN_WIDTH or alien.left <= 0:
            alien_direction *= -1
            for a in aliens:
                a.y += alien_height
                
    
    # Move bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Check for collisions
    for bullet in bullets[:]:
        for alien in aliens[:]:
            if bullet.colliderect(alien):
                bullets.remove(bullet)
                aliens.remove(alien)
                score += 1
                break

    # Draw player
    player = pygame.Rect(player_x, player_y, player_width, player_height)
    pygame.draw.rect(screen, GREEN, player)

    # Draw aliens
    for alien in aliens:
        pygame.draw.rect(screen, RED, alien)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)
    
    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # End game if aliens reach the player
    for alien in aliens:
        if alien.bottom >= player_y:
            running = False

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
