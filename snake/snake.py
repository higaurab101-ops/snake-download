import pygame
import random
import sys, os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
running = True
game_state = "menu"
Base_width,Base_height = 600,675
window_width = 600
window_height = 675
screen = pygame.display.set_mode((window_width, window_height),pygame.RESIZABLE)
game_surface_surface = pygame.Surface((Base_width,Base_height))
x = 0
y = 75
l = 50
game_surface = pygame.image.load(resource_path("checkerboard.svg.png"))
game_surface = pygame.transform.scale(game_surface,(600,600))
apple = pygame.image.load(resource_path("apple.png"))
high_score_clock = pygame.image.load(resource_path("pastbestclock.png"))
present_clock = pygame.image.load(resource_path("present.png"))
apple=pygame.transform.scale(apple,(50,50))
apple_score = pygame.image.load(resource_path("apple.png"))
apple_score =pygame.transform.scale(apple_score,(50,50))
high_score_trophy = pygame.image.load(resource_path("trophy.png"))
high_score_trophy=pygame.transform.scale(high_score_trophy,(100,100))
left = False
right = True
up = False
down = False
fullscreen = False
fruits = [random.randint(50,550),
          random.randint(50,550)]
speed = l
clock = pygame.time.Clock()
move_timer = 0
move_delay = 100
body_size = 1
segment_number = 0
segments = [(x,y)]
title = pygame.font.SysFont(None,200)
instruction = pygame.font.SysFont(None,50)
title = pygame.font.SysFont(None,200)
instruction = pygame.font.SysFont(None,50)
high_score = pygame.font.SysFont(None,50)
fruit_count = pygame.font.SysFont(None,50)
present_time = pygame.font.SysFont(None,50)
high_time = pygame.font.SysFont(None,50)
time_score = 0
high_time_score = 0
go = pygame.font.SysFont(None,60)
gtm = pygame.font.SysFont(None,45)
gtg = pygame.font.SysFont(None,45)
hi = 0
score = 0
time_score_second = 0
high_time_score_second = 0
bite_sound = pygame.mixer.Sound(resource_path("apple_bite.wav"))
hit_sound = pygame.mixer.Sound(resource_path("hitting_wall.wav"))
while running:
    keys = pygame.key.get_pressed()
    game_surface_surface.fill((0,0,0))
    pygame.display.set_caption("Snake")

    if game_state == "menu":
        title_text = title.render("Snake!",True,(255,255,255))
        instruction_text = instruction.render("Press s to start",True,(255,255,255))
        game_surface_surface.blit(title_text,(50,50))
        game_surface_surface.blit(instruction_text,(150,300))
        pygame.display.update()
        if keys[pygame.K_s]:
            game_state = "playing"

    if game_state == "playing":
        pygame.draw.rect(game_surface_surface,(100,100,100),(0,0,600,75))
        game_surface_surface.blit(game_surface,(0,75))
        game_surface_surface.blit(high_score_trophy,(5,1))
        high_score_text = high_score.render(f"{hi}",True,(255,255,255))
        fruit_count_text = fruit_count.render(f"{score}",True,(255,255,255))
        time_score_text = present_time.render(f"{int(time_score/60)}:{int(time_score_second)}",True,(255,255,255))
        high_time_text = high_time.render(f"{int(high_time_score/60)}:{int(high_time_score_second)}",True,(255,255,255))
        game_surface_surface.blit(apple_score,(200,25))
        game_surface_surface.blit(high_score_clock,(450,25))
        game_surface_surface.blit(present_clock,(300,25))
        game_surface_surface.blit(high_score_text,(100,25))
        game_surface_surface.blit(fruit_count_text,(250,30))
        game_surface_surface.blit(time_score_text,(365,30))
        game_surface_surface.blit(high_time_text,(505,30))

        head_x,head_y = segments[0]
        head_pos = (x,y)
        for segment in segments:
            player = pygame.draw.rect(game_surface_surface, (0,150,0), (*segment, l, l))
            head_rect = pygame.draw.rect(game_surface_surface, (0,150,0), (head_x,head_y, l, l))

        fruit_png = game_surface_surface.blit(apple,(fruits[0],fruits[1]))
        eye = pygame.draw.circle(game_surface_surface,(0,0,0),(head_x+25,head_y+25),5)


# move head
        if move_timer > move_delay:
            move_timer = 0

            if ((up and y==75) or (down and y==550) or (left and x==0) or (right and x==550) or head_pos in segments[1:]):
                hit_sound.set_volume(0.2)
                hit_sound.play()
                game_state = "game over"

            if right and x<550:
                x += l
            elif left and x>0:
                x -= l
            elif down and y<550:
                y += l
            elif up and y>75:
                y -= l


# add new head
            segments.insert(0, head_pos)

# remove last segment (normal movement)
            segments.pop()

            if head_rect.colliderect(fruit_png):
                fruits = [random.randint(50,550),
                random.randint(50,550)]
                bite_sound.set_volume(0.2)
                bite_sound.play()
                segments.insert(0, (x, y))
                score += 1

        

        if keys[pygame.K_LEFT] and not right:
            right=up=down= False
            left = True                

        if keys[pygame.K_RIGHT] and not left:
            left=up=down= False
            right = True

        if keys[pygame.K_UP] and not down:
            right=left=down= False
            up = True                

        if keys[pygame.K_DOWN] and not up:
            right=up=left= False
            down = True                

        move_timer += clock.get_time()


        pygame.display.update()
        clock.tick(60)
        if time_score!=0:
            time_score_second = time_score%60

        time_score+=1/60

    if game_state=="game over":
        go0 = go.render("Game Over",True,(255,255,255))
        gtm0= gtg.render("Press m to go back to main menu",True,(255,255,255))
        gtg0 = gtm.render("Press r to restart",True,(255,255,255))
        game_surface_surface.blit(go0,(175,50))
        game_surface_surface.blit(gtg0,(170,150))
        game_surface_surface.blit(gtm0,(85,200))
        if keys[pygame.K_r]:
            game_state = "playing"
            score = 0

        if keys[pygame.K_m]:
            game_state = "menu"
            score = 0

        if score > hi:
            hi = score
            
        if time_score > high_time_score:
            high_time_score = time_score
            high_time_score_second = time_score%60 


        x,y = 0,75
        segments = [(x,y)]
        left=up=down= False
        right = True
        score = 0
        time_score = 0

        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type==pygame.VIDEORESIZE:
            window_width, window_height = event.w, event.h
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_f:
                fullscreen =  not fullscreen           

                if fullscreen:
                    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    window_width, window_height = screen.get_size()
                else:
                    window_width,window_height = 800,800
                    screen = pygame.display.set_mode((window_width,window_height), pygame.RESIZABLE)


    x_offset = (window_width - Base_width) // 2
    y_offset = (window_height - Base_height) // 2

    screen.fill((0,0,0))  # background (black bars)
    screen.blit(game_surface_surface, (x_offset, y_offset))

pygame.quit()
        