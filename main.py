from sys import path
path.append("./GameEngine")

import pygame

from atlas import Atlas
from game_object import GameObject
from render_group import RenderGroup
from shield import Shield
from ship import Ship
from turret import Turret


def main():
    pygame.init()

    size = (1280, 720)
    background = 50, 50, 50
    screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)

    # Load all the stuffs
    explosion_atlas_image = pygame.image.load("Assets/Explosions/explosion1.png").convert_alpha()
    ship_image = pygame.image.load("Assets/SpaceShooterRedux/PNG/playerShip2_blue.png").convert_alpha()
    shield_images = [
        pygame.image.load("Assets/SpaceShooterRedux/PNG/Effects/shield3.png").convert_alpha(),
        pygame.image.load("Assets/SpaceShooterRedux/PNG/Effects/shield2.png").convert_alpha(),
        pygame.image.load("Assets/SpaceShooterRedux/PNG/Effects/shield1.png").convert_alpha()
    ]
    turret_image = pygame.image.load("Assets/SpaceShooterRedux/PNG/Parts/turretBase_big.png").convert_alpha()
    turret_gun_image = pygame.image.load("Assets/SpaceShooterRedux/PNG/Parts/gun04.png").convert_alpha()
    projectile_image = pygame.image.load("Assets/SpaceShooterRedux/PNG/Lasers/laserRed06.png").convert_alpha()

    # Create world
    pygame.display.set_icon(ship_image)
    pygame.display.set_caption("Game")
    world_rect = pygame.Rect(0, 0, size[0] * 2, size[1] * 2)
    screen_rect = screen.get_rect()

    # Create player
    player = Ship(ship_image, 0.9)
    player.set_pos(pygame.Vector2(screen_rect.width / 2.0, screen_rect.height / 2.0))
    player.set_scale(0.8)
    linear_velocity = 200.0
    angular_velocity = 1.5

    collision_group = pygame.sprite.Group()

    # Create a turret
    explosion_atlas = Atlas(explosion_atlas_image, (256, 256))
    turret = Turret(turret_image, projectile_image, collision_group, explosion_atlas)
    turret.set_scale(1.25)
    turret.set_pos(pygame.Vector2(screen_rect.width * 0.75, screen_rect.height * 0.75))
    turret.set_target(player)

    # Add player and turret to group of game objects
    render_group = RenderGroup(player, world_rect, screen_rect, True)
    render_group.add(turret)
    render_group.move_to_back(turret)

    # Add player to collision group
    collision_group.add(player)

    # Attach shield to player
    shield = Shield(shield_images)
    shield.transform()
    player.attach(shield, (0, 0))
    collision_group.add(shield)

    # Attach gun to turret
    turret_gun = GameObject(turret_gun_image)
    turret.attach(turret_gun, (0, -15))

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Exit
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Handle input for movement
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_s]:
            player.set_heading(player.heading + angular_velocity)
        if pressed_keys[pygame.K_f]:
            player.set_heading(player.heading - angular_velocity)
        if pressed_keys[pygame.K_e]:
            player.set_velocity(linear_velocity)
        if pressed_keys[pygame.K_d]:
            player.set_velocity(player.velocity * 0.8)

        # Update groups
        render_group.update(clock.get_time())

        # Render
        screen.fill(background)
        render_group.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
