import random

from vpython import *

# Scene setup
scene.width = 800
scene.height = 600
scene.title = "🚀 Dodge the Asteroids!"
scene.background = color.black
scene.camera.pos = vector(0, 1, -8)  # Zoomed-in starting position
scene.camera.axis = vector(0, -0.5, 8)  # Looking forward (+z)

# Rocket parts
rocket_base = vector(0, 0, 0)

body = cylinder(pos=rocket_base, axis=vector(0, 0, 2), radius=0.15, color=color.red)
nose = cone(pos=rocket_base + vector(0, 0, 2), axis=vector(0, 0, 0.3), radius=0.15, color=color.white)
cockpit = sphere(pos=rocket_base + vector(0, 0.2, 1.5), radius=0.07, color=color.cyan)

# Fins
fins = []
fin_size = vector(0.05, 0.2, 0.01)
fin_positions = [
    vector(0.15, -0.15, 0.3), vector(-0.15, -0.15, 0.3),
    vector(0.15, -0.15, 1), vector(-0.15, -0.15, 1)
]
for pos in fin_positions:
    fins.append(box(pos=rocket_base + pos, size=fin_size, color=color.gray(0.5)))

# Flame
flame = cone(pos=rocket_base + vector(0, 0, -0.3), axis=vector(0, 0, -0.5),
             radius=0.1, color=color.orange, emissive=True, opacity=0.6)

# Combine rocket
rocket = compound([body, nose, cockpit, flame] + fins)
rocket.pos = vector(0, 0, 0)

# Stars
stars = []
for _ in range(150):
    stars.append(
        sphere(
            pos=vector(random.uniform(-25, 25), random.uniform(-25, 25), random.uniform(-60, -10)),
            radius=0.05,
            color=color.white,
            emissive=True
        )
    )

# Asteroids
asteroids = []
for _ in range(10):
    rock = sphere(
        pos=vector(random.uniform(-10, 10), random.uniform(-5, 5), random.uniform(5, 40)),
        radius=random.uniform(0.3, 0.6),
        color=color.gray(0.6)
    )
    rock.v = vector(0, 0, -0.2)
    asteroids.append(rock)

# Controls
move_direction = 0


def keydown(evt):
    global move_direction
    if evt.key == 'left':
        move_direction = -1
    elif evt.key == 'right':
        move_direction = 1


def keyup(evt):
    global move_direction
    if evt.key in ['left', 'right']:
        move_direction = 0


scene.bind('keydown', keydown)
scene.bind('keyup', keyup)

# Main game loop
game_over = False

while not game_over:
    rate(60)

    # Move rocket left/right
    rocket.pos.x += move_direction * 0.3
    scene.camera.pos.x = rocket.pos.x  # move camera with rocket

    # Move asteroids toward player
    for rock in asteroids:
        rock.pos += rock.v

        # Recycle rock
        if rock.pos.z < -10:
            rock.pos = vector(random.uniform(-10, 10), random.uniform(-5, 5), random.uniform(20, 40))

        # Check collision
        if mag(rocket.pos - rock.pos) < (0.5 + rock.radius):
            label(pos=vector(rocket.pos.x, 2, rocket.pos.z),
                  text="💥 Game Over!", height=30, color=color.red, box=False)
            print("💥 CRASH DETECTED!")
            game_over = True
            break
