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
        self.wireless_controlled = False
        self.direction = "1 0"
        self.inputs = "keyboard"

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

    def rp(self, pos=None):
        if pos is None:
            return self.pos + self.im_pos - self.infos["centre"] + self.infos["screen_center"]
        return pos - self.infos["centre"] + self.infos["screen_center"]

    def draw(self):
        rp = self.rp()
        if self.anims is None:
            pg.draw.rect(self.infos["screen"], (100, 100, 100), pg.Rect(*rp.get(), *self.size.get()))
        else:
            image = self.animation_change()
            self.infos["screen"].blit(image, rp.get())

    def secondary_draw(self):
        pass

    def collision(self):
        self.on_ground = False
        collisions = []
        for elt in self.collisions:
            if type(elt[0]) not in (Sender, Player) and not (type(elt[0]) == Door and not elt[0].activ):
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
        elif self.anims[self.anim][anim_timer] == "pause":
            self.anim_timer -= 1
            image = self.anims[self.anim][self.anim_timer]
        elif type(self.anims[self.anim][anim_timer]) == str:
            self.anim = self.anims[self.anim][anim_timer]
            image = self.anims[self.anim][0]
            self.anim_timer = 0
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
    def images(filename, doing_after="reboot", size=None):
        i = 1
        res = []
        end = False
        while not end:
            f = os.path.dirname(__file__)+"\\"+"images\\"+filename+"_"+str(i)+".png"
            if os.path.exists(f):
                if size is not None:
                    im = pg.transform.scale(pg.image.load(f), size.get())
                else:
                    im = pg.image.load(f)
                res.append(im)
            else: end = True
            i += 1
        res.append(doing_after)
        return res


class Checkpoint(Object):
    def __init__(self, infos, pos, end_lvl=False):
        Object.__init__(self, infos)
        self.pos = pos
        self.size = Vec(50, 50)
        self.controllable = True
        self.proximity = 1
        self.end_lvl = end_lvl
        self.anims = {"stand": self.images("finisher")}

    def update(self):
        if self.controlled:
            return "new_checkpoint"


class Door(Object):
    def __init__(self, infos, pos, activated_by=0):
        Object.__init__(self, infos)
        self.pos = pos
        self.size = Vec(50, 50)
        self.activ = False
        self.font = pg.font.Font(None, 30)
        self.activated_by = activated_by
        self.anims = {"stand": self.images("door"),
                      "opening": self.images("door_open", "open"),
                      "open": self.images("open")}

    def update(self):
        if self.activ and self.anim[:4] != "open":
            self.anim = "opening"
        elif not self.activ:
            self.anim = "stand"

    def draw(self):
        rp = self.rp()
        image = self.animation_change()
        self.infos["screen"].blit(image, rp.get())
        im = self.font.render(str(self.activated_by), True, (0, 0, 0))
        self.infos["screen"].blit(im, (rp+self.size/2-Vec(10, 10)).get())


class Button(Object):
    def __init__(self, infos, pos, to_activate):
        Object.__init__(self, infos)
        self.pos = pos
        self.controllable = True
        self.font = pg.font.Font(None, 30)
        self.size = Vec(50, 50)
        self.anims = {"stand": self.images("button"),
                      "activated": self.images("button_activated")}
        self.to_activate = to_activate

    def update(self):
        if self.controlled:
            keys = self.infos["inputs"][self.inputs].keys
            self.to_activate.activ = True
            self.anim = "activated"
            if keys["right"]:
                self.direction = "1 0"
            elif keys["left"]:
                self.direction = "-1 0"
            elif keys["up"]:
                self.direction = "0 -1"
            elif keys["down"]:
                self.direction = "0 1"
            if keys["space"]:
                self.controlled = False
                self.speed.x(0)
                return "sender " + self.direction

    def draw(self):
        rp = self.rp()
        image = self.animation_change()
        self.infos["screen"].blit(image, rp.get())
        im = self.font.render(str(self.to_activate.activated_by), True, (0, 0, 0))
        self.infos["screen"].blit(im, (rp + self.size / 2-Vec(10, 10)).get())


