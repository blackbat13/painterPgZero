import math
import pgzrun
import pygame
import random

WIDTH = 1000
HEIGHT = 1000

TITLE = "Painter PgZero"

blue = Actor("blue", (50, 50))
blue.name = "Blue"
blue.color = "#2184D3"
blue.keys = {"left": "q", "right": "e", "power": "w"}

red = Actor("red", (WIDTH - 50, 50))
red.name = "Red"
red.color = "#DD4E54"
red.keys = {"left": "i", "right": "p", "power": "o"}

green = Actor("green", (50, HEIGHT - 50))
green.name = "Green"
green.color = "#49B47E"
green.keys = {"left": "left", "right": "right", "power": "up"}

grey = Actor("grey", (WIDTH - 50, HEIGHT - 50))
grey.name = "Grey"
grey.color = "#937F7C"
grey.keys = {"left": "kp7", "right": "kp9", "power": "kp8"}

players = [blue, red, green, grey]

color_surface = pygame.Surface((WIDTH, HEIGHT))
color_surface.fill("black")

item = Actor("bomb")
item.active = False

start_button = Actor("button", (WIDTH / 2, HEIGHT - 50))
start_button.text_color = "white"

music_button = Actor("music_on", (WIDTH - 100, 50))
music_button.on = True

sound_button = Actor("sound_on", (WIDTH - 50, 50))
sound_button.on = True

timer = -1

winner = ""

number_sounds = [sounds.time_over, sounds.one, sounds.two, sounds.three, sounds.four, sounds.five, sounds.six,
                 sounds.seven, sounds.eight, sounds.nine, sounds.ten]


def draw():
    screen.blit(color_surface, (0, 0))

    if timer == -1:
        draw_controls()
        draw_start_button()
        music_button.draw()
        sound_button.draw()
        return

    for pl in players:
        if pl.power:
            screen.draw.filled_circle(pl.pos, 25, "white")
        pl.draw()

    if item.active:
        item.draw()

    screen.draw.text(f"{timer}", center=(WIDTH / 2, 45), fontsize=50, color="yellow", fontname="kenney_bold")

    if timer == 0:
        for i, pl in enumerate(players):
            screen.draw.text(f"{pl.name}: {pl.percent:.2f}%", center=(WIDTH / 2, 200 + i * 100), fontsize=80,
                             color="white", fontname="kenney_future_square")
        screen.draw.text(f"{winner} wins!", center=(WIDTH / 2, HEIGHT - 300), fontsize=100, color="white",
                         fontname="kenney_bold")
        draw_start_button()

    music_button.draw()
    sound_button.draw()


def draw_controls():
    screen.draw.text(
        "Blue\nTurn: Q/E\nPower: W\n\nRed\nTurn: I/P\nPower: O\n\nGreen\nTurn: Left/Right\nPower: UP\n\nGrey (keypad)\nTurn: 7/9\nPower: 8\n\nStart: SPACE\nMute music: M\nMute sounds: S",
        midtop=(WIDTH / 2, 50), fontsize=40, color="white", fontname="kenney_future_square")


def draw_start_button():
    start_button.draw()
    screen.draw.text("START", center=start_button.pos, fontsize=25, color=start_button.text_color,
                     fontname="kenney_bold")


def on_mouse_down(pos):
    if timer <= 0 and start_button.collidepoint(pos):
        initialize()

    if music_button.collidepoint(pos):
        switch_music()

    if sound_button.collidepoint(pos):
        switch_sound()


def on_key_down(key):
    if timer <= 0 and key == keys.SPACE:
        initialize()

    if key == keys.M:
        switch_music()

    if key == keys.S:
        switch_sound()


def switch_music():
    if music_button.on:
        music_button.on = False
        music_button.image = "music_off"
        music.set_volume(0)
    else:
        music_button.on = True
        music_button.image = "music_on"
        music.set_volume(1)


def switch_sound():
    if sound_button.on:
        sound_button.on = False
        sound_button.image = "sound_off"
    else:
        sound_button.on = True
        sound_button.image = "sound_on"


def update():
    if timer <= 0:
        mouse_pos = pygame.mouse.get_pos()
        if start_button.collidepoint(mouse_pos):
            start_button.image = "button_hover"
            start_button.text_color = "black"
        else:
            start_button.image = "button"
            start_button.text_color = "white"

        return

    for pl in players:
        update_player(pl)


