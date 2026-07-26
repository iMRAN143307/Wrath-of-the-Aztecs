
import asyncio
import os
import random
import sys

import pygame

SONG_END = pygame.USEREVENT + 1


def resource_path(relative_path):
    try:
        base_path = sys.MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


async def main():
    def load(filename):
        image_path = resource_path(f"{filename}.png")
        return pygame.image.load(image_path).convert_alpha()

    def load_and_scale(filename):
        unscaled = pygame.image.load(resource_path(f"{filename}.png")).convert()
        return pygame.transform.scale(unscaled, (1280, 720))

    pygame.mixer.pre_init(44100, -16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    song0 = "aw1.wav"
    song1 = "aw2.wav"
    playlist = [song0, song1]
    pygame.mixer.music.set_endevent(SONG_END)
    pygame.mixer.music.load(random.choice(playlist))
    pygame.mixer.music.play()
    clock = pygame.time.Clock()
    running = True
    dt = 0
    jumping = 0
    grounded = False
    song_index = 0
    platforms_on_screen = []
    all_platforms = [
        pygame.Rect(600, 400, 200, 50),
        pygame.Rect(850, 180, 200, 50),
        pygame.Rect(1200, 200, 50, 520),
        pygame.Rect(1400, 480, 250, 75),
        pygame.Rect(1925, 275, 80, 600),
        pygame.Rect(2400, 190, 100, 225),
        pygame.Rect(2566, 520, 150, 50),
        pygame.Rect(3000, 150, 75, 600)
    ]
    player_pos = pygame.Rect(300, 600, 50, 77)
    camera_x = 0
    timer = 62.0
    integer_timer = "START"
    fontObj = pygame.font.Font(None, 64)
    background = load_and_scale("background")
    pf1r = load("mccopy")
    pf2r = load("mccopy1")
    pf3r = load("mccopy2")
    pf4r = load("mccopy3")
    pfjr = load("mcjump")
    pf1l = pygame.transform.flip(pf1r, True, False)
    pf2l = pygame.transform.flip(pf2r, True, False)
    pf3l = pygame.transform.flip(pf3r, True, False)
    pf4l = pygame.transform.flip(pf4r, True, False)
    pfjl = pygame.transform.flip(pfjr, True, False)
    prunr = [pf1r, pf1r, pf2r, pf2r, pf3r, pf3r, pf4r, pf4r]
    prunl = [pf1l, pf1l, pf2l, pf2l, pf3l, pf3l, pf4l, pf4l]
    psprite = pf1r
    prunindex = 0

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
            if psprite == pfjl:
                psprite = pf1l
            elif psprite == pfjr:
                psprite = pf1r
        for platform in platforms_on_screen:
            if player_pos.x + player_pos.w > platform.x and player_pos.x < platform.x + platform.w and player_pos.y + player_pos.h > platform.y and player_pos.y + player_pos.h < platform.y + platform.h and player_pos.y < platform.y and platform.y < player_pos.y + player_pos.h:
                player_pos.y = platform.y - player_pos.h
                grounded = True
                if psprite == pfjl:
                    psprite = pf1l
                elif psprite == pfjr:
                    psprite = pf1r
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
            if grounded == True:
                prunindex += 1
                prunindex = prunindex % 8
                psprite = prunl[prunindex]
        if keys[pygame.K_d]:
            player_pos.x += 500 * dt
            if grounded == True:
                prunindex += 1
                prunindex = prunindex % 8
                psprite = prunr[prunindex]

        if jumping != 0:
            player_pos.y -= jumping * dt
            jumping -= 200
            if psprite in prunr:
                psprite = pfjr
            elif psprite in prunl:
                psprite = pfjl


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

        if str(int(timer)) != integer_timer and int(timer) < 61:
            integer_timer = str(int(timer))

        timer -= dt

        screen.blit(background, (0, 0))

        screen.blit(fontObj.render(integer_timer, True, (255, 255, 255), None), (640, 50))

        for platform in platforms_on_screen:
            pygame.draw.rect(screen, "yellow", platform)

        pygame.draw.rect(screen, "white", player_pos)
        screen.blit(psprite, (player_pos.x - 14, player_pos.y))

        pygame.display.flip()

        dt = clock.tick(60) / 1000
        await asyncio.sleep(0)

    pygame.mixer.music.stop()
    pygame.quit()

asyncio.run(main())
