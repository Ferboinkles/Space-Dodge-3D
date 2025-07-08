from vpython import *
import random

# Setup scene
scene.background = color.black
scene.width = 801
scene.height = 601
scene.title = "Asteroid Dodger"
scene.forward = vector(0, 0, 1)

# Camera initial position
scene.camera.pos = vector(0, 0, 0)
scene.camera.axis = vector(0, 0, 1)

# Starfield
for _ in range(300):
    sphere(pos=vector(random.uniform(-100,100),
                      random.uniform(-100,100),
                      random.uniform(-100,100)),
           radius=0.1,
           color=color.white,
           emissive=True)

# Cockpit (player's view)
cockpit = box(pos=vector(0.1, -0.25, 1), size=vector(1, 0.5, 0.5), color=color.green)
from vpython import *
import random

# Setup scene
scene.background = color.black
scene.width = 800
scene.height = 600
scene.title = "Space Dodge V2"
scene.forward = vector(0, 0, 1)

# Camera initial position
scene.camera.pos = vector(0, 0, 0)
scene.camera.axis = vector(0, 0, 1)

# Starfield
for _ in range(300):
    sphere(pos=vector(random.uniform(-100,100),
                      random.uniform(-100,100),
                      random.uniform(-100,100)),
           radius=0.1,
           color=color.white,
    )
    asteroid.velocit
# Asteroids
asteroids = []

def spawn_asteroid():
    x = random.uniform(-10, 10)
    y = random.uniform(-5, 5)
    z = scene.camera.pos.z + 50
    size = random.uniform(0.5, 2)
    asteroid = sphere(
        pos=vector(x, y, z),
        radius=size,
        color=vector(0.3, 0.3, 0.3),
        shininess=0.7
    )
    asteroid.velocity = vector(0, 0, -random.uniform(0.005, 0.002))
    asteroids.append(asteroid)

for _ in range(5):
    spawn_asteroid()

# Movement
move_speed =4
turn_speed = 1

# Main loop
while True:
    rate(60)

    # Detect key presses directly
    keys = keysdown()

    if 'left' in keys or 'ArrowLeft' in keys:
        scene.camera.pos.x -= turn_speed
    if 'right' in keys or 'ArrowRight' in keys:
        scene.camera.pos.x += turn_speed

    # Move forward automatically
    scene.camera.pos.z += move_speed

    # Move asteroids and check collisions
    for asteroid in asteroids:
        asteroid.pos += asteroid.velocity

        # Recycle asteroid
        if asteroid.pos.z < scene.camera.pos.z - 10:
            asteroid.visible = False
            asteroids.remove(asteroid)
            spawn_asteroid()
            continue

        # Collision detection (simple bounding)
        dist = mag(asteroid.pos - scene.camera.pos)
        if dist < asteroid.radius + 0.5:
            print("💥 Hit!")
