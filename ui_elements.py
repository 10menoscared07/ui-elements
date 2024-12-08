import pygame
import sys
from enum import Enum

pygame.init()

vec2 = pygame.math.Vector2

def clamp(val, mini, maxi):
    if val >= maxi:
        return maxi
    if val <= mini:
        return mini
    return val

### classes

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.timer = 0
        self.finsied = False
    
    def update(self, deltaTime):
        self.timer += deltaTime
        if self.timer >= self.duration:
            self.finsied = True

    def getPercent(self):
        return clamp(self.timer/self.duration, 0, 1)*100

    def getNormalized(self):
        return clamp(self.timer/self.duration, 0, 1)

    def isFinished(self):
        return self.finsied
    
    def end(self):
        self.timer = 0
        self.finsied = True

    def reset(self):
        self.timer = 0
        self.finsied = False

class Interpolate:
    @staticmethod
    def lerp(final, initial, time, duration):
        return initial + (final-initial)*clamp(time/duration, 0, 1)
    
    @staticmethod
    def lerpNorm(final, initial, time):
        return initial + (final-initial)*clamp(time, 0, 1)

    @staticmethod
    def easeInOutNorm(final, initial, time):
        # Ease-in-out function
        if time < 0.5:
            # Ease-in phase
            value = initial + (final - initial) * (2 * time * time)
        else:
            # Ease-out phase
            value = initial + (final - initial) * (1 - pow(-2 * time + 2, 2) / 2)
        
        return value

class ButtonStyle:
    def __init__(self):
        self.text = {"size":50,
                    "font":"font.ttf",
                    "fg":(200,200,200),
                    "bg":None,
                    "antialias":True,
                    "wraplength":700}

        self.button = {"padx":15,
                       "pady":15,
                       "bg":(10,10,10),
                       'outline':(200,20,100),
                       'outline-thick':1}
        self.hoverInAnim = {"color":(200,200,200),
                        "thickness":5,
                        "over":False,
                        "ongoing":False,
                        'startPos':None,
                        'endPos':None}


        self.hover = {"fg":(250,250,250),
                    "size":52,
                    'padx':1,
                    'pady':2,
                    "font":"font.ttf",
                    'bg':(30,30,30)}

        self.clickAnim = {'bg':(30,30,30), 'ongoing':False}
        self.clickTime = 0.1
        self.hoverTime  = 0.2

