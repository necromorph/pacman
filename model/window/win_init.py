import pygame
import model.levels.level_init as levelinit
from pygame import *
from model.window.fonts import fonts
from model.window.menu import Menu
from model.window.gameover import GameOver


from model.player.pacman import Player
from model.player.ghosts import Monster

def create_window():
    # Объявляем переменные
    win_width = 800  # Ширина создаваемого окна
    win_height = 480  # Высота
    win_size = win_width, win_height  # Группируем ширину и высоту в одну переменную
    background_color = "#000000"

    done = True
    pygame.init()  # Инициация PyGame, обязательная строчка

    mixer.init()
    mixer.music.set_volume(-1)
    screen = display.set_mode(win_size)  # Создаем окошко
    Icon = image.load('F:/pacman_py/Images/Other/Trollman.png')
    display.set_icon(Icon)
    display.set_caption("Pac-Man")  # Пишем в шапку



    bg = Surface((win_width, win_height))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(background_color))  # Заливаем поверхность сплошным цветом

    # start menu
    points = [(300, 200, "Start Game", (135, 135, 135), (255, 255, 255), 0),
              (300, 250, "Quit Game", (135, 135, 135),  (255, 255, 255), 1)]

    game_menu = Menu(points)
    game_menu.menu(screen, bg)
    ###

    hero = Player(384, 352)

    left = right = up = down = False  # по умолчанию — стоим

    timer = pygame.time.Clock()
    text_str = fonts()
    mn = Monster(416, 352, 4, 0, 304, 336)

    score = 0
    lifes = 2
    level = 1

    e_p = levelinit.level_create(screen, hero, mn)

    mixer.stop()
    #mixer.music.load('F:/pacman_py/sound/pacman_chomp.wav')
    #mixer.music.play(-1, 0.0)
    mixer.music.load('F:/pacman_py/sound/AHA - Take On Me.mp3')
    mixer.music.play(-1, 1)
    while done:  # Основной цикл программы

        timer.tick(30)
        bg.fill(Color("#000000"))
        for e in event.get():  # Обрабатываем события
            if e.type == QUIT: #or (e.type == KEYUP and e.key == K_ESCAPE):
                done = False

            if e.type == KEYUP and e.key == K_ESCAPE:
                score = 0
                level = 0
                lifes = 3
                game_menu.menu(screen, bg)

            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True

            if e.type == KEYUP and e.key == K_UP:
                up = False

            if e.type == KEYUP and e.key == K_DOWN:
                down = False

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
        screen.blit(text_str.render("Lifes: " + str(lifes), 1, (255, 255, 255)), (200, 438))
        screen.blit(text_str.render("Score: " + str(score), 1, (255, 255, 255)), (200, 15))
        screen.blit(text_str.render("Level: " + str(level), 1, (255, 255, 255)), (450, 15))
        hero.update(left, right, up, down, e_p[0], e_p[2])  # передвижение
        mn.update(e_p[0], hero)  # передвигаем всех монстров

        for p in e_p[3]:
            if sprite.collide_circle(hero, p):
                e_p[3].remove(p)
                if score % 10000 == 0 and score != 0:
                    lifes += 1


        if sprite.collide_rect(hero, mn):
            lifes -= 1
            hero.rect.x = 384
            hero.rect.y = 352

        for p in e_p[2]:
            if sprite.collide_circle(hero, p):
                e_p[2].remove(p)
                score += 100;

        if lifes <= 0:
            mixer.music.stop()

            mixer.music.load('F:/pacman_py/sound/gm.mp3')
            mixer.music.play()

            game_over = [(300, 400, "Press Enter for new Game...", (135, 135, 135), (255, 255, 255), 1)]
            gm = GameOver(game_over)
            gm.gm(screen, bg)
            e_p = levelinit.level_create(screen, hero, mn)
            hero.rect.x = 384
            hero.rect.y = 352
            mn.rect.x = 448
            mn.rect.y = 352
            lifes = 3
            level = 1
            score = 0

        if score % 25000 == 0 and score != 0:
            e_p = levelinit.level_create(screen, hero, mn)
            hero.rect.x = 384
            hero.rect.y = 352
            mn.rect.x = 448
            mn.rect.y = 352
            level += 1

        e_p[1].draw(screen)
        e_p[3].draw(screen)

        display.update()  # обновление и вывод всех изменений на экран
