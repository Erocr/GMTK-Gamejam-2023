import pygame as pg
from math_assets import *
import os


class Effect:
    def __init__(self, sort, strength=1, duration=1):
        self.sort = sort
        self.strength = strength
        self.duration = duration

    def act(self, receiver, sender):
        if self.sort == "damage":
            receiver.take_damage(self.strength, sender)
        elif self.sort == "knockback":
            receiver.take_vector(self.strength)


class Hitbox:
    def __init__(self, pos, size, follow=None, effects=()):
        self.pos = pos
        self.size = size
        self.effects = effects
        self.follow = follow

    def __and__(self, other):
        x2, y2 = other.pos.get()
        w2, h2 = other.size.get()
        x1, y1 = self.pos.get()
        if self.follow is not None:
            x1 += self.follow.pos.x()
            y1 += self.follow.pos.y()
        w1, h1 = self.size.get()
        return x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2


class Image:
    def __init__(self, infos, pos, image, proximity=0):
        self.pos = pos
        self.image = image
        self.infos = infos
        self.size = Vec(*self.image.get_size())
        self.proximity = proximity

    def rp(self):
        return self.pos - self.infos["centre"] + self.infos["screen_center"]

    def draw(self):
        self.infos["screen"].blit(self.image, self.rp().get())


class Bar:
    def __init__(self, infos, pos, max_size, max_x, color, direction="r"):
        self.pos = pos
        self.infos = infos
        self.max_size = max_size
        self.max_x = max_x
        self.x = max_x
        self.color = color
        self.direction = direction
        self.size = self.max_size

    def set(self, x):
        self.x = x
        self.size = self.max_size
        if self.direction == "r":
            self.size.x(self.x/self.max_x*self.max_size.x())
        if self.direction == "d":
            self.size.y(self.x/self.max_x*self.max_size.y())

    def draw(self):
        color2 = self.color[0]*0.5, self.color[1]*0.5, self.color[2]*0.5
        pg.draw.rect(self.infos["screen"], color2, pg.Rect(*self.pos.get(), *self.size.get()))
        pg.draw.rect(self.infos["screen"], self.color, pg.Rect(*self.pos.get(), *self.size.get()))


class Text:
    def __init__(self, infos, pos, text, size=15, color=(255, 255, 255)):
        self.infos = infos
        self.pos = pos
        self.text = text
        self.font = pg.font.Font(None, size)
        self.color = color

    def set(self, text):
        self.text = text

    def draw(self):
        im = self.font.render(self.text, True, self.color)
        self.infos["screen"].blit(im, self.pos.get())


class TextWithInfo:
    def __init__(self, infos, pos, text_part1, info, text_part2, size=15, color=(255, 255, 255)):
        self.infos = infos
        self.pos = pos
        self.text_part1 = text_part1
        self.info = info
        self.text_part2 = text_part2
        self.font = pg.font.Font(None, size)
        self.color = color

    def set(self, info):
        self.info = info

    def draw(self):
        im = self.font.render(self.text_part1+str(self.info)+self.text_part2, True, self.color)
        self.infos["screen"].blit(im, self.pos.get())


class ImageUI:
    def __init__(self, infos, pos, image):
        self.infos = infos
        self.image = image
        self.pos = pos
        self.visible = True

    def set(self, new_image=None, visible=None):
        if new_image is not None:
            self.image = new_image
        if visible is not None:
            self.visible = visible

    def draw(self):
        if self.visible:
            self.infos["screen"].blit(self.image, self.pos.get())


