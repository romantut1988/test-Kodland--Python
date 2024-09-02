import pgzrun
import random
from pgzero.loaders import sounds
from pygame import Rect

WIDTH = 600
HEIGHT = 400
PLAYER_SPEED = 5
ENEMY_SPEED = 2
music_enabled = True

player_images = ["ghost", "ghost-2"]
enemy_images = ["gun.png", "gun.png"]
background_music = "sounds/background_music.mp3"


class Player:
    def __init__(self):
        self.images = player_images
        self.image = self.images[0]
        self.rect = Rect((400, 300), (50, 50))
        self.player_anim_count = 0

    def update(self):
        if keyboard.left and self.rect.x > 0:
            self.rect.x -= PLAYER_SPEED
            self.image = self.images[1]
        elif keyboard.right and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += PLAYER_SPEED
            self.image = self.images[1]
        else:
            self.player_anim_count += 1
            if self.player_anim_count >= 10:
                self.player_anim_count = 0
                self.image = self.images[0] if self.image == self.images[1] else self.images[1]

        if keyboard.up and self.rect.y > 0:
            self.rect.y -= PLAYER_SPEED
        elif keyboard.down and self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += PLAYER_SPEED

    def draw(self):
        screen.blit(self.image, self.rect.topleft)


class Enemy:
    def __init__(self, x, y):
        self.images = enemy_images
        self.image = self.images[0]
        self.rect = Rect((x, y), (30, 30))
        self.enemy_anim_count = 0

    def update(self, player):
        if self.rect.x < player.rect.x:
            self.rect.x += ENEMY_SPEED
            self.enemy_anim_count += 1
            if self.enemy_anim_count >= 10:
                self.enemy_anim_count = 0
                self.image = self.images[1] if self.image == self.images[0] else self.images[0]
        elif self.rect.x > player.rect.x:
            self.rect.x -= ENEMY_SPEED
            self.enemy_anim_count += 1
            if self.enemy_anim_count >= 10:
                self.enemy_anim_count = 0
                self.image = self.images[1] if self.image == self.images[0] else self.images[0]

        if self.rect.y < player.rect.y:
            self.rect.y += ENEMY_SPEED
        elif self.rect.y > player.rect.y:
            self.rect.y -= ENEMY_SPEED

    def draw(self):
        screen.blit(self.image, self.rect.topleft)


player = Player()
enemies = [Enemy(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(5)]
game_started = False


def collided_enemy():
    return player.rect.collidelistall([enemy.rect for enemy in enemies])


def draw():
    if not game_started:
        draw_menu()
    else:
        screen.clear()
        player.draw()
        for enemy in enemies:
            enemy.draw()


def update():
    if game_started:
        player.update()
        for enemy in enemies:
            enemy.update(player)

        if collided_enemy(): 
            sounds.finish.play()


def draw_menu():
    screen.clear()
    screen.draw.text("Мини игра охотники за приведениями", center=(WIDTH // 2, HEIGHT // 4), fontsize=30)

    # Кнопка "Начать игру"
    start_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 - 50), (200, 50))
    screen.draw.filled_rect(start_button, (0, 255, 0))
    screen.draw.text("Старт игры", center=start_button.center, fontsize=30)

    # Кнопка "Вкл/Выкл музыку и звуки"
    sound_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 10), (200, 50))
    screen.draw.filled_rect(sound_button, (0, 0, 255))
    screen.draw.text("Звук: " + ("Вкл" if music_enabled else "Выкл"), center=sound_button.center, fontsize=30)

    # Кнопка "Выход"
    exit_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 70), (200, 50))
    screen.draw.filled_rect(exit_button, (255, 0, 0))
    screen.draw.text("Выход", center=exit_button.center, fontsize=30)


def on_mouse_down(pos):
    global game_started, music_enabled
    if not game_started:
        start_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 - 50), (200, 50))
        sound_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 10), (200, 50))
        exit_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 70), (200, 50))

        if start_button.collidepoint(pos):
            game_started = True
            if music_enabled:
                music.play('background_music')

        elif sound_button.collidepoint(pos):
            music_enabled = not music_enabled
            if music_enabled:
                music.set_volume(1.0)
                music.play('background_music')
            else:
                music.set_volume(0)

        elif exit_button.collidepoint(pos):
            exit()


pgzrun.go()
