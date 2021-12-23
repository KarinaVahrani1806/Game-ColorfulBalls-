from superwires import games
from random import randint
import pygame
import sys

pygame.init()

window = pygame.display.set_mode((600,550))
pygame.display.set_caption("ColorfullBalls")
screen = pygame.display.set_mode((600,550))


class Menu:
    def __init__(self,punkts = [120, 140, u'Punkt', (250,250,30) ,(250,30,250)]):
        self.punkts = punkts
    def render(self,poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4],),(i[0], i[1]))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3], ), (i[0], i[1]))
    def menu(self):
        done = True
        font_menu = pygame.font.Font('freesansbold.ttf', 50)
        punkt = 0
        while done:
            screen.fill((176, 196, 222))

            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0]> i[0] and mp[0]<i[0]+155 and mp[1]>i[1] and mp[1]<i[1]+50:
                    punkt = i[5]
            self.render(screen, font_menu, punkt)


            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts)-1:
                            punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        sys.exit()
            window.blit(screen,(0,0))
            pygame.display.flip()


punkts = [(169,140, u'Почати гру', (0, 0, 205), (0, 0, 205), 0),
          (220,215, u'Вийти', (0, 0, 205), (0, 0, 205), 0)]
game = Menu(punkts)
game.menu()

games.init(screen_width=600, screen_height=550, fps=50)
wall_image = games.load_image("background.jpg", transparent=False)
games.screen.background = wall_image

bask_image1 = games.load_image("redbask.png")
bask_image2 = games.load_image("greenbask.png")
bask_image3 = games.load_image("yellowbask.png")

class BasketRed(games.Sprite):
    def __init__(self, x, type_name,):
        self.type_name = type_name
        super(BasketRed, self).__init__(image=bask_image1, x=x, y=460)

    def handle_click(self):
        if len(builder.visible_balls) > 0:
            lowest_balls = builder.visible_balls[0]
            if lowest_balls.type_name == self.type_name:
                builder.visible_balls.remove(lowest_balls)
                games.screen.remove(lowest_balls)

    def update(self):
        overlapping_sprites = self.get_overlapping_sprites()

        for sprite in overlapping_sprites:
            if sprite.type_name != self.type_name:
                games.screen.quit()


class BasketGreen(games.Sprite):
    def __init__(self, x, type_name):
        self.type_name = type_name

        super(BasketGreen, self).__init__(image=bask_image2, x=x, y=460)

    def handle_click(self):
        if len(builder.visible_balls) > 0:
            lowest_balls = builder.visible_balls[0]
            if lowest_balls.type_name == self.type_name:
                builder.visible_balls.remove(lowest_balls)
                games.screen.remove(lowest_balls)

    def update(self):
        overlapping_sprites = self.get_overlapping_sprites()

        for sprite in overlapping_sprites:
            if sprite.type_name != self.type_name:
                games.screen.quit()



class BasketYellow(games.Sprite):
    def __init__(self, x, type_name):
        self.type_name = type_name
        super(BasketYellow, self).__init__(image=bask_image3, x=x, y=460)

    def handle_click(self):
        if len(builder.visible_balls) > 0:
            lowest_balls = builder.visible_balls[0]
            if lowest_balls.type_name == self.type_name:
                builder.visible_balls.remove(lowest_balls)
                games.screen.remove(lowest_balls)



    def update(self):
        overlapping_sprites = self.get_overlapping_sprites()

        for sprite in overlapping_sprites:
            if sprite.type_name != self.type_name:
                games.screen.quit()




class ColorfulBalls(games.Sprite):
    def __init__(self, image, type_name):
        self.type_name = type_name
        # dy - скорость падения вниз
        super(ColorfulBalls, self).__init__(image=image, x=games.screen.width / 2, y=games.screen.height - 527, dx=0, dy=2)



class BallsBuilderSprite(games.Sprite):
    def __init__(self):
        self.in_removal_mode = False
        self.click_was_handled = False
        # интервал появления мусора
        self.frames_interval = 60
        self.passed_frames = 0
        self.created_balls = 0
        self.visible_balls = []

        super(BallsBuilderSprite, self).__init__(image=bask_image2, x=-400, y=-400)

    def update(self):
        # сколько прошло
        if self.passed_frames == 0:
            # +1 к созданому шарику
            self.created_balls += 1
            # дописать функцию
            new_balls = random_balls()
            self.visible_balls.append(new_balls)
            games.screen.add(new_balls)

        # прошел один кадр
        self.passed_frames += 1

        if self.passed_frames == self.frames_interval:
            self.passed_frames = 0

            if self.created_balls == 20:
                self.frames_interval = 45
            elif self.created_balls == 40:
                self.frames_interval = 30
            elif self.created_balls == 60:
                self.frames_interval = 20

        if games.mouse.is_pressed(0):
            # не в режиме удаления
            if self.in_removal_mode is False:
                self.in_removal_mode = True
                # клик еще не обработан
                self.click_was_handled = False
        # кнопку отпустили - выходим из режима удаления
        elif self.click_was_handled:
            self.in_removal_mode = False

        if self.in_removal_mode and self.click_was_handled is False:
            if check_point(games.mouse.x, games.mouse.y, bask_red):
                bask_red.handle_click()
            elif check_point(games.mouse.x, games.mouse.y, bask_green):
                bask_green.handle_click()
            elif check_point(games.mouse.x, games.mouse.y, bask_yellow):
                bask_yellow.handle_click()

            self.click_was_handled = True




bask_red = BasketRed(x=106, type_name="red")
bask_green = BasketGreen(x=313, type_name="green")
bask_yellow = BasketYellow(x=521, type_name="yellow")


builder = BallsBuilderSprite()

def check_point(x, y, sprite):
    return sprite.left <= x <= sprite.right and sprite.top <= y <= sprite.bottom

def random_balls():
    value = randint(1, 3)

    if value == 1:
        return red_balls()
    elif value == 2:
        return green_balls()
    else:
        return yellow_balls()

def red_balls():
    return ColorfulBalls(image=games.load_image("pixil-frame-0 (1).png"), type_name="red")


def green_balls():
    return ColorfulBalls(image=games.load_image("pixil-frame-0 (2).png"), type_name="green")


def yellow_balls():
    return ColorfulBalls(image=games.load_image("pixil-frame-0 (3).png"), type_name="yellow")





games.screen.add(bask_red)
games.screen.add(bask_green)
games.screen.add(bask_yellow)
games.screen.add(builder)

games.screen.mainloop()
