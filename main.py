import math
import pgzrun
import pygame
import random

WIDTH = 1000
HEIGHT = 1000

TITLE = "Painter PgZero"

blue = Actor("blue", (50, 50))
blue.velocity = 10
blue.max_velocity = 10
blue.acceleration = 0.1
blue.radius = 20
blue.color = "#2184D3"
blue.keys = {"left": "q", "right": "e", "forward": "w"}

red = Actor("red", (WIDTH - 50, 50))
red.velocity = 20
red.max_velocity = 20
red.acceleration = 0.1
red.radius = 12
red.color = "#DD4E54"
red.keys = {"left": "i", "right": "p", "forward": "o"}

green = Actor("green", (50, HEIGHT - 50))
green.velocity = 10
green.max_velocity = 10
green.acceleration = 0.1
green.radius = 20
green.color = "#49B47E"
green.keys = {"left": "left", "right": "right", "forward": "up"}

grey = Actor("grey", (WIDTH - 50, HEIGHT - 50))
grey.velocity = 5
grey.max_velocity = 5
grey.acceleration = 0.1
grey.radius = 40
grey.color = "#937F7C"
grey.keys = {"left": "kp7", "right": "kp9", "forward": "kp8"}

players = [blue, red, green, grey]

color_surface = pygame.Surface((WIDTH, HEIGHT))
color_surface.fill("white")

item = Actor("bomb")
item.active = False
item.type = "bomb"


def draw():
    screen.blit(color_surface, (0, 0))

    for pl in players:
        pl.draw()

    if item.active:
        item.draw()


def update():
    for pl in players:
        update_player(pl)


def update_player(player):
    if keyboard[player.keys["left"]]:
        player.angle += 1 + player.velocity / 2
    if keyboard[player.keys["right"]]:
        player.angle -= 1 + player.velocity / 2
    if keyboard[player.keys["forward"]]:
        player.velocity += player.acceleration

    if player.velocity > player.max_velocity:
        player.velocity = player.max_velocity

    if player.velocity < 0:
        player.velocity = 0

    player.x += math.sin(math.radians(player.angle + 90)) * player.velocity
    player.y += math.cos(math.radians(player.angle + 90)) * player.velocity

    if not (0 <= player.x < WIDTH and 0 <= player.y < HEIGHT):
        player.x -= math.sin(math.radians(player.angle + 90)) * player.velocity
        player.y -= math.cos(math.radians(player.angle + 90)) * player.velocity
        player.angle += random.randint(100, 250)

    pygame.draw.circle(color_surface, player.color, player.pos, player.radius)

    for other_player in players:
        if other_player == player:
            continue

        if player.colliderect(other_player):
            player.x -= math.sin(math.radians(player.angle + 90)) * player.velocity
            player.y -= math.cos(math.radians(player.angle + 90)) * player.velocity
            player.angle += random.randint(100, 250)

    if item.active and player.colliderect(item):
        if item.type == "bomb":
            pygame.draw.circle(color_surface, player.color, player.pos, 250)

        item.active = False
        clock.schedule(activate_item, 1.0 + random.random() * 5)


def activate_item():
    item.active = True
    item.x = random.randint(50, WIDTH - 50)
    item.y = random.randint(50, HEIGHT - 50)


clock.schedule(activate_item, 2.0)

pgzrun.go()