class ActivatorByPos(Object):
    def __init__(self, infos, pos, size, to_activate):
        Object.__init__(self, infos)
        self.act_pos = pos
        self.act_size = size
        self.to_activate = to_activate
        self.font = pg.font.Font(None, 30)

    def update(self):
        self.to_activate.activ = False
        for elt in self.infos["objects"]:
            if elt.size == self.act_size and dist(elt.pos, self.act_pos) < 30:
                self.to_activate.activ = True
                break

    def draw(self):
        pass

    def secondary_draw(self):
        rp = self.rp(self.act_pos)
        pg.draw.rect(self.infos["screen"], (200, 0, 255), pg.Rect(*(rp+Vec(10, 10)).get(),
                                                                  *(self.act_size-Vec(20, 20)).get()))
        im = self.font.render(str(self.to_activate.activated_by), True, (0, 0, 0))
        self.infos["screen"].blit(im, (rp+self.size/2+Vec(10, 10)).get())


class PlatformVertical(Object):
    def __init__(self, infos, pos, size=Vec(50, 50), max_up=None, max_down=None):
        Object.__init__(self, infos)
        self.pos = pos
        self.size = size
        self.inputs = "keyboard"
        self.controllable = True
        self.anims = {"stand": self.images("vertical", size=self.size)}
        self.max_up = max_up
        self.max_down = max_down

    def update(self):
        keys = self.infos["inputs"][self.inputs].keys
        if self.controlled or self.wireless_controlled:
            self.speed = Vec(0, 0)
            if keys["up"] and (self.max_up is None or self.max_up < self.pos.y()):
                self.speed = Vec(0, -5)
                self.pos += Vec(0, -10)
            if keys["down"] and (self.max_down is None or self.max_down > self.pos.y()):
                self.speed = Vec(0, 5)
                self.pos += Vec(0, 10)
        if self.controlled:
            if keys["right"]:
                self.direction = "1 0"
            elif keys["left"]:
                self.direction = "-1 0"
            elif keys["up"]:
                self.direction = "0 -1"
            elif keys["down"]:
                self.direction = "0 1"
            if keys["space"]:
                self.controlled = False
                self.speed.x(0)
                return "sender " + self.direction

    def secondary_draw(self):
        if self.controlled or self.wireless_controlled:
            m = self.pos.copy()
            m.y(self.max_up)
            M = self.pos+self.size
            M.y(self.max_down+self.size.y())
            rp = self.rp(m)
            pg.draw.rect(self.infos["screen"], (0, 255, 100), pg.Rect(*rp.get(), *(M-m).get()))


class Mirror(Object):
    def __init__(self, infos, pos, in_dir, out_dir):
        Object.__init__(self, infos)
        self.pos = pos
        self.size = Vec(50, 50)
        self.in_dir = in_dir
        self.out_dir = out_dir
        if in_dir == Vec(0, -1) and out_dir == Vec(1, 0):
            self.anims = {"stand": self.images("mirroir_bd")}
        if in_dir == Vec(0, -1) and out_dir == Vec(-1, 0):
            self.anims = {"stand": self.images("mirroir_bg")}


class Observer(Object):
    def __init__(self, infos, pos, size=Vec(50, 50)):
        Object.__init__(self, infos)
        self.pos = pos
        self.size = size
        self.controllable = True
        self.inputs = "keyboard"
        self.anims = {"stand": self.images("observer", size=self.size)}

    def update(self):
        if self.controlled:
            keys = self.infos["inputs"][self.inputs].keys
            if keys["right"]:
                self.direction = "1 0"
            elif keys["left"]:
                self.direction = "-1 0"
            elif keys["up"]:
                self.direction = "0 -1"
            elif keys["down"]:
                self.direction = "0 1"
            if keys["space"]:
                self.speed.x(0)
                self.controlled = False
                return "sender " + self.direction