def use_power(player):
    if player.name == "Blue":
        player.power = False
        color_surface.fill("black")
        clock.schedule_unique(activate_power_blue, player.power_timeout)
    if player.name == "Red":
        player.power = False
        player.velocity += 5
        clock.schedule_unique(activate_power_red, player.power_timeout)
    if player.name == "Green":
        player.power = False
        for _ in range(150):
            pl = random.choice(players)
            pygame.draw.circle(color_surface, pl.color, (random.randint(0, WIDTH), random.randint(0, HEIGHT)), 50)
        clock.schedule_unique(activate_power_green, player.power_timeout)
    if player.name == "Grey":
        player.power = False
        player.radius += 15
        player.velocity -= 1
        clock.schedule_unique(activate_power_grey, player.power_timeout)


def update_player(player):
    if keyboard[player.keys["left"]]:
        player.angle += 1 + player.velocity / 2
    if keyboard[player.keys["right"]]:
        player.angle -= 1 + player.velocity / 2
    if keyboard[player.keys["power"]] and player.power:
        use_power(player)

    player.x += math.sin(math.radians(player.angle + 90)) * player.velocity
    player.y += math.cos(math.radians(player.angle + 90)) * player.velocity

    if not (0 <= player.x < WIDTH and 0 <= player.y < HEIGHT):
        player.x -= math.sin(math.radians(player.angle + 90)) * player.velocity
        player.y -= math.cos(math.radians(player.angle + 90)) * player.velocity
        player.angle += random.randint(100, 250)
        if sound_button.on:
            sounds.impact.play()

    pygame.draw.circle(color_surface, player.color, player.pos, player.radius)

    for other_player in players:
        if other_player == player:
            continue

        if player.colliderect(other_player):
            player.x -= math.sin(math.radians(player.angle + 90)) * player.velocity
            player.y -= math.cos(math.radians(player.angle + 90)) * player.velocity
            player.angle += random.randint(100, 250)

    if item.active and player.colliderect(item):
        if item.image == "bomb":
            pygame.draw.circle(color_surface, player.color, player.pos, 250)
            if sound_button.on:
                sounds.explosion.play()
        if item.image == "star":
            for _ in range(20):
                pygame.draw.circle(color_surface, player.color, (random.randint(0, WIDTH), random.randint(0, HEIGHT)),
                                   50)
            if sound_button.on:
                sounds.star.play()
        if item.image == "coin":
            player.radius += 5
            if sound_button.on:
                sounds.coin.play()

        item.active = False
        clock.schedule(activate_item, 1.0 + random.random() * 5)


def activate_item():
    item.active = True
    item.x = random.randint(50, WIDTH - 50)
    item.y = random.randint(50, HEIGHT - 50)
    item.image = random.choice(["bomb", "star", "coin"])


def reduce_timer():
    global timer

    timer -= 1

    if timer == 20 and sound_button.on:
        sounds.hurry_up.play()

    if timer <= 10 and sound_button.on:
        number_sounds[timer].play()

    if timer == 0:
        clock.unschedule(reduce_timer)
        compute_winner()
        music.play("results")


def compute_winner():
    global winner

    for pl in players:
        pl.surface_color = color_surface.get_at((int(pl.x), int(pl.y)))
        pl.pixels = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            color = color_surface.get_at((x, y))
            for pl in players:
                if color == pl.surface_color:
                    pl.pixels += 1
                    break

    mx = 0
    for pl in players:
        pl.percent = (pl.pixels / (WIDTH * HEIGHT)) * 100
        if pl.percent > mx:
            mx = pl.percent
            winner = pl.name


def activate_power_blue():
    blue.power = True


def activate_power_red():
    red.power = True


def activate_power_green():
    green.power = True


def activate_power_grey():
    grey.power = True


def initialize():
    global timer

    color_surface.fill("black")

    blue.pos = (50, 50)
    red.pos = (WIDTH - 50, 50)
    green.pos = (50, HEIGHT - 50)
    grey.pos = (WIDTH - 50, HEIGHT - 50)

    blue.velocity = 10
    blue.radius = 20
    blue.power = False
    blue.power_timeout = 45
    clock.schedule_unique(activate_power_blue, blue.power_timeout)

    red.velocity = 20
    red.radius = 12
    red.power = False
    red.power_timeout = 5
    clock.schedule_unique(activate_power_red, red.power_timeout)

    green.velocity = 10
    green.radius = 20
    green.power = False
    green.power_timeout = 30
    clock.schedule_unique(activate_power_green, green.power_timeout)

    grey.velocity = 5
    grey.radius = 40
    grey.power = False
    grey.power_timeout = 15
    clock.schedule_unique(activate_power_grey, grey.power_timeout)

    item.active = False

    timer = 60
    clock.schedule(activate_item, 2.0)
    clock.schedule_interval(reduce_timer, 1)

    music.play("game")


music.play("menu")
pgzrun.go()
