import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 800
display_height = 600
apple_thickness = block_size = 20
snake_list = []
coordinates = []
for x in range(0, display_width - block_size + 1, block_size):
    for y in range(0, display_height - block_size + 1, block_size):
        coordinates.append([float(x), float(y)])
print(coordinates)
FPS = 15
direction = "right"
clock = pygame.time.Clock()
small_font = pygame.font.Font("timeburnerbold.ttf", 25)
med_font = pygame.font.SysFont("timeburnerbold.ttf", 50)
large_font = pygame.font.SysFont("timeburnerbold.ttf", 80)

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake')

snakehead_image = pygame.image.load('snakehead.png')
snakehead_image = pygame.transform.scale(snakehead_image, (block_size, block_size))
apple = pygame.image.load('apple.png')
apple = pygame.transform.scale(apple, (apple_thickness, apple_thickness))
tail_image = pygame.image.load('tail.png')
tail_image = pygame.transform.scale(tail_image, (block_size, block_size))
icon_image = pygame.image.load('apple.png')
pygame.display.set_icon(icon_image)



def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        game_display.fill(white)
        message_to_screen("Welcome to Snake",
                          green,
                          -100,
                          size="large")
        message_to_screen("The objective of the game is to eat red apples",
                          black,
                          -30)
        message_to_screen("The more apples you eat, the longer you get",
                          black,
                          10)
        message_to_screen("If you run into yourself, or the edges, you die!",
                          black,
                          50)
        message_to_screen("Press C to play or Q to quit.",
                          black,
                          180)
        pygame.display.update()
        clock.tick(5)

def snake(block_size, snake_list):
    if direction == "right":
        head = pygame.transform.rotate(snakehead_image, 270)
    if direction == "left":
        head = pygame.transform.rotate(snakehead_image, 90)
    if direction == "up":
        head = snakehead_image
    if direction == "down":
        head = pygame.transform.rotate(snakehead_image, 180)
    game_display.blit(head, (snake_list[-1][0], snake_list[-1][1]))
    if len(snake_list) > 1:
        next_to_end = snake_list[1]
        end = snake_list[0]
        if next_to_end[0] < end[0] and next_to_end[1] == end[1]:
            tail = pygame.transform.rotate(tail_image, 90)
        if next_to_end[0] > end[0] and next_to_end[1] == end[1]:
            tail = pygame.transform.rotate(tail_image, 270)
        if next_to_end[0] == end[0] and next_to_end[1] < end[1]:
            tail = tail_image
        if next_to_end[0] == end[0] and next_to_end[1] > end[1]:
            tail = pygame.transform.rotate(tail_image, 180)
        game_display.blit(tail, (snake_list[0][0], snake_list[0][1]))
    for cor in snake_list[1:-1]:
        pygame.draw.rect(game_display, green, [cor[0], cor[1], block_size, block_size])

def text_objects(text, color, size):
    if size == "small":
        text_surface = small_font.render(text, True, color)
    elif size == "medium":
        text_surface = med_font.render(text, True, color)
    elif size == "large":
        text_surface = large_font.render(text, True, color)
    return text_surface, text_surface.get_rect()

def message_to_screen(msg, color, y_displace = 0, size = "small"):
    text_surface, text_rect = text_objects(msg, color, size)
    text_rect.center = (display_width / 2), (display_height / 2) + y_displace
    game_display.blit(text_surface, text_rect)

def score(score):
    text = small_font.render("Score: " + str(score), True, black)
    game_display.blit(text, [0, 0])

def rand_apple_gen():
    copy = coordinates[:]
    for coor in snake_list:
        copy.remove(coor)
    rand_coord = random.randint(0, len(copy))
    rand_apple_x = copy[rand_coord][0]
    rand_apple_y = copy[rand_coord][1]
    return rand_apple_x, rand_apple_y

def game_loop():
    global direction
    global snake_list
    direction = "right"
    game_exit = False
    game_over = False
    lead_x = display_width / 2
    lead_y = display_height / 2
    lead_x_change = block_size
    lead_y_change = 0
    snake_list = []
    snake_length = 1
    rand_apple_x, rand_apple_y = rand_apple_gen()
    while not game_exit:
        while game_over:
            game_display.fill(black)
            message_to_screen("Game over",
                              red,
                              y_displace=-100,
                              size="large")
            message_to_screen("Press C to play again or Q to quit",
                              white,
                              y_displace=50,
                              size="medium")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                    if event.key == pygame.K_c:
                        game_loop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "right":
                    lead_x_change = -block_size
                    lead_y_change = 0
                    direction = "left"
                elif event.key == pygame.K_RIGHT and direction != "left":
                    lead_x_change = block_size
                    lead_y_change = 0
                    direction = "right"
                elif event.key == pygame.K_UP and direction != "down":
                    lead_y_change = -block_size
                    lead_x_change = 0
                    direction = "up"
                elif event.key == pygame.K_DOWN and direction != "up":
                    lead_y_change = block_size
                    lead_x_change = 0
                    direction = "down"

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            game_over = True

        lead_x += lead_x_change
        lead_y += lead_y_change
        game_display.fill(white)
        game_display.blit(apple, (rand_apple_x, rand_apple_y))
        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]
        for cors in snake_list[:-1]:
            if cors == snake_head:
                game_over = True
        snake(block_size, snake_list)
        score(snake_length - 1)
        pygame.display.update()
        if rand_apple_x <= lead_x <= rand_apple_x + apple_thickness \
                and rand_apple_x <= lead_x + block_size <= rand_apple_x + apple_thickness:
            if rand_apple_y <= lead_y <= rand_apple_y + apple_thickness \
                    and rand_apple_y <= lead_y + block_size <= rand_apple_y + apple_thickness:
                    rand_apple_x, rand_apple_y = rand_apple_gen()
                    snake_length += 1
        clock.tick(FPS)

    pygame.quit()
    quit()
game_intro()
game_loop()