# You need to use f, g and h keys to play
import pyglet
import random


class Gamerun(pyglet.window.Window):
    def __init__(self):
        super(Gamerun, self).__init__(330, 600, 'Bouncy Tiles')
        self.tile1speed = 3
        self.tile2speed = 3
        self.tile3speed = 3
        self.truelist = ['on_loose1', 'on_loose2', 'on_loose3', 'upw1', 'upw2', 'upw3']
        for i in self.truelist:
            setattr(self, i, True)
        self.falselist = ['loose', 'min1', 'min2', 'min3']
        for i in self.falselist:
            setattr(self, i, False)
        self.batch = pyglet.graphics.Batch()
        self.bgimage = pyglet.resource.image('bg.jpg')
        self.tileimg = pyglet.resource.image('blackimg.jpg')
        self.pointerimg = pyglet.resource.image('point.png')
        self.pointerimgclicked = pyglet.resource.image('pointclicked.png')
        self.tileimg.height = 75
        self.tileimg.width = 107
        self.tileslist = ['tilesp1', 'tilesp2', 'tilesp3']
        for s in self.tileslist:
            setattr(self, s, pyglet.sprite.Sprite(self.tileimg, batch=self.batch))
        self.tilesp1.position = 0, 525, 0
        self.tilesp2.position = 112, 525, 0
        self.tilesp3.position = 223, 525, 0
        self.pointer1 = pyglet.sprite.Sprite(self.pointerimg, batch=self.batch)
        self.pointer2 = pyglet.sprite.Sprite(self.pointerimg, batch=self.batch)
        self.pointer3 = pyglet.sprite.Sprite(self.pointerimg, batch=self.batch)
        self.tilesp1.color = (0, 0, 0)
        self.tilesp2.color = (0, 0, 0)
        self.tilesp3.color = (0, 0, 0)
        self.score = 0
        file = open("bscore.txt", "r")
        self.bestscore = file.read()
        file.close
        file = open("rscore.txt", "r")
        self.recscore = file.read()
        file.close

    def on_draw(self):
        self.clear()
        self.bgimage.blit(0, 0)
        self.scorelabel = pyglet.text.Label(f'S:{str(self.score)}', font_size=30, anchor_x='center', x=165, y=560, batch=self.batch)
        self.bestscorelbl = pyglet.text.Label(f'B:{str(self.bestscore)}', font_size=30, anchor_x='center', x=60, y=560, batch=self.batch)
        self.recscorelbl = pyglet.text.Label(f'R:{str(self.recscore)}', font_size=30, anchor_x='center', x=278, y=560, batch=self.batch)
        self.pointer1.position = 30, 250, 0
        self.pointer2.position = 140, 250, 0
        self.pointer3.position = 250, 250, 0
        self.batch.draw()

        if self.upw1:
            self.tilesp1.y -= self.tile1speed
        if self.upw2:
            self.tilesp2.y -= self.tile2speed
        if self.upw3:
            self.tilesp3.y -= self.tile3speed

        if self.tilesp1.y < 0:
            self.upw1 = False
            self.min1 = True
            if self.on_loose1:
                self.loose = True
            else:
                self.on_loose1 = True
                self.score += 1

        if self.tilesp2.y < 0:
            self.upw2 = False
            self.min2 = True
            if self.on_loose2:
                self.loose = True
            else:
                self.on_loose2 = True
                self.score += 1

        if self.tilesp3.y < 0:
            self.upw3 = False
            self.min3 = True
            if self.on_loose3:
                self.loose = True
            else:
                self.on_loose3 = True
                self.score += 1

        if self.min1:
            self.tilesp1.y += self.tile1speed
        if self.min2:
            self.tilesp2.y += self.tile2speed
        if self.min3:
            self.tilesp3.y += self.tile3speed

        if self.tilesp1.y > 525:
            self.min1 = False
            self.upw1 = True
            if self.on_loose1:
                self.loose = True
            else:
                self.on_loose1 = True
                self.score += 1

        if self.tilesp2.y > 525:
            self.min2 = False
            self.upw2 = True
            if self.on_loose2:
                self.loose = True
            else:
                self.on_loose2 = True
                self.score += 1

        if self.tilesp3.y > 525:
            self.min3 = False
            self.upw3 = True
            if self.on_loose3:
                self.loose = True
            else:
                self.on_loose3 = True
                self.score += 1

        if self.loose:

            file = open("bscore.txt", "r")
            if int(file.read()) < self.score:
                file.close()
                file = open("bscore.txt", "w")
                file.write(str(self.score))
            file.close()

            file = open("rscore.txt", "w")
            file.write(str(self.score))
            file.close()

            pyglet.app.exit()

    def on_key_press(self, symbol, modifier):
        if symbol == 102:
            self.check_collision1(self.pointer1, self.tilesp1)
            self.pointer1 = pyglet.sprite.Sprite(self.pointerimgclicked, batch=self.batch)
        if symbol == 103:
            self.check_collision2(self.pointer2, self.tilesp2)
            self.pointer2 = pyglet.sprite.Sprite(self.pointerimgclicked, batch=self.batch)
        if symbol == 104:
            self.check_collision3(self.pointer3, self.tilesp3)
            self.pointer3 = pyglet.sprite.Sprite(self.pointerimgclicked, batch=self.batch)

    def on_key_release(self, symbol, modifiers):
        if symbol == 102:
            self.pointer1 = pyglet.sprite.Sprite(self.pointerimg, batch=self.batch)
        if symbol == 103:
            self.pointer2 = pyglet.sprite.Sprite(self.pointerimg, batch=self.batch)
        if symbol == 104:
            self.pointer3 = pyglet.sprite.Sprite(self.pointerimg, batch=self.batch)

    def check_collision1(self, pointer1, tilesp1):
        pointer1_box = (
            pointer1.x,
            pointer1.y,
            pointer1.x + pointer1.width,
            pointer1.y + pointer1.height
        )

        tilesp1_box = (
            tilesp1.x,
            tilesp1.y,
            tilesp1.x + tilesp1.width,
            tilesp1.y + tilesp1.height
        )

        if self.bounding_box_collision(pointer1_box, tilesp1_box):
            self.on_loose1 = False
            self.tile1speed = random.randint(2, 6)
            self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
            self.tilesp1.color = self.color
        else:
            self.loose = True

    def check_collision2(self, pointer2, tilesp2):
        pointer2_box = (
            pointer2.x,
            pointer2.y,
            pointer2.x + pointer2.width,
            pointer2.y + pointer2.height
        )

        tilesp2_box = (
            tilesp2.x,
            tilesp2.y,
            tilesp2.x + tilesp2.width,
            tilesp2.y + tilesp2.height
        )

        if self.bounding_box_collision(pointer2_box, tilesp2_box):
            self.on_loose2 = False
            self.tile2speed = random.randint(2, 6)
            self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
            self.tilesp2.color = self.color
        else:
            self.loose = True

    def check_collision3(self, pointer3, tilesp3):
        pointer3_box = (
            pointer3.x,
            pointer3.y,
            pointer3.x + pointer3.width,
            pointer3.y + pointer3.height
        )

        tilesp3_box = (
            tilesp3.x,
            tilesp3.y,
            tilesp3.x + tilesp3.width,
            tilesp3.y + tilesp3.height
        )

        if self.bounding_box_collision(pointer3_box, tilesp3_box):
            self.on_loose3 = False
            self.tile3speed = random.randint(2, 6)
            self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
            self.tilesp3.color = self.color
        else:
            self.loose = True

    def bounding_box_collision(self, box1, box2):
        x1, y1, x2, y2 = box1
        x3, y3, x4, y4 = box2
        return not (x2 < x3 or x4 < x1 or y2 < y3 or y4 < y1)


if __name__ == '__main__':
    pyglet.resource.path = ['res']
    pyglet.resource.reindex()
    window = Gamerun()
    pyglet.app.run()
