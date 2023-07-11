from objects import *


class Start:
    def __init__(self):
        global infos
        self.screens = images("intro", "start", infos["screen_size"])
        self.anim = 0

    def update(self):
        if infos["inputs"]["keyboard"].keys["space"]:
            self.anim += 1
            if self.screens[self.anim] == "start":
                return Controller()

    def draw(self):
        infos["screen"].blit(self.screens[self.anim], (0, 0))
        pg.display.flip()

    def collisions(self):
        pass

    @staticmethod
    def set_music(file):
        pg.mixer.Channel(0).play(pg.mixer.Sound(os.path.dirname(__file__) + "\\" + "musics\\" + str(file)), -1)


class Controller:
    def __init__(self):
        """ Channel 0 for background music (extradiegetic), channel 1 for ambiance, channel 2 for player's sounds,
            channel 3 for enemies sounds"""
        global infos
        self.tutorial = images("tutorial", size=(Vec(*infos["screen_size"]) - Vec(200, 200)).get())
        self.actual_tutorial = 0
        self.tutorial_to_go = 2
        self.player = None
        self.objects = []
        self.actual_level = 0
        self.checkpoint = None
        self.lvl(True)
        self.UIs = {}
        self.to_do = []
        # self.set_music("bg_music1.mp3")

    def lvl(self, first_use=False):
        if self.actual_level == 0:
            self.objects = [Platform(infos, Vec(100, 0), Vec(700, 50)),
                            Checkpoint(infos, Vec(50, 0)),
                            Platform(infos, Vec(0, -450), Vec(50, 500)),
                            Platform(infos, Vec(0, -500), Vec(800, 50)),
                            PlatformVertical(infos, Vec(250, -50), max_up=-250, max_down=-50),
                            Platform(infos, Vec(300, -200), Vec(50, 200)),
                            Platform(infos, Vec(350, -150), Vec(50, 150)),
                            Platform(infos, Vec(400, -100), Vec(50, 100)),
                            Platform(infos, Vec(450, -50), Vec(50, 50)),
                            PlatformHorizontal(infos, Vec(500, -250), max_right=600, max_left=400),
                            Platform(infos, Vec(700, -300), Vec(100, 350)),
                            Checkpoint(infos, Vec(750, -300)),
                            PlatformHorizontal(infos, Vec(1000, -350), max_left=800, max_right=1150),
                            Platform(infos, Vec(1200, -400), Vec(100, 100)),
                            Checkpoint(infos, Vec(1250, -400)),
                            Platform(infos, Vec(1500, -450), Vec(150, 600)),
                            PlatformVertical(infos, Vec(1550, -550), Vec(50, 100), max_up=-900, max_down=-400),
                            Platform(infos, Vec(1500, -750), Vec(50, 200)),
                            Platform(infos, Vec(1600, -750), Vec(50, 200)),
                            Platform(infos, Vec(1500, -900), Vec(50, 100)),
                            Platform(infos, Vec(1600, -900), Vec(50, 100)),
                            Platform(infos, Vec(1500, -1400), Vec(500, 500)),
                            Platform(infos, Vec(2000, -1400), Vec(50, 150)),
                            PlatformVertical(infos, Vec(1400, -800), Vec(100, 50), max_up=-800, max_down=-450),
                            Checkpoint(infos, Vec(1600, -450)),
                            PlatformVertical(infos, Vec(1650, -450), Vec(100, 50), max_up=-450, max_down=50),
                            Platform(infos, Vec(1650, 100), Vec(500, 50)),
                            Platform(infos, Vec(1750, -400), Vec(50, 400)),
                            Platform(infos, Vec(1800, -350), Vec(50, 350)),
                            Platform(infos, Vec(1850, -300), Vec(50, 300)),
                            PlatformVertical(infos, Vec(1900, 0), Vec(50, 100), max_up=-450, max_down=0),
                            Platform(infos, Vec(1950, -200), Vec(50, 200)),
                            PlatformVertical(infos, Vec(2000, 0), Vec(50, 100), max_up=-1200, max_down=0),
                            Platform(infos, Vec(2050, -200), Vec(50, 200)),
                            Platform(infos, Vec(2100, 0), Vec(50, 100)),
                            Platform(infos, Vec(2150, -200), Vec(150, 350)),
                            Platform(infos, Vec(2050, -1400), Vec(150, 300)),
                            Platform(infos, Vec(2050, -1000), Vec(100, 100)),
                            Platform(infos, Vec(2200, -1400), Vec(100, 500)),
                            Platform(infos, Vec(2300, -1400), Vec(50, 700)),
                            Platform(infos, Vec(2300, -650), Vec(50, 150)),
                            Platform(infos, Vec(2300, -350), Vec(50, 500)),
                            Platform(infos, Vec(2400, -1400), Vec(450, 700)),
                            Platform(infos, Vec(2400, -650), Vec(450, 150)),
                            Platform(infos, Vec(2850, -1400), Vec(450, 1000)),
                            Platform(infos, Vec(2400, -300), Vec(1500, 450)),
                            Platform(infos, Vec(2350, -700), Vec(50, 100)),
                            PlatformVertical(infos, Vec(2350, -450), Vec(50, 100), max_up=-600, max_down=50),
                            PlatformVertical(infos, Vec(2150, -1050), Vec(50, 100), max_up=-1050, max_down=-150),
                            Checkpoint(infos, Vec(3300, -299), True)]
        elif self.actual_level == 1:
            wireless1 = PlatformHorizontal(infos, Vec(5300, -800), size=Vec(100, 50), max_left=5300, max_right=5400)
            wireless2 = PlatformVertical(infos, Vec(10650, -50), Vec(100, 50), max_up=-50, max_down=250)
            door1 = Door(infos, Vec(9250, 700), 1)
            door2 = Door(infos, Vec(10600, -150), 2)
            self.objects = [Platform(infos, Vec(2400, -300), Vec(1500, 450)),
                            Checkpoint(infos, Vec(3300, -299)),
                            Platform(infos, Vec(3400, -350), Vec(100, 50)),
                            Platform(infos, Vec(3500, -400), Vec(100, 100)),
                            Platform(infos, Vec(3600, -450), Vec(100, 150)),
                            Platform(infos, Vec(3700, -500), Vec(100, 200)),
                            Platform(infos, Vec(3800, -550), Vec(100, 250)),
                            Platform(infos, Vec(3900, 50), Vec(200, 50)),
                            PlatformVertical(infos, Vec(4000, 0), Vec(100, 50), max_down=50, max_up=-600),
                            Platform(infos, Vec(4100, -650), Vec(100, 750)),
                            Platform(infos, Vec(4300, -700), Vec(100, 800)),
                            Platform(infos, Vec(4500, -750), Vec(100, 850)),
                            PlatformHorizontal(infos, Vec(4950, -800), Vec(100, 50), max_left=4700, max_right=4950),
                            Platform(infos, Vec(5150, -850), Vec(150, 900)),
                            Platform(infos, Vec(5400, -1250), Vec(400, 450)),
                            Platform(infos, Vec(5400, -750), Vec(400, 450)),
                            Lever(infos, Vec(5200, -900), wireless1),
                            wireless1,
                            Checkpoint(infos, Vec(5250, -851)),
                            Platform(infos, Vec(5500, -150), Vec(250, 200)),
                            Player(infos, Vec(5550, -200)),
                            Checkpoint(infos, Vec(5650, -151)),
                            Player(infos, Vec(5900, -200)),
                            Player(infos, Vec(6250, -50)),
                            Platform(infos, Vec(6400, 50), Vec(100, 200)),
                            Checkpoint(infos, Vec(6450, 50)),
                            Player(infos, Vec(6600, 50)),
                            Platform(infos, Vec(6750, 50), Vec(100, 200)),
                            Checkpoint(infos, Vec(6800, 50)),
                            Platform(infos, Vec(6950, 0), Vec(100, 200)),
                            Platform(infos, Vec(7150, -50), Vec(100, 200)),
                            Platform(infos, Vec(7350, -100), Vec(100, 200)),
                            Platform(infos, Vec(7550, -150), Vec(100, 200)),
                            Platform(infos, Vec(7750, -200), Vec(100, 200)),
                            Platform(infos, Vec(7950, -250), Vec(100, 1200)),
                            Checkpoint(infos, Vec(8000, -249)),
                            Player(infos, Vec(8300, -150)),
                            Platform(infos, Vec(8500, -1000), Vec(200, 1450)),
                            PlatformVertical(infos, Vec(8400, 300), Vec(100, 50), max_up=300, max_down=550),
                            Platform(infos, Vec(8500, 550), Vec(300, 600)),
                            Checkpoint(infos, Vec(8750, 551)),
                            Platform(infos, Vec(8900, 550), Vec(100, 250)),
                            PlatformHorizontal(infos, Vec(8850, 850), Vec(50, 50), max_left=8850, max_right=9350),
                            PlatformVertical(infos, Vec(8800, 850), Vec(50, 50), max_down=850, max_up=550),
                            Platform(infos, Vec(9000, 750), Vec(350, 50)),
                            Observer(infos, Vec(9400, 700)),
                            door1,
                            Platform(infos, Vec(9000, 550), Vec(550, 150)),
                            Button(infos, Vec(9000, 700), door2),
                            Platform(infos, Vec(9650, 500), Vec(100, 50)),
                            Platform(infos, Vec(9850, 450), Vec(100, 50)),
                            PlatformVertical(infos, Vec(10050, 400), Vec(100, 50), max_down=400, max_up=-150),
                            Observer(infos, Vec(9750, -150)),
                            Button(infos, Vec(9450, -150), door1),
                            Observer(infos, Vec(10350, -150)),
                            door2,
                            wireless2,
                            Platform(infos, Vec(10650, -100), Vec(100, 50)),
                            Lever(infos, Vec(10650, -150), wireless2),
                            Platform(infos, Vec(10250, 350), Vec(100, 50)),
                            Platform(infos, Vec(10450, 300), Vec(100, 50)),
                            Platform(infos, Vec(10600, -100), Vec(50, 250)),
                            Platform(infos, Vec(10850, 250), Vec(550, 50)),
                            Checkpoint(infos, Vec(10950, 251), True)]
        if self.actual_level == 2:
            door1 = Door(infos, Vec(12200, 50), 1)
            door5 = Door(infos, Vec(14700, 700), 4)
            door6 = Door(infos, Vec(14200, -200), 6)
            door7 = Door(infos, Vec(14700, 300), 7)
            door8 = Door(infos, Vec(14750, 300), 8)
            self.objects = [Platform(infos, Vec(10850, 250), Vec(550, 50)),
                            Checkpoint(infos, Vec(10950, 251), True),
                            Platform(infos, Vec(11500, 200), Vec(100, 50)),
                            Platform(infos, Vec(11700, 150), Vec(100, 50)),
                            PlatformHorizontal(infos, Vec(11850, 300), Vec(100, 50), max_left=11850, max_right=12250),
                            ActivatorByPos(infos, Vec(12250, 300), Vec(100, 50), door1),
                            Observer(infos, Vec(11900, 400)),
                            Observer(infos, Vec(12250, 400)),
                            door1,
                            Mirror(infos, Vec(11900, 100), Vec(0, -1), Vec(-1, 0)),
                            Platform(infos, Vec(11950, 100), Vec(350, 50)),
                            Platform(infos, Vec(11950, 0), Vec(300, 50)),
                            Checkpoint(infos, Vec(12250, 101)),
                            Platform(infos, Vec(12400, 50), Vec(100, 50))] + self.partie1(Vec(12400, 0)) + \
                           [Platform(infos, Vec(13800, 350), Vec(200, 800)),
                            Platform(infos, Vec(14100, 350), Vec(1000, 350)),
                            Player(infos, Vec(13800, 300)),
                            Checkpoint(infos, Vec(13850, 351)),
                            PlatformVertical(infos, Vec(14000, 350), Vec(100, 50), max_up=350, max_down=1000),
                            Platform(infos, Vec(14200, 950), Vec(100, 50)),
                            Platform(infos, Vec(14400, 900), Vec(50, 100)),
                            Mirror(infos, Vec(14400, 700), Vec(0, -1), Vec(1, 0)),
                            Mirror(infos, Vec(14750, 700), Vec(0, -1), Vec(-1, 0)),
                            Button(infos, Vec(14750, 900), door6),
                            Platform(infos, Vec(14700, 800), Vec(50, 200)),
                            door5,
                            Platform(infos, Vec(13800, -500), Vec(50, 700)),
                            Platform(infos, Vec(13900, -500), Vec(50, 700)),
                            Observer(infos, Vec(13850, 0)),
                            Observer(infos, Vec(13850, -300)),
                            Mirror(infos, Vec(13950, 150), Vec(0, -1), Vec(1, 0)),
                            PlatformHorizontal(infos, Vec(14200, 150), Vec(100, 50), max_left=14200, max_right=14500),
                            PlatformHorizontal(infos, Vec(14500, 50), Vec(100, 50), max_left=14500, max_right=14600),
                            Mirror(infos, Vec(14459, 50), Vec(0, -1), Vec(1, 0)),
                            ActivatorByPos(infos, Vec(14300, 150), Vec(100, 50), door5),
                            ActivatorByPos(infos, Vec(14500, 150), Vec(100, 50), door7),
                            ActivatorByPos(infos, Vec(14600, 50), Vec(100, 50), door8),
                            Mirror(infos, Vec(14650, 150), Vec(0, -1), Vec(-1, 0)),
                            door7,
                            door8,
                            Platform(infos, Vec(14200, 200), Vec(50, 150)),
                            Mirror(infos, Vec(14150, 100), Vec(0, -1), Vec(-1, 0)),
                            Observer(infos, Vec(13950, 100)),
                            Mirror(infos, Vec(13950, -100), Vec(0, -1), Vec(1, 0)),
                            Mirror(infos, Vec(14200, -100), Vec(0, 1), Vec(-1, 0)),
                            Platform(infos, Vec(14200, -50), Vec(250, 200)),
                            door6,
                            Mirror(infos, Vec(14200, -250), Vec(0, -1), Vec(-1, 0)),
                            Platform(infos, Vec(14250, -250), Vec(200, 200)),
                            PlatformVertical(infos, Vec(14050, -250), Vec(100, 50), max_up=-250, max_down=300),
                            Platform(infos, Vec(14700, -500), Vec(200, 800))]
        if first_use: self.checkpoint = self.objects[1]  # 49  18  21  25  28  35  40  63  1  12  32
        self.player = Player(infos, self.checkpoint.pos + Vec(-25, -50))
        self.objects.append(self.player)
        infos["objects"] = self.objects
        self.player.controlled = True

    def partie1(self, p):
        door1 = Door(infos, p + Vec(850, 200), activated_by=1)
        door2 = Door(infos, p + Vec(900, 200), activated_by=2)
        door3 = Door(infos, p + Vec(600, 0), activated_by=3)
        return [Platform(infos, p + Vec(0, 50), Vec(100, 50)),
                Platform(infos, p + Vec(250, -50), Vec(100, 250)),
                PlatformHorizontal(infos, p + Vec(250, 200), max_left=p.x() + 250, max_right=p.x() + 500),
                Platform(infos, p + Vec(400, -50), Vec(150, 100)),
                Platform(infos, p + Vec(400, 100), Vec(150, 100)),
                PlatformVertical(infos, p + Vec(350, -50), max_up=p.y() - 50, max_down=p.y() + 150),
                PlatformVertical(infos, p + Vec(550, 50), max_up=p.y() - 50, max_down=p.y() + 150),
                PlatformHorizontal(infos, p + Vec(650, 0), max_left=p.x() + 650, max_right=p.x() + 700),
                ActivatorByPos(infos, p + Vec(700, 0), Vec(50, 50), door2),
                Platform(infos, p + Vec(750, -50), Vec(50, 150)),
                Platform(infos, p + Vec(750, 200), Vec(50, 100)),
                Platform(infos, p + Vec(850, 0), Vec(300, 200)),
                PlatformVertical(infos, p + Vec(800, 100), Vec(50, 100), max_up=p.y() - 100, max_down=p.y() + 250),
                ActivatorByPos(infos, p + Vec(850, -50), Vec(50, 50), door3),
                ActivatorByPos(infos, p + Vec(1050, -50), Vec(50, 50), door1),
                PlatformHorizontal(infos, p + Vec(950, -50), max_left=p.x() + 850, max_right=p.x() + 1050),
                Player(infos, p + Vec(1000, 200)),
                Platform(infos, p + Vec(1000, 250), Vec(150, 50)),
                Checkpoint(infos, p + Vec(1100, 251)),
                door1, door2, door3]

    def set_music(self, file):
        pg.mixer.Channel(0).play(pg.mixer.Sound(os.path.dirname(__file__) + "\\" + "musics\\" + str(file)), -1)

    def collisions(self):
        for elt in self.objects:
            elt.collisions = []
        for i1 in range(len(self.objects)):
            if self.objects[i1] == self.player or type(self.objects[i1]) == Sender or type(self.objects[i1] == Player):
                for i2 in range(len(self.objects)):
                    if i1 != i2:
                        coll = self.objects[i1] & self.objects[i2]
                        if coll:
                            self.objects[i1].collisions.append((self.objects[i2], *coll))
                            self.objects[i2].collisions.append((self.objects[i1], coll[0], -coll[1]))
                            for effect in self.objects[i1].effects:
                                effect.act(self.objects[i2], self.objects[i1])
                            for effect in self.objects[i2].effects:
                                effect.act(self.objects[i1], self.objects[i2])
                        for elt in self.objects[i1].hitboxes:
                            if elt & self.objects[i2]:
                                for effect in elt.effects:
                                    effect.act(self.objects[i2], self.objects[i1])
                        for elt in self.objects[i2].hitboxes:
                            if elt & self.objects[i1]:
                                for effect in elt.effects:
                                    effect.act(self.objects[i1], self.objects[i2])

    def update(self):
        if self.actual_tutorial < self.tutorial_to_go:
            if infos["inputs"]["keyboard"].keys["space"]:
                self.actual_tutorial += 1
        else:
            i = 0
            while i < len(self.to_do):
                if self.to_do[i][:4] == "pass":
                    self.to_do.pop(i)
                elif self.to_do[i][:6] == "sender":
                    d = self.to_do[i].split(" ")[1:]
                    d = Vec(int(d[0]), int(d[1]))
                    self.objects.append(
                        Sender(infos, self.player.pos + self.player.size / 2 - Vec(15, 15), d, self.player))
                    self.to_do.pop(i)
                elif self.to_do[i] == "new_checkpoint":
                    for o in range(len(self.objects)):
                        elt = self.objects[o]
                        if elt.controlled:
                            if elt.end_lvl:
                                self.actual_level += 1
                                self.lvl()
                                self.checkpoint = self.objects[1]
                                self.lvl()
                            else:
                                self.checkpoint = elt
                                self.lvl()
                            break
                    self.to_do.pop(i)
                elif self.to_do[i] == "reset":
                    self.lvl()
                    self.to_do.pop(i)
                else:
                    i += 1
            i = 0
            while i < len(self.objects):
                if self.objects[i].controlled and self.objects[i] != self.player and type(self.objects[i]) != Checkpoint:
                    self.player.controlled = False
                    self.player = self.objects[i]
                if self.objects[i].delete:
                    self.objects.pop(i)
                else:
                    i += 1
            for elt in self.objects:
                a = elt.update()
                if a is not None: self.to_do.append(a)
                if type(elt) == Checkpoint and elt.pos == self.checkpoint.pos:
                    elt.anim = "taked"
            self.collisions()
            a = self.player.collision()
            if a is not None: self.to_do.append(a)
            for i in range(len(self.objects) - 1, -1, -1):
                if type(self.objects[i]) == Sender or type(self.objects[i]) == Player:
                    self.objects[i].collision()
            if infos["inputs"]["keyboard"].keys["reset"]:
                self.lvl()

    def draw(self):
        infos["centre"] = self.player.pos
        if type(self.player) == Lever:
            infos["centre"] = self.player.control.pos
        infos["screen"].fill((250, 250, 250))
        screen = Hitbox(infos["centre"] - Vec(*infos["screen_size"]) / 2, Vec(*infos["screen_size"]))
        self.checkpoint.anim = "taked"
        to_draw = ()
        for elt in self.objects:
            if screen & elt or type(elt) == ActivatorByPos:
                to_draw += (elt,)
        # merge_sort(to_draw, self.get_proximity)
        second_turn = []
        for elt in to_draw:
            if type(elt) == ActivatorByPos:
                second_turn.append(elt)
            else:
                elt.secondary_draw()
            for elt in second_turn:
                elt.secondary_draw()
        for elt in to_draw:
            elt.draw()
        self.player.draw()
        for elt in self.UIs:
            self.UIs[elt].draw()
        if self.actual_tutorial < self.tutorial_to_go:
            infos["screen"].blit(self.tutorial[self.actual_tutorial], (100, 100))
        pg.display.flip()

    @staticmethod
    def get_proximity(elt):
        return elt.proximity


