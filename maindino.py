import pygame
import random

pygame.init()

# resolution
display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))

# win title
pygame.display.set_caption('Run, Dino! Run!')

# Sounds
pygame.mixer.music.load("sounds/background.mp3")
pygame.mixer.music.set_volume(0.5)

jump_sound = pygame.mixer.Sound('sounds/Jump.wav')
fall_sound = pygame.mixer.Sound('sounds/Bdish.wav')
button_sound = pygame.mixer.Sound('sounds/button.wav')

# window icon
icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)


# init images
cactus_img = [pygame.image.load('img/Cactus0.png'), pygame.image.load('img/Cactus1.png'),
              pygame.image.load('img/Cactus2.png')]

cactus_options = [69, 449, 37, 410, 40, 420]

stone_img = [pygame.image.load('img/stone0.png'),
             pygame.image.load('img/stone1.png')]
cloud_img = [pygame.image.load('img/cloud0.png'),
             pygame.image.load('img/cloud1.png')]

dino_img = [pygame.image.load('img/dino0.png'), pygame.image.load('img/dino1.png'),
            pygame.image.load(
                'img/dino2.png'), pygame.image.load('img/dino3.png'),
            pygame.image.load('img/dino4.png')]

img_counter = 0

score = 0
max_score = 0

above_cactus = False

# dino size
user_width = 60
user_height = 100

# cactus
cactus_width = 20
cactus_height = 70

# spawn cactus

cactus_x = display_width - 50
cactus_y = display_height - cactus_height - 100

# spawn user
user_x = display_width // 3
user_y = display_height - user_height - 100

# upd fps
clock = pygame.time.Clock()

# jump dino
jump_dino = False
jump_counter = 30


class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            # pygame.draw.rect(display, (224, 121, 31), (self.x, self.y, self.width, self.height))
            self.x -= self.speed
            return True
        else:
            return False
            # self.x = display_width + 100 + random.randrange(-80, 60)

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))


class Button:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.inactive_color = (13, 162, 58)
        self.active_color = (23, 204, 58)

    def draw(self, x, y, message, action=None, font_size = 30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pygame.draw.rect(display, self.active_color,
                             (x, y, self.width, self.height))

            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(300)
                if action is not None:
                    if action == quit:
                        pygame.quit()
                        quit()
                    else:
                        action()

        else:
            pygame.draw.rect(display, self.inactive_color,
                             (x, y, self.width, self.height))

        print_text(message=message, x = x + 10, y = y + 10, font_size=font_size)


def game_cycle():
    global jump_dino
    game = True
    cactus_arr = []
    create_cactus(cactus_arr)
    pygame.mixer.music.play(-1)
    land = pygame.image.load('img/background.png')

    stone, cloud = open_random_objects()

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # jump button
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            jump_dino = True
        if keys[pygame.K_ESCAPE]:
            pause()

        if jump_dino:
            jump()

        # scores counter init
        scores_counter(cactus_arr)

        # background color
        display.blit(land, (0, 0))

        # scores
        print_text(f'Scores: {score}', 700, 10)

        # draw cactus
        draw_array(cactus_arr)

        # draw objects
        move_objects(stone, cloud)

        # draw dino
        draw_dino()

        if check_collision(cactus_arr):
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(fall_sound)
            game = False

        pygame.display.update()

        clock.tick(60)

    return game_over()


def jump():
    global user_y, jump_dino, jump_counter
    if jump_counter >= -30:
        if jump_counter == 30:
            pygame.mixer.Sound.play(jump_sound)
        if jump_counter == -30:
            pygame.mixer.Sound.play(fall_sound)
        user_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 30
        jump_dino = False


def create_cactus(array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 600, height, width, img, 4))


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 150
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(200, 350)

    return radius


def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = cactus_img[choice]
            width = cactus_options[choice * 2]
            height = cactus_options[choice * 2 + 1]

            cactus.return_self(radius, height, width, img)


