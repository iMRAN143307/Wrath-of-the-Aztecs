import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
jumping = 0
grounded = False
platforms_on_screen = []
all_platforms = [pygame.Rect(screen.get_width() / 4, 400, 100, 50)]

player_pos = pygame.Rect(screen.get_width() / 2, 600, 50, 100)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    grounded = False

    player_pos.y = player_pos.y + (300 * dt)
    if player_pos.y >= 600:
        player_pos.y = 600
        grounded = True
    else:
        for platform in platforms_on_screen:
            if player_pos.x + player_pos.w > platform.x and player_pos.x < platform.x + platform.w and player_pos.y + player_pos.h > platform.y and player_pos.y + player_pos.h < platform.y + platform.h:
                player_pos.y = platform.y - player_pos.h
                grounded = True
                #soft platforms would use just this, hard platforms would use this plus the other 3
            elif player_pos.x + player_pos.w > platform.x and player_pos.x + player_pos.w < platform.x + platform.w and player_pos.y + player_pos.h > platform.y and player_pos.y + player_pos.h < platform.y + platform.h:
                player_pos.x = platform.x - player_pos.w
                print("left")
            elif player_pos.x < platform.x + platform.w and player_pos.x > platform.x and player_pos.y + player_pos.h > platform.y and player_pos.y + player_pos.h < platform.y + platform.h:
                player_pos.x = platform.x + platform.w
                print("right")
            elif player_pos.y < platform.y + platform.h:
                player_pos.y = platform.y + platform.h
                print("up")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and grounded == True and jumping == 0:
        jumping = 7000
    if keys[pygame.K_s] and grounded == False:
        player_pos.y += 1200 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 500 * dt
    if keys[pygame.K_d]:
        player_pos.x += 500 * dt

    if jumping != 0:
        player_pos.y -= jumping * dt
        jumping -= 200

    screen.fill("black")

    platforms_on_screen = []

    for platform in all_platforms:
        if platform.x < 1280 or platform.x > 0:
            platforms_on_screen.append(platform)

    for platform in platforms_on_screen:
        pygame.draw.rect(screen, "yellow", platform)

    pygame.draw.rect(screen, "white", player_pos)

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