def images(filename, doing_after="reboot", size=None):
    i = 1
    res = []
    end = False
    while not end:
        f = os.path.dirname(__file__) + "\\" + "images\\" + filename + "_" + str(i) + ".png"
        if os.path.exists(f):
            if size is not None:
                im = pg.transform.scale(pg.image.load(f), size)
            else:
                im = pg.image.load(f)
            res.append(im)
        else:
            end = True
        i += 1
    res.append(doing_after)
    return res


black = (0, 0, 0)
white = (255, 255, 255)
pg.font.init()
pg.mixer.init(channels=4)
infos = {"screen_size": (1280, 660), "inputs": {"keyboard": Keyboard()}}
screen = pg.display.set_mode(infos["screen_size"], pg.RESIZABLE)  # , pg.FULLSCREEN)
infos["screen"] = screen
infos["screen_size"] = pg.display.get_surface().get_size()
infos["screen_center"] = Vec(*infos["screen_size"]) / 2
infos["centre"] = infos["screen_center"]
infos["debug"] = True
controller = Start()
clock = pg.time.Clock()
end = False
while not end:
    for inp in infos["inputs"]:
        infos["inputs"][inp].update()
    temp = controller.update()
    if temp is not None:
        controller = temp
    controller.draw()
    if infos["inputs"]["keyboard"].keys["resized"]:
        infos["screen_size"] = pg.display.get_surface().get_size()
        infos["screen_center"] = Vec(*infos["screen_size"]) / 2
    if infos["inputs"]["keyboard"].keys["end"]:
        pg.quit()
        break
    clock.tick(30)
pg.quit()
