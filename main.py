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
        self.tutorial_to_go = 0
        self.player = None
        self.objects = []
        self.actual_level = 0
        self.checkpoint = None
        self.lvl(True)
        self.UIs = {}
        self.background = pg.image.load(os.path.dirname(__file__)+"\\images\\background.png")
        self.to_do = []
        #self.set_music("bg_music1.mp3")

    def lvl(self, first_use=False):
        door1 = Door(infos, Vec(3500, -300))
        self.objects = [Checkpoint(infos, Vec(50, 0)),
                        Platform(infos, Vec(100, 0), Vec(700, 50)),
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
                        PlatformVertical(infos, Vec(1400, -800), Vec(100, 50), max_up=-800, max_down=-400),
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
                        Platform(infos, Vec(2400, -300), Vec(1000, 450)),
                        Platform(infos, Vec(2350, -700), Vec(50, 100)),
                        PlatformVertical(infos, Vec(2350, -450), Vec(50, 100), max_up=-600, max_down=50),
                        PlatformVertical(infos, Vec(2150, -1050), Vec(50, 100), max_up=-1050, max_down=-150),
                        Checkpoint(infos, Vec(3300, -299)),
                        door1,
                        ActivatorByPos(infos, Vec(3350, -350), Vec(50, 50), door1),
                        PlatformVertical(infos, Vec(3350, -650), Vec(50, 50), max_up=-650, max_down=-300),
                        Mirror(infos, Vec(3300, -650), Vec(0, -1), Vec(1, 0))]
        if first_use: self.checkpoint = self.objects[0]  # 49
        self.player = Player(infos, self.checkpoint.pos+Vec(-25, -50))
        self.objects.append(self.player)
        infos["objects"] = self.objects
        self.player.controlled = True

    def set_music(self, file):
        pg.mixer.Channel(0).play(pg.mixer.Sound(os.path.dirname(__file__)+"\\"+"musics\\"+str(file)), -1)

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
                    self.objects.append(Sender(infos, self.player.pos+self.player.size/2, d, self.player))
                    self.to_do.pop(i)
                elif self.to_do[i] == "new_checkpoint":
                    for elt in self.objects:
                        if elt.controlled:
                            self.checkpoint = elt
                            break
                    self.lvl()
                    self.to_do.pop(i)
                else:
                    i += 1
            i = 0
            while i < len(self.objects):
                if self.objects[i].controlled and self.objects[i] != self.player:
                    self.player.controlled = False
                    self.player = self.objects[i]
                if self.objects[i].delete:
                    self.objects.pop(i)
                else:
                    i += 1
            for elt in self.objects:
                a = elt.update()
                if a is not None: self.to_do.append(a)
            self.collisions()
            a = self.player.collision()
            if a is not None: self.to_do.append(a)
            for i in range(len(self.objects)-1, -1, -1):
                if type(self.objects[i]) == Sender or type(self.objects[i]) == Player:
                    self.objects[i].collision()
            if infos["inputs"]["keyboard"].keys["reset"]:
                self.lvl()

    def draw(self):
        infos["centre"] = self.player.pos
        infos["screen"].fill((250, 250, 250))
        screen = Hitbox(infos["centre"]-Vec(*infos["screen_size"])/2, Vec(*infos["screen_size"]))
        to_draw = ()
        for elt in self.objects:
            if screen & elt or type(elt) == ActivatorByPos:
                to_draw += (elt,)
        #merge_sort(to_draw, self.get_proximity)
        for elt in to_draw:
            if type(elt) == ActivatorByPos:
                pass
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
screen = pg.display.set_mode(infos["screen_size"])  # , pg.FULLSCREEN)
infos["screen"] = screen
infos["screen_size"] = pg.display.get_surface().get_size()
infos["screen_center"] = Vec(*infos["screen_size"])/2
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
    if infos["inputs"]["keyboard"].keys["end"]:
        pg.quit()
        break
    clock.tick(30)
pg.quit()