class Button:
    class State(Enum):
        DEFAULT = 1
        HOVERED = 2
        LEFTCLICKED = 3
        RIGHTCLICKED = 4
        DISABLED = -1


    def __init__(self,mgr, pos, text, function, style:ButtonStyle):
        self.pos = pos ### center aligned
        self.mgr = mgr

        self.mgr.buttons.append(self)
        self.function = function
        self.style = style

        self.text = {"text":text, 
                    "size":self.style.text['size'],
                    "font":self.style.text['font'],
                    "fg":self.style.text['fg'],
                    "bg":self.style.text['bg'],
                    "antialias":self.style.text['antialias'],
                    "wraplength":self.style.text['wraplength'],}
        
        self.button = {"padx":self.style.button['padx'],
                       "pady":self.style.button['pady'],
                       "bg":self.style.button['bg'],
                       'outline':self.style.button['outline'],
                       'outline-thick':self.style.button['outline-thick'],}

        self.font = pygame.font.Font(self.text['font'], self.text['size'])



        self.state = Button.State.DEFAULT

        ### making animation for hover
        self.hoverInTimer = Timer(self.style.hoverTime)
        self.hoverInAnim = {"color":self.style.hoverInAnim['color'],
                        "thickness":self.style.hoverInAnim['thickness'],
                        "over":self.style.hoverInAnim['over'],
                        "ongoing":self.style.hoverInAnim['ongoing'],
                        'startPos':self.style.hoverInAnim['startPos'],
                        'endPos':self.style.hoverInAnim['endPos'],}


        self.hover = {"fg":self.style.hover['fg'],
                    "size":self.style.hover['size'],
                    'padx':self.style.hover['padx'],
                    'pady':self.style.hover['pady'],
                    "font":self.style.hover['font'],
                    'bg':self.style.hover['bg'],}

        self.clickAnim = {'bg':self.style.clickAnim['bg'],
                          'ongoing':False}
        self.clickTimer = Timer(self.style.clickTime)

        self.hoverFont = pygame.font.Font(self.hover['font'], self.hover['size'])

        self.altered = True


    def manageSurfaces(self):

        if self.altered:
            if self.state == Button.State.HOVERED:
                self.textImage = self.hoverFont.render(self.text['text'], self.text['antialias'], self.hover['fg'], None, self.text['wraplength'])
                self.textRect = self.textImage.get_rect(center=self.pos)

                    
                self.buttonRect = self.textRect.copy()
                self.buttonRect.width += 2*self.button['padx'] + 2*self.hover['padx']
                self.buttonRect.height += 2*self.button['pady'] + 2*self.hover['pady']
                self.buttonRect.center = self.textRect.center
            else:

                self.textImage = self.font.render(self.text['text'], self.text['antialias'], self.text['fg'], self.text['bg'], self.text['wraplength'])
                self.textRect = self.textImage.get_rect(center=self.pos)
                    
                self.buttonRect = self.textRect.copy()
                self.buttonRect.width += 2*self.button['padx']
                self.buttonRect.height += 2*self.button['pady']
                self.buttonRect.center = self.textRect.center

            self.altered = False


    def eventUpdate(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.state == Button.State.HOVERED:
                    self.state = Button.State.LEFTCLICKED
                    
                    self.function()
                    self.clickAnim['ongoing'] = True
                    
                    

    def update(self, dt):
        self.manageSurfaces()
        mousePos = pygame.mouse.get_pos()

        if self.buttonRect.collidepoint(*mousePos):
            self.state = Button.State.HOVERED
            if not self.hoverInAnim['ongoing']:
                self.hoverInAnim['ongoing'] = True
                self.hoverInAnim['over'] = False
                self.altered = True
        else:
            self.state = Button.State.DEFAULT

            if self.hoverInAnim['ongoing']:
                self.hoverInAnim['ongoing'] = False
                self.hoverInAnim['over'] = True
                self.hoverInAnim['endPos'] = None
                self.hoverInAnim['startPos'] = None
                self.hoverInTimer.reset()
                self.altered = True


        if self.hoverInAnim['ongoing']:
            self.hoverInTimer.update(dt)

            self.hoverInAnim['startPos'] = vec2(0,0)
            self.hoverInAnim['startPos'].x = self.buttonRect.midbottom[0] + Interpolate.easeInOutNorm(self.buttonRect.width//2, 0, self.hoverInTimer.getNormalized())
            self.hoverInAnim['startPos'].y  = self.buttonRect.midbottom[1]

            self.hoverInAnim['endPos'] = vec2(0,0)
            self.hoverInAnim['endPos'].x = self.buttonRect.midbottom[0] - Interpolate.easeInOutNorm(self.buttonRect.width//2, 0, self.hoverInTimer.getNormalized())
            self.hoverInAnim['endPos'].y  = self.buttonRect.midbottom[1]

            if self.hoverInTimer.isFinished():
                self.hoverInAnim['over'] = True


        if self.clickAnim['ongoing']:
            self.clickTimer.update(dt)
            if self.clickTimer.isFinished():
                self.clickAnim['ongoing'] = False
                self.clickTimer.reset()


    def draw(self, window):
        if self.state == Button.State.HOVERED or self.state == Button.State.LEFTCLICKED:

            if self.clickAnim['ongoing']:
                pygame.draw.rect(window, self.clickAnim['bg'], self.buttonRect, )
            else:
                pygame.draw.rect(window, self.button['bg'], self.buttonRect, )

            # pygame.draw.rect(window, self.button['outline'], self.buttonRect, width=self.button['outline-thick'])
            window.blit(self.textImage, self.textRect)

        else:
            pygame.draw.rect(window, self.button['bg'], self.buttonRect)
            window.blit(self.textImage, self.textRect)

        

        if self.hoverInAnim['ongoing']:
            pygame.draw.line(window, self.hoverInAnim['color'],self.hoverInAnim['startPos'], self.hoverInAnim['endPos'], self.hoverInAnim['thickness'])

class LabelStyle:
    def __init__(self):
        self.text = {"font":"font.ttf",
                    "fg":(200,200,200),
                    "bg":None,
                    "antialias":True,
                    "wraplength":600}
        
class Label:
    def __init__(self, mgr, pos, text, style:LabelStyle):
        self.pos = pos
        self.mgr = mgr

        self.mgr.labels.append(self)
        
        self.text = {"text":text, 
                    "size":style.text['size'],
                    "font":style.text['font'],
                    "fg":style.text['fg'],
                    "bg":style.text['bg'],
                    "antialias":style.text['antialias'],
                    "wraplength":style.text['wraplength'],}

        self.font = pygame.font.Font(self.text['font'], self.text['size'])

        self.altered = True

    def change(self, prop, val):
        try:
            self.text[prop] = val
            self.altered = True
        except:
            print("Unknown property or invalid value")

    def manageSurfaces(self):
        if self.altered:
            self.altered = False

            self.textImage = self.font.render(self.text['text'], self.text['antialias'], self.text['fg'], self.text['bg'], self.text['wraplength'])
            self.textRect = self.textImage.get_rect(center=self.pos)

    def update(self, dt):
        self.manageSurfaces()

    def draw(self, window):
        window.blit(self.textImage, self.textRect)

class UIManager:
    def __init__(self):
        self.buttons = []
        self.labels = []

    def update(self, dt):
        for btn in self.buttons:
            btn.update(dt)

        for lbl in self.labels:
            lbl.update(dt)

    def draw(self, window):
        for btn in self.buttons:
            btn.draw(window)

        for lbl in self.labels:
            lbl.draw(window)

    def eventUpdate(self, event):
        for btn in self.buttons:
            btn.eventUpdate(event)

### gameloop

res = vec2(1280, 720)
screen = pygame.window.Window("ui elements", res,)

dt = 1/60
MAXFPS = 100000
clock = pygame.time.Clock()

def clicked():
    global lbl1, count
    count += 1
    lbl1.change("text", f"U clicked button {count} timers")

### initiaing the ui elements
ui = UIManager()

bs = ButtonStyle()
btn1 = Button(ui, vec2(300,300), "Will u press me!", clicked, bs)
btn2 = Button(ui, vec2(600,500), "Click me twice", clicked, bs)

ls = LabelStyle()
ls.text['size'] = 20

lbl1 = Label(ui, vec2(500,400), "None clicked!", ls)


ls2 = LabelStyle()
ls2.text['size'] = 50

lbl2 = Label(ui, vec2(640,100), "ui elements ", ls2)

count = 0


### gameloop
while 1:
    window = screen.get_surface()
    clock.tick(MAXFPS)
    window.fill((30,30,30))


    fps = clock.get_fps()
    dt = 1/fps if fps else 1/60

    lbl2.change("text", f"current fps : {int(fps)}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        ui.eventUpdate(event)

    ui.update(dt)
    ui.draw(window)

    screen.flip()
