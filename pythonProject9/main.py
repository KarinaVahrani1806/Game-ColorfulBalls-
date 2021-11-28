from superwires import games
from random import randint

games.init(screen_width=650, screen_height=550, fps=50)
wall_image = games.load_image("background.jpg", transparent=False)
games.screen.background = wall_image

bask_image = games.load_image("basketr.png")



class Basket(games.Sprite):
    def __init__(self, x, type_name):
        self.type_name = type_name
        super(Basket, self).__init__(image=bask_image, x=x, y=460)

    # обработать клик
    def handle_click(self):
        if len(builder.visible_balls) > 0:
            lowest_balls = builder.visible_balls[0]
            if lowest_balls.type_name == self.type_name:
                builder.visible_balls.remove(lowest_balls)
                games.screen.remove(lowest_balls)

    def update(self):
        # вытягиват пересекающие спрайты
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

        super(BallsBuilderSprite, self).__init__(image=bask_image, x=-400, y=-400)


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
        # уменшения интервала - сколько кадров пройдет между
        # появлением шариков
        if self.created_balls == 20:
            self.frames_interval = 45
        elif self.created_balls == 40:
            self.frames_interval = 30
        elif self.created_balls == 60:
            self.frames_interval = 20

        # обработка клика мыши, 0 значит левая кнопка
        if games.mouse.is_pressed(0):
            # не в режиме удаления
            if self.in_removal_mode is False:
                self.in_removal_mode = True
                # клик еще не обработан
                self.click_was_handled = False
        # кнопку отпустили - выходим из режима удаления
        elif self.click_was_handled:
            self.in_removal_mode = False

        # в режиме удаления и еще не обработали клик
        if self.in_removal_mode and self.click_was_handled is False:
            if check_point(games.mouse.x, games.mouse.y, bask_red):
                bask_red.handle_click()
            elif check_point(games.mouse.x, games.mouse.y, bask_green):
                bask_green.handle_click()
            elif check_point(games.mouse.x, games.mouse.y, bask_yellow):
                bask_yellow.handle_click()

            self.click_was_handled = True

# создали 3 спрайта
bask_red = Basket(x=106, type_name="red")
bask_green = Basket(x=313, type_name="green")
bask_yellow = Basket(x=521, type_name="yellow")

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
    return ColorfulBalls(image=games.load_image("redball_1.png"), type_name="red")


def green_balls():
    return ColorfulBalls(image=games.load_image("greenball-removebg-preview.png"), type_name="green")


def yellow_balls():
    return ColorfulBalls(image=games.load_image("yellowball-removebg-preview.png"), type_name="yellow")


games.screen.add(bask_red)
games.screen.add(bask_green)
games.screen.add(bask_yellow)
games.screen.add(builder)

games.screen.mainloop()



