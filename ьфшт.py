import json

import random



import pygame as pg



# Инициализация pg

pg.init()



# Размеры окна

SCREEN_WIDTH = 900

SCREEN_HEIGHT = 550



BUTTON_WIDTH = 200

BUTTON_HEIGHT = 60



DOG_WIDTH = 250

DOG_HEIGHT = 300



ICON_SIZE = 100



TOY_SIZE = 100



font = pg.font.Font(None, 38)

mini_font = pg.font.Font(None, 12)





def text_render(text, font_r=font):

    return font_r.render(str(text), True, 'black')





def load_image(image, width, height):

    file = pg.image.load(image)

    file = pg.transform.scale(file, (width, height))

    return file




class GameOver:
    def __init__(self,game):
        self.game = game
    def draw(self):
        lose_font = pg.font.Font(None, 142)
        self.game.screen.blit(lose_font.render("Вы проиграли!", True, "red"),(SCREEN_WIDTH//2-350, SCREEN_HEIGHT//2-75))


class Item:

    def __init__(self, name, price, file, is_using=False, is_bought=False, satiety=0, health=0):

        self.name = name

        self.price = price

        self.is_bought = is_bought

        self.is_using = is_using

        self.satiety = satiety

        self.health = health



        self.image = load_image(file, DOG_WIDTH // 2, DOG_HEIGHT // 2)

        self.full_image = load_image(file, DOG_WIDTH, DOG_HEIGHT)





class Toy:

    def __init__(self):

        self.image = load_image("images/toys/blue bone.png", TOY_SIZE, TOY_SIZE)

        self.rect = self.image.get_rect()

        self.rect.x = random.randint(125, 700)

        self.rect.y = SCREEN_HEIGHT // 2 - 340



    def draw(self, screen):

        screen.blit(self.image, self.rect)



    def update(self):

        self.rect.y += 2





class Dog:

    def __init__(self):

        self.image = load_image('images/dog.png', DOG_WIDTH / 2, DOG_HEIGHT / 2)

        self.rect = self.image.get_rect()

        self.rect.x = SCREEN_WIDTH // 2 - 100

        self.rect.y = SCREEN_HEIGHT // 2 + 50



    def draw(self, screen):

        screen.blit(self.image, self.rect)



    def update(self):

        keys = pg.key.get_pressed()

        if self.rect.x > 115:

            if keys[pg.K_a]:

                self.rect.x -= 3

        if self.rect.x < 640:

            if keys[pg.K_d]:

                self.rect.x += 3





class MiniGame:

    def __init__(self, game):

        self.game = game



        self.background = load_image("images/game_background.png", SCREEN_WIDTH, SCREEN_HEIGHT)



        self.dog = Dog()

        self.toys = []



        self.score = 0



        self.start_time = pg.time.get_ticks()

        self.interval = 1000 * 10



    def new_game(self):

        self.dog = Dog()

        self.toys = []



        self.score = 0



        self.start_time = pg.time.get_ticks()

        self.interval = 1000 * 10



    def draw(self, screen):

        screen.blit(self.background, (0, 0))

        screen.blit(self.dog.image, self.dog.rect)

        for i in self.toys:

            i.draw(screen)

        screen.blit(text_render(self.score), (115, 90))

        # self.toys.draw()



    def update(self):

        if self.start_time + self.interval < pg.time.get_ticks():

            if self.game.happiness + self.score > 100:

                self.game.happiness = 100

            else:

                self.game.happiness += self.score

            self.game.mode = "Main"

            self.new_game()

            return True

        self.dog.update()

        chance = random.randint(1, 100)

        if chance == 3:

            self.toys.append(Toy())

        for i in self.toys:

            if self.dog.rect.colliderect(i.rect):

                self.toys.remove(i)

                self.score += 1

            i.update()





class ClothesMenu:

    def __init__(self, game, data):

        self.menu_page = load_image("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_on = load_image("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.top_label_off = load_image("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.top_label_on = load_image("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)



        self.game = game



        self.items = []

        self.data = data

        for item in data:

            self.items.append(Item(*item.values()))



        self.current_item = 0



        self.item_rect = self.items[0].image.get_rect()

        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)



        self.next_button = Button("Вперед", 600, 400,

                                  width=int(BUTTON_WIDTH // 1.2),

                                  height=int(BUTTON_HEIGHT // 1.2),

                                  func=self.to_next)



        self.prev_button = Button("Назад", 125, 400,

                                  width=int(BUTTON_WIDTH // 1.2),

                                  height=int(BUTTON_HEIGHT // 1.2),

                                  func=self.to_prev)



        self.use_button = Button("Надеть", 125, 325,

                                 width=int(BUTTON_WIDTH // 1.2),

                                 height=int(BUTTON_HEIGHT // 1.2),

                                 func=self.use)



        self.buy_button = Button("Купить", 370, 350,

                                 width=int(BUTTON_WIDTH // 1.5),

                                 height=int(BUTTON_HEIGHT // 1.5),

                                 func=self.buy)

        self.menu_buttons = [self.use_button, self.buy_button, self.prev_button, self.next_button]



    def to_next(self):

        if self.current_item != len(self.items) - 1:

            self.current_item += 1

        else:

            self.current_item = 0



    def buy(self):

        if self.game.mode == "Clothes menu":

            if self.game.money >= self.items[self.current_item].price:

                self.game.money -= self.items[self.current_item].price

                self.items[self.current_item].is_bought = True

                self.data[self.current_item]['is_bought'] = True





    def use(self):

        if self.game.mode == "Clothes menu":

            if self.items[self.current_item].is_bought:

                self.items[self.current_item].is_using = True

                self.data[self.current_item]['is_using'] = True



    def to_prev(self):

        if self.game.mode == "Clothes menu":

            if self.current_item != 0:

                self.current_item -= 1

            else:

                self.current_item = len(self.items) - 1



    def update(self):

        for i in self.menu_buttons:

            i.update()



    def is_clicked(self, event):

        for i in self.menu_buttons:

            i.is_clicked(event)



    def draw(self, screen):

        screen.blit(self.menu_page, (0, 0))

        screen.blit(self.items[self.current_item].image, self.item_rect)



        if self.items[self.current_item].is_bought:

            screen.blit(self.bottom_label_on, (0, 0))

        else:

            screen.blit(self.bottom_label_off, (0, 0))

        if self.items[self.current_item].is_using:

            screen.blit(self.top_label_on, (0, 0))

        else:

            screen.blit(self.top_label_off, (0, 0))



        for i in self.menu_buttons:

            i.draw(screen)



        self.game.screen.blit(text_render(self.items[self.current_item].price), (425, 165))

        self.game.screen.blit(text_render("Надето"), (650, 115))

        self.game.screen.blit(text_render("Куплено"), (645, 185))





class FoodMenu:

    def __init__(self, game, data):

        self.menu_page = load_image("images/menu/menu_page.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image("images/menu/bottom_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_on = load_image("images/menu/bottom_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.top_label_off = load_image("images/menu/top_label_off.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.top_label_on = load_image("images/menu/top_label_on.png", SCREEN_WIDTH, SCREEN_HEIGHT)



        self.game = game



        self.items = []

        for item in data:

            val = list(item.values())

            self.items.append(Item(val[0], val[1], val[2], satiety=val[3], health=val[4]))





        self.current_item = 0



        self.item_rect = self.items[0].image.get_rect()

        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)



        self.next_button = Button("Вперед", 600, 400,

                                  width=int(BUTTON_WIDTH // 1.2),

                                  height=int(BUTTON_HEIGHT // 1.2),

                                  func=self.to_next)



        self.prev_button = Button("Назад", 125, 400,

                                  width=int(BUTTON_WIDTH // 1.2),

                                  height=int(BUTTON_HEIGHT // 1.2),

                                  func=self.to_prev)



        self.buy_button = Button("Съесть", 370, 350,

                                 width=int(BUTTON_WIDTH // 1.5),

                                 height=int(BUTTON_HEIGHT // 1.5),

                                 func=self.buy)

        self.menu_buttons = [self.buy_button, self.prev_button, self.next_button]



    def to_next(self):

        if self.game.mode == "Food menu":

            if self.current_item != len(self.items) - 1:

                self.current_item += 1

            else:

                self.current_item = 0



    def buy(self):

        if self.game.mode == "Food menu":

            if self.game.money >= self.items[self.current_item].price:

                self.game.money -= self.items[self.current_item].price

            if self.game.satiety + self.items[self.current_item].satiety > 100:

                self.game.satiety = 100

            else:

                self.game.satiety += self.items[self.current_item].satiety

            if self.game.health + self.items[self.current_item].health > 100:

                self.game.health = 100

            else:

                self.game.health += self.items[self.current_item].health



    def to_prev(self):

        if self.game.mode == "Food menu":

            if self.current_item != 0:

                self.current_item -= 1

            else:

                self.current_item = len(self.items) - 1



    def update(self):

        for i in self.menu_buttons:

            i.update()



    def is_clicked(self, event):

        for i in self.menu_buttons:

            i.is_clicked(event)



    def draw(self, screen):

        screen.blit(self.menu_page, (0, 0))

        screen.blit(self.items[self.current_item].image, self.item_rect)



        for i in self.menu_buttons:

            i.draw(screen)



        self.game.screen.blit(text_render(self.items[self.current_item].price), (425, 165))





class Button:

    def __init__(self, text, x, y, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, text_font=font, func=None):

        self.idle_image = load_image("images/button.png", width, height)

        self.pressed_image = load_image("images/button_clicked.png", width, height)

        self.image = self.idle_image

        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)



        self.is_pressed = False

        self.text = text_render(text, text_font)

        self.text_rect = self.text.get_rect()

        self.text_rect.center = self.rect.center

        self.func = func



    def draw(self, screen):

        screen.blit(self.image, self.rect)

        screen.blit(self.text, self.text_rect)



    def update(self):

        mouse_pos = pg.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):

            if self.is_pressed:

                self.image = self.pressed_image

            else:

                self.image = self.idle_image



    def is_clicked(self, event):

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:

            if self.rect.collidepoint(event.pos):

                self.is_pressed = True

                self.func()



        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:

            self.is_pressed = False





class Game:

    def __init__(self):



        # Создание окна

        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        pg.display.set_caption("Виртуальный питомец")



        self.bg = load_image('images/background.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.happiness_image = load_image('images/happiness.png', ICON_SIZE, ICON_SIZE)

        self.satiety_image = load_image('images/satiety.png', ICON_SIZE, ICON_SIZE)

        self.health_image = load_image('images/health.png', ICON_SIZE, ICON_SIZE)

        self.money_image = load_image('images/money.png', ICON_SIZE, ICON_SIZE)

        self.dog_image = load_image('images/dog.png', DOG_WIDTH, DOG_HEIGHT)



        self.INCREASE_COINS = pg.USEREVENT + 1

        pg.time.set_timer(self.INCREASE_COINS, 3000)

        self.DECREASE = pg.USEREVENT + 2

        pg.time.set_timer(self.DECREASE, 1000)

        self.mode = "Main"

        with open('save.json', encoding="utf-8") as file:

            self.data = json.load(file)

        self.happiness = self.data['happiness']

        self.satiety = self.data['satiety']

        self.health = self.data['health']

        self.money = self.data['money']



        self.coins_per_second = self.data['coins_per_second']

        self.costs_of_upgrade = {}

        for key, value in self.data['costs_of_upgrade'].items():

            self.costs_of_upgrade[int(key)] = value



        button_x = SCREEN_WIDTH - BUTTON_WIDTH - 10

        self.eat_button = Button("Еда", button_x, 100, func=self.food_menu_on)

        self.clothes_button = Button("Одежда", button_x, 110 + BUTTON_HEIGHT, func=self.clothes_menu_on)

        self.game_button = Button("Игры", button_x, 120 + BUTTON_HEIGHT * 2, func=self.mini_game_on)



        self.upgrade_button = Button("Учучшить", 0, 0, BUTTON_WIDTH // 3, BUTTON_HEIGHT // 3, mini_font, self.inc_coins)



        self.buttons = [self.game_button, self.clothes_button, self.eat_button, self.upgrade_button]



        self.clothes_menu = ClothesMenu(self, self.data['clothes'])



        self.food_menu = FoodMenu(self, self.data['foods'])

        self.gameover = GameOver(self)

        self.mini_game = MiniGame(self)



        self.run()



    def inc_coins(self):

        for cost, check in self.costs_of_upgrade.items():

            if not check and self.money >= cost:

                self.coins_per_second += 1

                self.money -= cost

                self.costs_of_upgrade[cost] = True

                break



    def clothes_menu_on(self):

        self.mode = "Clothes menu"



    def food_menu_on(self):

        self.mode = "Food menu"



    def mini_game_on(self):

        self.mode = "Mini game"

        self.mini_game.start_time = pg.time.get_ticks()



    def run(self):

        while True:

            self.event()

            self.update()

            self.draw()



    def event(self):

        for event in pg.event.get():

            if event.type == pg.QUIT:

                self.data['money'] = self.money

                self.data['happiness'] = self.happiness

                self.data['satiety'] = self.satiety

                self.data['health'] = self.health

                print(self.data)

                with open("save.json", "w") as file:

                    json.dump(self.data, file)

                pg.quit()

                exit()


            if event.type == pg.KEYDOWN:

                if self.mode == "GO":
                    self.data["money"] = 0
                    self.data["happiness"] = 100
                    self.data["satiety"] = 100
                    self.data["health"] = 100
                    for i in range(len(self.data["clothes"])):
                        self.data["clothes"][i]["is_bought"] = False
                        self.data["clothes"][i]["is_using"] = False

                    self.data["costs_of_upgrade"]["100"] = False
                    self.data["costs_of_upgrade"]["1000"] = False
                    self.data["costs_of_upgrade"]["5000"] = False
                    self.data["costs_of_upgrade"]["10000"] = False
                    with open("save.json", "w") as file:
                        json.dump(self.data,file)
                    pg.quit()
                    exit()

                if event.key == pg.K_ESCAPE:

                    self.mode = "Main"



            if event.type == self.INCREASE_COINS:

                self.money += self.coins_per_second



            if event.type == self.DECREASE:

                num = random.randint(1, 10)

                if num <= 5:

                    self.satiety -= 1

                elif 5 < num <= 9:

                    self.happiness -= 1

                else:

                    self.health -= 1





            for i in self.buttons:

                i.is_clicked(event)

            self.clothes_menu.is_clicked(event)

            self.food_menu.is_clicked(event)

        if self.health <=0 or self.happiness <=0 or self.satiety <=0:
            self.mode = "GO"




    def update(self):

        for i in self.buttons:

            i.update()

        self.clothes_menu.update()

        self.food_menu.update()

        if self.mode == "Mini game":

            self.mini_game.update()



    def draw(self):

        self.screen.blit(self.bg, (0, 0))

        self.screen.blit(self.happiness_image, (0, 0))

        self.screen.blit(self.satiety_image, (0, 95))

        self.screen.blit(self.health_image, (0, 190))

        self.screen.blit(self.money_image, (SCREEN_WIDTH - 100, 0))

        self.screen.blit(self.dog_image, (250, 175))



        self.screen.blit(text_render(self.happiness), (90, 40))

        self.screen.blit(text_render(self.satiety), (90, 135))

        self.screen.blit(text_render(self.health), (90, 230))

        self.screen.blit(text_render(self.money), (SCREEN_WIDTH - 150, 40))



        for i in self.buttons:

            i.draw(self.screen)



        if self.mode == "Clothes menu":

            self.clothes_menu.draw(self.screen)



        if self.mode == "Food menu":

            self.food_menu.draw(self.screen)



        if self.mode == "Mini game":

            self.mini_game.draw(self.screen)

        if self.mode == "GO":
            self.gameover.draw()



        pg.display.flip()





if __name__ == "__main__":

    Game()

