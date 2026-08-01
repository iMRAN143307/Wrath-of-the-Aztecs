
import asyncio
import os
import random
import sys

import pygame

SONG_END = pygame.USEREVENT + 1
LOSE = pygame.USEREVENT + 2
WIN = pygame.USEREVENT + 3

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
screen = pygame.display.set_mode((1280, 720))

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

    def load_and_scale(filename, size, transparent):
        if transparent == False:
            unscaled = pygame.image.load(resource_path(f"{filename}.png")).convert()
        else:
            unscaled = pygame.image.load(resource_path(f"{filename}.png")).convert_alpha()
        return pygame.transform.scale(unscaled, size)

    song0 = "aw1.ogg"
    song1 = "aw2.ogg"
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
        pygame.Rect(3000, 150, 75, 600),
        pygame.Rect(3400, 170, 200, 60),
        pygame.Rect(3850, 390, 150, 600),
        pygame.Rect(4200, 200, 125, 75),
        pygame.Rect(4500, 100, 125, 75),
        pygame.Rect(5000, 400, 100, 400),
        pygame.Rect(5400, 300, 250, 100),
        pygame.Rect(600 + 5200, 400, 200, 50),
        pygame.Rect(850 + 5200, 180, 200, 50),
        pygame.Rect(1200 + 5200, 200, 50, 520),
        pygame.Rect(1400 + 5200, 480, 250, 75),
        pygame.Rect(1925 + 5200, 275, 80, 600),
        pygame.Rect(2400 + 5200, 190, 100, 225),
        pygame.Rect(2566 + 5200, 520, 150, 50),
        pygame.Rect(3000 + 5200, 150, 75, 600),
        pygame.Rect(3400 + 5200, 170, 200, 60),
        pygame.Rect(3850 + 5200, 390, 150, 600),
        pygame.Rect(4200 + 5200, 200, 125, 75),
        pygame.Rect(9850, 300, 150, 50),
        pygame.Rect(10400, 120, 50, 700)
    ]
    player_pos = pygame.Rect(300, 600, 50, 77)
    timer = 32.0
    integer_timer = "START"
    fontObj = pygame.font.Font(None, 64)
    background = load_and_scale("background", (1280, 720), False)
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
    wall = load_and_scale("wall", (162, 654), True)
    scaffolding = load("scaffolding")
    platformextend = load("platformextend")
    flood = load_and_scale("flood", (720, 720), True)
    large_flood = load_and_scale("flood", (2000, 1600), True)
    water = load_and_scale("water", (960, 720), False)
    house = load_and_scale("house", (720, 720), True)
    small_house = load_and_scale("house", (200, 200), True)
    flood_edge = 0
    lost = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SONG_END:
                song_index = (song_index + 1) % len(playlist)
                pygame.mixer.music.load(playlist[song_index])
                pygame.mixer.music.play()
            if event.type == LOSE:
                lost = True
            if event.type == WIN:
                lost = False

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
        if keys[pygame.K_r] and lost != None:
            lost = None
            jumping = 0
            grounded = False
            platforms_on_screen = []
            all_platforms = [
                pygame.Rect(600, 400, 200, 50),
                pygame.Rect(850, 180, 200, 50),
                pygame.Rect(1200, 200, 50, 520),
                pygame.Rect(1400, 480, 250, 75),
                pygame.Rect(1925, 275, 80, 600),
                pygame.Rect(2400, 190, 100, 225),
                pygame.Rect(2566, 520, 150, 50),
                pygame.Rect(3000, 150, 75, 600),
                pygame.Rect(3400, 170, 200, 60),
                pygame.Rect(3850, 390, 150, 600),
                pygame.Rect(4200, 200, 125, 75),
                pygame.Rect(4500, 100, 125, 75),
                pygame.Rect(5000, 400, 100, 400),
                pygame.Rect(5400, 300, 250, 100),
                pygame.Rect(600 + 5200, 400, 200, 50),
                pygame.Rect(850 + 5200, 180, 200, 50),
                pygame.Rect(1200 + 5200, 200, 50, 520),
                pygame.Rect(1400 + 5200, 480, 250, 75),
                pygame.Rect(1925 + 5200, 275, 80, 600),
                pygame.Rect(2400 + 5200, 190, 100, 225),
                pygame.Rect(2566 + 5200, 520, 150, 50),
                pygame.Rect(3000 + 5200, 150, 75, 600),
                pygame.Rect(3400 + 5200, 170, 200, 60),
                pygame.Rect(3850 + 5200, 390, 150, 600),
                pygame.Rect(4200 + 5200, 200, 125, 75),
                pygame.Rect(9850, 300, 150, 50),
                pygame.Rect(10400, 120, 50, 700)
            ]
            player_pos = pygame.Rect(300, 600, 50, 77)
            timer = 32.0
            integer_timer = "START"
            flood_edge = 0

        if jumping != 0:
            player_pos.y -= jumping * dt
            jumping -= 200
            if psprite in prunr:
                psprite = pfjr
            elif psprite in prunl:
                psprite = pfjl


        platforms_on_screen = []

        if player_pos.x < 500:
            player_pos.x = 500
            flood_edge += 500 * dt
            for platform in all_platforms:
                platform.x += 500 * dt
                if platform.x < 1280 or platform.x + platform.w > 0:
                    platforms_on_screen.append(platform)
        elif player_pos.x > 720:
            player_pos.x = 720
            flood_edge -= 500 * dt
            for platform in all_platforms:
                platform.x -= 500 * dt
                if platform.x < 1280 or platform.x + platform.w > 0:
                    platforms_on_screen.append(platform)
        else:
            for platform in all_platforms:
                if platform.x < 1280 or platform.x + platform.w > 0:
                    platforms_on_screen.append(platform)

        if str(int(timer)) != integer_timer and int(timer) < 31:
            integer_timer = str(int(timer))

        timer -= dt

        if all_platforms[-1].x < 400 and lost == None:
            pygame.event.post(pygame.event.Event(WIN))
        elif player_pos.x < flood_edge - (720 - player_pos.y) and lost == None:
            pygame.event.post(pygame.event.Event(LOSE))

        flood_edge += 337 * dt

        screen.blit(background, (0, 0))

        if lost == None:

            screen.blit(fontObj.render(integer_timer, True, (255, 255, 255), None), (640, 50))

            for platform in platforms_on_screen:
                if platform.h > platform.w:
                    crop = (platform.w - wall.get_width() ,platform.h - wall.get_height())
                    cropped_surface = pygame.Surface((wall.get_width() + crop[0], wall.get_height() + crop[1]))
                    cropped_surface.fill(pygame.Color(60, 65, 60))
                    cropped_surface.blit(wall, crop)
                    screen.blit(cropped_surface, (platform.x, platform.y))

                elif platform.w >= platform.h:
                    size = (platform.w + 10, 720 - platform.y)
                    scalefolding = pygame.transform.scale(scaffolding, size)
                    size = (platform.w + 10, 1)
                    scaleextend = pygame.transform.scale(platformextend, size)
                    screen.blit(scalefolding, (platform.x, platform.y))
                    for i in range(platform.h):
                        screen.blit(scaleextend, (platform.x, platform.y + i))

            screen.blit(small_house, (10800 - (10400 - all_platforms[-1].x), 477))

            screen.blit(psprite, (player_pos.x - 14, player_pos.y))

            screen.blit(flood, (flood_edge - 720, 0))
            screen.blit(water, (flood_edge - (720 + 960), 0))

        elif lost == True:
            screen.blit(fontObj.render("GAME OVER", True, (255, 255, 255), None), (520, 50))
            screen.blit(house, (280, 0))
            screen.blit(large_flood, (0, 0))

        elif lost == False:
            screen.blit(fontObj.render("CONGRATULATIONS", True, (255, 255, 255), None), (460, 50))
            screen.blit(house, (280, 0))

        pygame.display.flip()

        dt = clock.tick(60) / 1000
        await asyncio.sleep(0)

    pygame.mixer.music.stop()
    pygame.quit()

asyncio.run(main())