def open_random_objects():
    choice = random.randrange(0, 2)
    img_of_stone = stone_img[choice]

    choice = random.randrange(0, 2)
    img_of_cloud = cloud_img[choice]

    stone = Object(display_width, display_height - 80, 10, img_of_stone, 4)
    cloud = Object(display_width, 80, 70, img_of_cloud, 2)

    return stone, cloud


def move_objects(stone, cloud):
    check = stone.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]
        stone.return_self(display_width, 500 +
                          random.randrange(10, 80), stone.width, img_of_stone)

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(display_width, random.randrange(
            10, 80), cloud.width, img_of_cloud)


def draw_dino():
    global img_counter
    if img_counter == 25:
        img_counter = 0

    display.blit(dino_img[img_counter // 5], (user_x, user_y))
    img_counter += 1


def print_text(message, x, y, font_color=(0, 0, 0), font_type='font/Thintel.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    pygame.mixer.music.pause()
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text('Paused. Press enter to continue ', 270, 300)

        # jump button
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)
    pygame.mixer.music.unpause()


def check_collision(barriers):
    for barrier in barriers:
        if barrier.y == 449:
            if not jump:
                if barrier.x <= user_x + user_width - 22 <= barrier.x + barrier.width:
                    return True
            elif jump_counter >= 0:
                if user_y + user_height - 5 >= barrier.y:
                    if barrier.x <= user_x + user_width - 22 <= barrier.x + barrier.width:
                        return True
            else:
                if user_y + user_height - 10 >= barrier.y:
                    if barrier.x <= user_x <= barrier.x + barrier.width:
                        return True
        else:
            if not jump:
                if barrier.x <= user_x + user_width + 5 <= barrier.x + barrier.width:
                    return True
            elif jump_counter == 10:
                if user_y + user_height - 5 >= barrier.y:
                    if barrier.x <= user_x + user_width - 5 <= barrier.x + barrier.width:
                        return True
            elif jump_counter <= 1:
                if user_y + user_height - 2 >= barrier.y:
                    if barrier.x <= user_x + 13 <= barrier.x + barrier.width:
                        return True
            elif jump_counter >= 1:
                if user_y + user_height - 2 >= barrier.y:
                    if barrier.x <= user_x + user_width - 22 <= barrier.x + barrier.width:
                        return True
            else:
                if user_y + user_height - 3 >= barrier.y:
                    if barrier.x <= user_x + user_width + 5 <= barrier.x + barrier.width:
                        return True

    return False


def game_over():
    global score, max_score
    if score > max_score:
        max_score = score

    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        print_text('Game Over. Press Enter to play again, Esc to exit', 210, 300)
        print_text(f'Max scores: {max_score}', 350, 325)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(15)


def scores_counter(barriers):
    global score, above_cactus

    if not above_cactus:
        for barrier in barriers:
            if barrier.x <= user_x + user_width / 2 <= barrier.x + barrier.width:
                if user_y + user_height - 5 <= barrier.y:
                    above_cactus = True
                    break
    else:
        if jump_counter == -30:
            score += 1
            above_cactus = False


def show_menu():
    menu_background = pygame.image.load('img/Menu.png')
    show = True
    
    start_button = Button(150, 70)
    quit_button = Button(150, 70)
    

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(menu_background, (0, 0))

        start_button.draw(330, 200, 'Start game', start_game, 50)
        quit_button.draw(330, 300, 'Leave :(((', quit, 50)
        pygame.display.update()
        clock.tick(60)


def start_game():
    global score, make_jump, jump_counter, user_y

    while game_cycle():
        score = 0
        make_jump = False
        jump_counter = 30
        user_y = display_height - user_height - 100



show_menu()

while game_cycle():
    score = 0
    make_jump = False
    jump_counter = 30
    user_y = display_height - user_height - 100

pygame.quit()
quit()