class Object:
    def __init__(self, infos):
        self.infos = infos
        self.pos = Vec(0, 0)
        self.size = Vec(0, 0)
        self.im_pos = Vec(0, 0)
        self.speed = Vec(0, 0)
        self.anims = None
        self.anim_rithm = 1
        self.prev_anim = "stand"
        self.anim = "stand"
        self.anim_timer = 0
        self.proximity = 0
        self.life = None
        self.hitboxes = ()
        self.effects = ()
        self.controllable = False
        self.delete = False
        self.collisions = []
        self.controlled = False

    def __and__(self, other):
        x1, y1 = self.pos.get()
        w1, h1 = self.size.get()
        if Object in type(other).__bases__:
            x2, y2 = other.pos.get()
            w2, h2 = other.size.get()
            if x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2:
                dirs = (x2 + w2 - x1, x2 - x1 - w1, y2 + h2 - y1, y2 - y1 - h1)  # (right, left, down, up)
                res = min(dirs[0], -dirs[1], dirs[2], -dirs[3])
                if res == dirs[0]:
                    direction = Vec(1, 0)
                elif res == -dirs[1]:
                    direction = Vec(-1, 0)
                elif res == dirs[2]:
                    direction = Vec(0, 1)
                else:
                    direction = Vec(0, -1)
                return direction, res
            return False
        elif type(other) == Vec:
            x2, y2 = other.get()
            if x1 < x2 < x1 + w1 and y1 < y2 < y1 + h1:
                return True
            return False

    def rp(self):
        return self.pos + self.im_pos - self.infos["centre"] + self.infos["screen_center"]

    def draw(self):
        rp = self.rp()
        if self.anims is None:
            pg.draw.rect(self.infos["screen"], (255, 255, 255), pg.Rect(*rp.get(), *self.size.get()), 3)
        else:
            image = self.animation_change()
            self.infos["screen"].blit(image, rp.get())

    def collision(self):
        self.on_ground = False
        collisions = []
        for elt in self.collisions:
            if type(elt[0]) not in ():
                if elt[1].x() == 0 and int(elt[1].y() < 0) == int(self.speed.y() > 0):
                    self.speed.y(0)
                elif elt[1].y() == 0 and int(elt[1].x() < 0) == int(self.speed.x() > 0):
                    self.speed.x(0)
                if (elt[1] == Vec(0, -1) and elt[2] > 0) or (elt[1] == Vec(0, 1) and elt[2] < 0):
                    self.on_ground = True
            move = elt[1] * elt[2]
            for v in collisions:
                if v.x() == move.x() == 0 or v.y() == move.y() == 0:
                    move = Vec(0, 0)
                    break
            collisions.append(move)
            move = Vec(int(move.x() * 0.99), int(move.y() * 0.99))
            self.pos += move

    def update(self):
        pass

    def take_damage(self, damage, sender):
        if self.life is not None:
            self.life -= damage

    @staticmethod
    def set_music(file):
        pg.mixer.Channel(2).play(pg.mixer.Sound("musics/" + str(file)))

    def take_vector(self, vec):
        if self.speed is not None:
            self.speed += vec

    def animation_change(self):
        if self.prev_anim != self.anim: self.anim_timer = 0
        anim_timer = int(self.anim_timer)
        if self.anims[self.anim][anim_timer] == "reboot":
            self.anim_timer = 0
            image = self.anims[self.anim][0]
        elif type(self.anims[self.anim][anim_timer]) == str:
            self.anim = self.anims[self.anim][anim_timer]
            image = self.anims[self.anim][0]
        else: image = self.anims[self.anim][anim_timer]
        if self.prev_anim == self.anim: self.anim_timer += 1/self.anim_rithm
        self.prev_anim = self.anim
        return image

    def anim_dir(self):
        underscore = False
        res = ""
        for i in range(len(self.anim)):
            if underscore:
                res += self.anim[i]
            if self.anim[i] == "_":
                underscore = not underscore
        if res == "left":
            return -1
        elif res == "right":
            return 1
        return 0

    @staticmethod
    def images(filename, doing_after="reboot"):
        i = 1
        res = []
        end = False
        while not end:
            f = os.path.dirname(__file__)+"\\"+"images\\"+filename+"_"+str(i)+".png"
            if os.path.exists(f):
                res.append(pg.image.load(f))
            else: end = True
            i += 1
        res.append(doing_after)
        return res


class PlatformVertical(Object):
    def __init__(self, infos, pos, size=Vec(30, 30)):
        Object.__init__(self, infos)
        self.pos = pos
        self.size = size
        self.inputs = "keyboard"
        self.controllable = True
        self.anims = {"stand": self.images("vertical")}

    def update(self):
        if self.controlled:
            keys = self.infos["inputs"][self.inputs].keys
            if keys["up"]:
                self.pos += Vec(0, -5)
            if keys["down"]:
                self.pos += Vec(0, 5)
            if keys["space"] and keys["right"]:
                self.controlled = False
                return "sender 1 0"
            elif keys["space"] and keys["left"]:
                self.controlled = False
                return "sender -1 0"
            elif keys["space"] and keys["up"]:
                self.controlled = False
                return "sender 0 -1"
            elif keys["space"] and keys["down"]:
                self.controlled = False
                return "sender 0 1"


class Sender(Object):
    def __init__(self, infos, pos, direction, sender):
        Object.__init__(self, infos)
        self.pos = pos
        self.dir = direction
        self.timer = 0
        self.sender = sender
        if direction == Vec(1, 0):
            self.anims = {"stand": self.images("sender_right")}
        elif direction == Vec(-1, 0):
            self.anims = {"stand": self.images("sender_left")}
        elif direction == Vec(0, 1):
            self.anims = {"stand": self.images("sender_down")}
        else:
            self.anims = {"stand": self.images("sender_up")}

    def update(self):
        self.pos += self.dir * 30
        self.timer += 1
        if self.timer >= 20:
            self.delete = True
            self.sender.controlled = True

    def collision(self):
        print(self.collisions)
        for elt in self.collisions:
            if elt[0].controllable and not elt[0].controlled:
                elt[0].controlled = True
                self.sender.controlled = False
                self.delete = True
                break