class PlatformHorizontal(Object):
    def __init__(self, infos, pos, size=Vec(50, 50), max_right=None, max_left=None, only_wireless=-1):
        Object.__init__(self, infos)
        self.pos = pos
        self.size = size
        self.inputs = "keyboard"
        self.only_wireless = only_wireless
        if only_wireless < 0:
            self.controllable = True
        self.max_right = max_right
        self.font = pg.font.Font(None, 40)
        self.max_left = max_left
        self.anims = {"stand": self.images("horizontal", size=self.size)}

    def draw(self):
        rp = self.rp()
        image = self.animation_change()
        self.infos["screen"].blit(image, rp.get())
        if self.only_wireless >= 0:
            im = self.font.render(str(self.only_wireless), True, (255, 255, 255))
            self.infos["screen"].blit(im, (rp + self.size / 2 - Vec(10, 10)).get())


    def secondary_draw(self):
        if self.controlled or self.wireless_controlled:
            m = self.pos.copy()
            m.x(self.max_left)
            M = self.pos+self.size
            M.x(self.max_right+self.size.x())
            rp = self.rp(m)
            pg.draw.rect(self.infos["screen"], (0, 255, 100), pg.Rect(*rp.get(), *(M-m).get()))

    def update(self):
        keys = self.infos["inputs"][self.inputs].keys
        if self.controlled or self.wireless_controlled:
            if keys["right"] and (self.max_right is None or self.pos.x() < self.max_right):
                self.speed = Vec(5, 0)
                self.pos += Vec(10, 0)
            elif keys["left"] and (self.max_left is None or self.pos.x() > self.max_left):
                self.speed = Vec(-5, 0)
                self.pos += Vec(-10, 0)
            else:
                self.speed = Vec(0, 0)
        if self.controlled:
            if keys["right"]:
                self.direction = "1 0"
            elif keys["left"]:
                self.direction = "-1 0"
            elif keys["up"]:
                self.direction = "0 -1"
            elif keys["down"]:
                self.direction = "0 1"
            if keys["space"]:
                self.speed.x(0)
                self.controlled = False
                return "sender " + self.direction


class Lever(Object):
    def __init__(self, infos, pos, control):
        Object.__init__(self, infos)
        self.infos = infos
        self.pos = pos
        self.controllable = True
        self.size = Vec(30, 30)
        self.control = control
        self.anims = {"stand": self.images("lever")}

    def update(self):
        self.control.wireless_controlled = self.controlled
        keys = self.infos["inputs"][self.inputs].keys
        if self.controlled:
            if keys["right"]:
                self.direction = "1 0"
            elif keys["left"]:
                self.direction = "-1 0"
            elif keys["up"]:
                self.direction = "0 -1"
            elif keys["down"]:
                self.direction = "0 1"
            if keys["space"]:
                self.speed.x(0)
                self.controlled = False
                return "sender " + self.direction


class Sender(Object):
    def __init__(self, infos, pos, direction, sender):
        Object.__init__(self, infos)
        self.pos = pos
        self.size = Vec(30, 30)
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
        self.pos += self.dir * 20
        self.timer += 1
        if self.timer >= 30:
            self.delete = True
            self.sender.controlled = True

    def collision(self):
        for elt in self.collisions:
            if elt[0].controllable and elt[0] != self.sender:
                elt[0].controlled = True
                self.sender.controlled = False
                self.delete = True
                break
            elif type(elt[0]) == Mirror:
                if self.dir == elt[0].in_dir:
                    self.pos = elt[0].pos+elt[0].size/2-self.size/2
                    self.dir = elt[0].out_dir
                    self.timer = max(0, self.timer - 10)
                    if self.dir == Vec(1, 0):
                        self.anims = {"stand": self.images("sender_right")}
                    elif self.dir == Vec(-1, 0):
                        self.anims = {"stand": self.images("sender_left")}
                    elif self.dir == Vec(0, 1):
                        self.anims = {"stand": self.images("sender_down")}
                    else:
                        self.anims = {"stand": self.images("sender_up")}
                elif self.dir == -elt[0].out_dir:
                    self.pos = elt[0].pos+elt[0].size/2-self.size/2
                    self.dir = -elt[0].in_dir
                    self.timer = max(0, self.timer - 10)
                    if self.dir == Vec(1, 0):
                        self.anims = {"stand": self.images("sender_right")}
                    elif self.dir == Vec(-1, 0):
                        self.anims = {"stand": self.images("sender_left")}
                    elif self.dir == Vec(0, 1):
                        self.anims = {"stand": self.images("sender_down")}
                    else:
                        self.anims = {"stand": self.images("sender_up")}
            elif elt[0] != self.sender and not (type(elt[0]) == Door and elt[0].activ):
                self.delete = True
                self.sender.controlled = True


