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
        self.tutorial_to_go = 1
        self.player = Player(infos, Vec(0, 0))
        self.objects = [self.player,
                        Platform(infos, Vec(0, 40), Vec(1000, 20)),
                        PlatformVertical(infos, Vec(100, 0))]
        self.UIs = {}
        infos["objects"] = self.objects
        self.to_do = []
        #self.set_music("bg_music1.mp3")

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

    def draw(self):
        infos["centre"] = self.player.pos
        infos["screen"].fill(black)
        screen = Hitbox(infos["centre"]-Vec(*infos["screen_size"])/2, Vec(*infos["screen_size"]))
        to_draw = ()
        for elt in self.objects:
            if screen & elt:
                to_draw += (elt,)
        merge_sort(to_draw, self.get_proximity)
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
