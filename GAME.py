import pgzrun
import random

WIDTH = 600
HEIGHT = 400


class Player:
    def __init__(self):
        self.actor = Actor("personagem_0")
        self.actor.pos = (100, 200)
        self.frames = ["personagem_1","personagem_2","personagem_3","personagem_4"]
        self.frames_nomove = ["frame_0","frame_1","frame_2","frame_3","frame_4","frame_5"]
        self.index = 0
        self.timer = 0

    def move(self):
        moving = False

        if keyboard.right:
            self.actor.x += 2
            moving = True
        if keyboard.left:
            self.actor.x -= 2
            moving = True
        if keyboard.down:
            self.actor.y += 2
            moving = True
        if keyboard.up:
            self.actor.y -= 2
            moving = True

        self.actor.x = max(self.actor.width//2, min(WIDTH - self.actor.width//2, self.actor.x))
        self.actor.y = max(self.actor.height//2, min(HEIGHT - self.actor.height//2, self.actor.y))

        return moving

    def animate(self, moving):
        if moving:
            self.timer += 0.5
            if self.timer > 6:
                self.timer = 0
                self.index = (self.index + 2) % 4
                self.actor.image = self.frames[self.index]
        else:
            self.timer += 0.25
            if self.timer > 6:
                self.timer = 0
                self.index = (self.index + 2) % 4
                self.actor.image = self.frames_nomove[self.index]

    def draw(self):
        self.actor.draw()


class Enemy:
    def __init__(self):
        self.actor = Actor("inimigo_0",
            (random.randint(0 + 50, WIDTH-50), random.randint(0 + 50, HEIGHT-50))
        )
        self.actor.dx = 1
        self.frames = ["inimigo_1","inimigo_2","inimigo_3","inimigo_4"]
        self.frames_nomove = ["inimigo_0","inimigoparado_1","inimigoparado_2",
                            "inimigoparado_3","inimigoparado_4",
                            "inimigoparado_5","inimigoparado_6"]
        self.index = 0
        self.timer = 0

    def update(self):
        if random.randint(0,100) < 2:
            self.actor.dx = random.choice([-1, 0, 1])

        self.actor.x += self.actor.dx

        if self.actor.left < 0 or self.actor.right > WIDTH:
            self.actor.dx *= -1

        moving = self.actor.dx != 0

        if moving:
            self.timer += 0.5
            if self.timer > 6:
                self.timer = 0
                self.index = (self.index + 3) % 4
                self.actor.image = self.frames[self.index]
        else:
            self.timer += 0.25
            if self.timer > 6:
                self.timer = 0
                self.index = (self.index + 3) % 4
                self.actor.image = self.frames_nomove[self.index]

    def draw(self):
        self.actor.draw()


background = Actor("fundo")
background.pos = (WIDTH/2, HEIGHT/2)

player = Player()
enemies = [Enemy() for i in range(4)]

crystal = Actor("cristal")
crystal.pos = (300, 170)

estado = "MENU"
score = 0
life = 10
som = True

music.play("musicadefundo")
music.set_volume(0.5)


def reset():
    global score, life
    score = 0
    life = 10
    if som:
        music.play("musicadefundo")


def draw():
    screen.clear()

    if estado=="MENU":
        screen.fill((0, 0, 0))
        screen.draw.text("Fragmentos do Reino Sombrio",center=(WIDTH/2,120),fontsize=40)
        b1=Rect((200,200),(200,50))
        b2=Rect((200,270),(200,50))
        b3=Rect((200,340),(200,50))

        screen.draw.filled_rect(b1,"green")
        screen.draw.text("INICIAR",center=b1.center,fontsize=30)
        screen.draw.filled_rect(b2,"orange")
        screen.draw.text("SOM ON" if som else "SOM OFF",center=b2.center,fontsize=30)
        screen.draw.filled_rect(b3,"red")
        screen.draw.text("SAIR",center=b3.center,fontsize=30)


    elif estado=="PLAYING":
        background.draw()
        player.draw()
        for e in enemies:
            e.draw()
        crystal.draw()
        screen.draw.text(f"pontos: {score}",(20,20),fontsize=30)
        screen.draw.text(f"vida: {life}",(20,55),fontsize=30)

    elif estado=="GAME_OVER":
        screen.draw.text("FIM DE JOGO",center=(WIDTH/2,160),fontsize=60,color="red")
        r=Rect((180,240),(240,60))
        screen.draw.filled_rect(r,"blue")
        screen.draw.text("REINICIAR",center=r.center,fontsize=30)


def update():
    global score, life, estado

    if estado != "PLAYING":
        return

    moving = player.move()
    player.animate(moving)

    for enemy in enemies:
        enemy.update()

        if player.actor.colliderect(enemy.actor):
            life -= 1
            enemy.actor.x = random.randint(50, WIDTH-50)
            if life <= 0:
                estado="GAME_OVER"
                music.stop()

    if player.actor.colliderect(crystal):
        score += 1
        crystal.pos = (
            random.randint(0 + 50, WIDTH-50),
            random.randint(0 + 50, HEIGHT-50)
        )
        if score>=10:
            estado="GAME_OVER"
            music.stop()

def on_mouse_down(pos):
    global estado,som

    if estado=="MENU":
        if Rect((200,200),(200,50)).collidepoint(pos):
            estado="PLAYING"
            reset()

        elif Rect((200,270),(200,50)).collidepoint(pos):
            som=not som
            music.play("musicadefundo") if som else music.stop()

        elif Rect((200,340),(200,50)).collidepoint(pos):
            quit()

    elif estado=="GAME_OVER":
        if Rect((180,240),(240,60)).collidepoint(pos):
            estado="PLAYING"
            reset()

pgzrun.go()