class Player(Object):
    def __init__(self, infos, pos):
        Object.__init__(self, infos)
        self.pos = pos
        self.proximity = 1
        self.size = Vec(40, 40)
        self.im_pos = Vec(0, 0)
        self.speed = Vec(0, 0)
        self.collisions = []
        self.inputs = "keyboard"
        self.on_ground = False
        self.jump = False
        self.activ = False
        self.bonus_jump = True
        self.controllable = True
        self.anim_rithm = 3
        self.anim = "stand_right"
        self.anims = {"stand_right": self.images("stand_right"),
                      "stand_left": self.images("stand_left"),
                      "walk_right": self.images("walk_right"),
                      "walk_left": self.images("walk_left"),
                      "jump_right": self.images("jump_right"),
                      "jump_left": self.images("jump_left"),
                      "fall_right": self.images("fall_right"),
                      "fall_left": self.images("fall_left")}

    def update(self):
        keys = self.infos["inputs"][self.inputs].keys
        if self.controlled or self.wireless_controlled:
            self.activ = True
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
                    if self.anim_dir() == -1:
                        self.anim = "stand_left"
                    else:
                        self.anim = "stand_right"
            elif not keys["right"] and self.speed.x() > 0:
                acceleration += Vec(-0.7, 0)
            elif not keys["left"] and self.speed.x() < 0:
                acceleration += Vec(0.7, 0)
            if self.on_ground:
                self.bonus_jump = False
            if keys["up"] and (self.on_ground or self.bonus_jump):
                self.bonus_jump = False
                self.speed.y(-15)
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
        if self.controlled:
            if keys["right"]:
                self.direction = "1 0"
            elif keys["left"]:
                self.direction = "-1 0"
            elif keys["up"]:
                self.direction = "0 -1"
            elif keys["down"]:
                self.direction = "0 1"
            if keys["space"]:
                self.speed.x(0)
                self.controlled = False
                return "sender "+self.direction
            if (self.pos.x() < 6000 and self.pos.y() > 100) or (self.pos.x() < 8000 and self.pos.y() > 200) or \
                    (self.pos.x() < 9000 and self.pos.y() > 1100) or (self.pos.x() < 13800 and self.pos.y() > 600) or \
                    (self.pos.x() > 13800 and self.pos.y() > 1100):
                return "reset"
            if self.anim[:4] == "fall": self.anim_rithm = 5
            else: self.anim_rithm = 3
        else:
            if self.anim_dir() == -1:
                self.anim = "stand_left"
            else:
                self.anim = "stand_right"
            if not self.on_ground and self.speed.y() < 13 and self.activ:
                self.speed += Vec(0, 1.5)
            self.pos += self.speed

    @staticmethod
    def set_music(file):
        pg.mixer.Channel(2).play(pg.mixer.Sound("musics/" + str(file)))

    def collision(self):
        self.on_ground = False
        collisions = []
        for elt in self.collisions:
            if type(elt[0]) not in (Sender,) and not (type(elt[0]) == Door and elt[0].activ):
                if elt[1].x() == 0 and int(elt[1].y() < 0) == int(self.speed.y() > 0):
                    self.speed.y(0)
                    if elt[0].controlled:
                        self.pos += elt[0].speed*2
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
                     "up": False, "down": False, "dash": False, "reset": False, "escape": False, "resized": False}

    def update(self):
        self.keys["end_turn"] = False
        self.keys["reset"] = False
        self.keys["space"] = False
        self.keys["escape"] = False
        self.keys["resized"] = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.keys["end"] = True
            elif event.type == pg.WINDOWRESIZED:
                self.keys["resized"] = True
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
                elif event.key == pg.K_ESCAPE:
                    self.keys["escape"] = True
