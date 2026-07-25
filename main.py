import pygame

SONG_END = pygame.USEREVENT + 1

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
screen = pygame.display.set_mode((1280, 720))
song0 = "aw1.wav"
song1 = "aw2.wav"
song2 = "gbd3.wav"
playlist = [song0, song1, song2]
pygame.mixer.music.set_endevent(SONG_END)
pygame.mixer.music.load(song0)
pygame.mixer.music.play()
clock = pygame.time.Clock()
running = True
dt = 0
jumping = 0
grounded = False
song_index = 0
platforms_on_screen = []
all_platforms = [pygame.Rect(600, 400, 200, 50), pygame.Rect(850, 180, 200, 50), pygame.Rect(1200, 200, 50, 520)]
player_pos = pygame.Rect(screen.get_width() / 2, 600, 50, 100)
camera_x = 0
timer = 60
integer_timer = "START"

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SONG_END:
            song_index = (song_index + 1) % len(playlist)
            pygame.mixer.music.load(playlist[song_index])
            pygame.mixer.music.play()

    grounded = False

    player_pos.y = player_pos.y + (500 * dt)
    if player_pos.y >= 600:
        player_pos.y = 600
        grounded = True
    else:
        for platform in platforms_on_screen:
            if player_pos.x + player_pos.w > platform.x and player_pos.x < platform.x + platform.w and player_pos.y + player_pos.h > platform.y and player_pos.y + player_pos.h < platform.y + platform.h and player_pos.y < platform.y and platform.y < player_pos.y + player_pos.h:
                player_pos.y = platform.y - player_pos.h
                grounded = True
                #soft platforms would use just this, hard platforms would use this plus the other 3
            elif player_pos.x + player_pos.w > platform.x and player_pos.x + player_pos.w < platform.x + platform.w and player_pos.y + player_pos.h > platform.y and player_pos.y + player_pos.h < platform.y + platform.h:
                player_pos.x = platform.x - player_pos.w
            elif player_pos.x < platform.x + platform.w and player_pos.x > platform.x and player_pos.y + player_pos.h > platform.y and player_pos.y + player_pos.h < platform.y + platform.h:
                player_pos.x = platform.x + platform.w
            elif player_pos.x + player_pos.w > platform.x and player_pos.x < platform.x + platform.w and player_pos.y < platform.y + platform.h and player_pos.y > platform.y:
                player_pos.y = platform.y + platform.h
                jumping = 0

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and grounded == True and jumping == 0:
        jumping = 3400
    if keys[pygame.K_s] and grounded == False:
        player_pos.y += 1200 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 500 * dt
    if keys[pygame.K_d]:
        player_pos.x += 500 * dt

    if jumping != 0:
        player_pos.y -= jumping * dt
        jumping -= 200

    platforms_on_screen = []

    if player_pos.x < 500:
        camera_x -= 500 * dt
        player_pos.x = 500
        for platform in all_platforms:
            platform.x += 500 * dt
            if platform.x < 1280 or platform.x + platform.w > 0:
                platforms_on_screen.append(platform)
    elif player_pos.x > 720:
        camera_x += 500 * dt
        player_pos.x = 720
        for platform in all_platforms:
            platform.x -= 500 * dt
            if platform.x < 1280 or platform.x + platform.w > 0:
                platforms_on_screen.append(platform)
    else:
        for platform in all_platforms:
            if platform.x < 1280 or platform.x + platform.w > 0:
                platforms_on_screen.append(platform)

    screen.fill("black")

    for platform in platforms_on_screen:
        pygame.draw.rect(screen, "yellow", platform)

    pygame.draw.rect(screen, "white", player_pos)

    if int(timer) != integer_timer:
        integer_timer = int(timer)
        #put integer_timer as text on the screen

    timer -= dt

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()
