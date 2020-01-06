import pygame
pygame.init()
import random

# Colors-RGB value
white = (255, 255, 255)
red = (255,0,0)
black =(0,0,0)

#Screen width and height
screen_width = 700
screen_height = 500

#Creating Window
gamewindow = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Snake Game")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)


def text_score(text, color, x, y):
    #render-function of pygame(text, antialising-make high resolution to low resolution, color)
    screen_text = font.render(text, True, color)
    gamewindow.blit(screen_text, [x,y])

def plot_snake(gamewindow, color, snk_list,snake_size):
    # Returns a tuple containing the coordinate of the head
    for x,y in snk_list:
        pygame.draw.rect(gamewindow, color, (x, y, snake_size, snake_size))


def welcome():
    exit_game = False
    while not exit_game:
        gamewindow.fill((170, 145, 68))
        text_score("Welcome to Snakes", black, 200, 150)
        text_score("Press Enter to begin!", black, 190, 200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()
        pygame.display.update()
        clock.tick(60)

#Game Loop- for handling all the events
def gameloop():
    # game specific variables
    exit_game = False
    game_over = False
    snake_x = 40
    snake_y = 50
    snake_size = 20
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 5
    fps = 60 #frame per second- how many frames are displayed in 1 sec


    with open("snake_highscore.txt", "r") as f:
        highscore = f.read()

    while not exit_game:
        if game_over:
            #update new high score
            with open("snake_highscore.txt", "w") as f:
                f.write(str(highscore))

            gamewindow.fill(white)
            text_score("Game Over! Press Enter To Continue", red, 95, 180)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x =init_velocity
                        velocity_y = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                            velocity_y = -init_velocity
                            velocity_x = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                            velocity_y = init_velocity
                            velocity_x = 0
            snake_x += velocity_x
            snake_y += velocity_y


            if abs(snake_x - food_x) < 13 and abs(snake_y - food_y) <13:
                score+=10
                # Generate food at random location within the width and height
                food_x = random.randint(20, screen_width /2)
                food_y = random.randint(20, screen_height / 2)
                snk_length+=5

                #Save high score into the highscore.txt file
                if score> int(highscore):
                    highscore = score

            gamewindow.fill(white)
            text_score("Score: " + str(score) + " Highscore: "+str(highscore), red, 5, 5)
            pygame.draw.rect(gamewindow, red, (food_x, food_y, snake_size, snake_size))

            # Draws the snake body
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)


            # for every part check if the head collides with the body
            if len(snk_list) > snk_length:
                del snk_list[0]

            # remove the first instance from the body of the snake.
            if head in snk_list[:-1]:
                game_over = True

            #window border collision detection
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
            plot_snake(gamewindow, black, snk_list, snake_size)
        clock.tick(fps) #update time with frame
        pygame.display.update()

    pygame.quit()
    quit()
welcome()