class Player(Object):
    def __init__(self, infos, pos):
        Object.__init__(self, infos)
        self.pos = pos
        self.controlled = True
        self.proximity = 1
        self.size = Vec(20, 40)
        self.im_pos = Vec(0, 0)
        self.speed = Vec(0, 0)
        self.collisions = []
        self.inputs = "keyboard"
        self.on_ground = False
        self.jump = False
        self.controllable = True
        self.anims = {"stand": self.images("stand"),
                      "walk_right": self.images("walk_right"),
                      "walk_left": self.images("walk_left"),
                      "jump_right": self.images("jump_right"),
                      "jump_left": self.images("jump_left"),
                      "fall_right": self.images("fall_right"),
                      "fall_left": self.images("fall_left")}

    def update(self):
        if self.controlled:
            keys = self.infos["inputs"][self.inputs].keys
            acceleration = Vec(0, 0)
            if keys["right"] and self.speed.x() < 6:
                acceleration += Vec(0.7, 0)
                if self.on_ground:
                    self.anim = "walk_right"
            if keys["left"] and self.speed.x() > -6:
                acceleration += Vec(-0.7, 0)
                if self.on_ground:
                    self.anim = "walk_left"
            if self.speed.x() > 6:
                acceleration += Vec(-1, 0)
            elif self.speed.x() < -6:
                acceleration += Vec(1, 0)
            if not keys["left"] and not keys["right"] and abs(self.speed.x()) <= 1:
                self.speed.x(0)
                if self.on_ground:
                    self.anim = "stand"
            elif not keys["right"] and self.speed.x() > 0:
                acceleration += Vec(-0.7, 0)
            elif not keys["left"] and self.speed.x() < 0:
                acceleration += Vec(0.7, 0)
            if keys["up"] and self.on_ground:
                self.speed += Vec(0, -15)
                self.jump = True
                if self.anim_dir() == -1:
                    self.anim = "jump_left"
                else:
                    self.anim = "jump_right"
            if self.jump and self.speed.y() > 0:
                if self.anim_dir() == -1:
                    self.anim = "fall_left"
                else:
                    self.anim = "fall_right"
                self.jump = False
            if not self.on_ground and self.speed.y() < 13:
                acceleration += Vec(0, 1.5)
            self.speed += acceleration
            self.pos += self.speed
            if keys["space"]:
                self.speed.x(0)
                self.controlled = False
            if keys["space"] and keys["right"]:
                return "sender 1 0"
            elif keys["space"] and keys["left"]:
                return "sender -1 0"
            elif keys["space"] and keys["up"]:
                return "sender 0 -1"
            elif keys["space"] and keys["down"]:
                return "sender 0 1"
        else:
            if not self.on_ground and self.speed.y() < 13:
                self.speed += Vec(0, 1.5)
            self.pos += self.speed

    @staticmethod
    def set_music(file):
        pg.mixer.Channel(2).play(pg.mixer.Sound("musics/" + str(file)))


class Platform(Object):
    def __init__(self, infos, pos, size, image=None):
        Object.__init__(self, infos)
        self.pos = pos
        self.size = size
        self.im_pos = Vec(0, 0)
        self.speed = Vec(0, 0)
        self.collisions = []
        self.inputs = "keyboard"
        self.on_ground = False
        if image is not None:
            self.anims = {"stand": pg.image.load(image)}
        self.proximity = 0


class Keyboard:
    def __init__(self):
        self.keys = {"end": False, "right": False, "left": False, "jump": False, "end_turn": False,
                     "up": False, "down": False, "dash": False, "reset": False}

    def update(self):
        self.keys["end_turn"] = False
        self.keys["reset"] = False
        self.keys["space"] = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.keys["end"] = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    self.keys["right"] = True
                elif event.key == pg.K_LEFT:
                    self.keys["left"] = True
                elif event.key == pg.K_UP:
                    self.keys["up"] = True
                elif event.key == pg.K_DOWN:
                    self.keys["down"] = True
                elif event.key == pg.K_z:
                    self.keys["jump"] = True
                elif event.key == pg.K_SPACE:
                    self.keys["space"] = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_RIGHT:
                    self.keys["right"] = False
                elif event.key == pg.K_LEFT:
                    self.keys["left"] = False
                elif event.key == pg.K_UP:
                    self.keys["up"] = False
                elif event.key == pg.K_DOWN:
                    self.keys["down"] = False
                elif event.key == pg.K_z:
                    self.keys["jump"] = False
                elif event.key == pg.K_e:
                    self.keys["end_turn"] = True
                elif event.key == pg.K_r:
                    self.keys["reset"] = True
