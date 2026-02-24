import pygame # Импортируем библиотеку

pygame.init() # инициализация

windows = pygame.display.set_mode(size=(1536, 1024)) # установка размера карты

running = True # Для запуска экрана

clock = pygame.time.Clock() # Создаём метод для работы со временем

#################### Добавления анимации главному герою ########################

walkRight = [pygame.image.load('main_hero/hero_walk_right1.png'),pygame.image.load('main_hero/hero_walk_right2.png'),pygame.image.load('main_hero/hero_walk_right3.png'),pygame.image.load('main_hero/hero_walk_right4.png'),pygame.image.load('main_hero/hero_walk_right5.png'),pygame.image.load('main_hero/hero_walk_right6.png'),pygame.image.load('main_hero/hero_walk_right7.png'),pygame.image.load('main_hero/hero_walk_right8.png')]
walkLeft = [pygame.image.load('main_hero/hero_walk_left1.png'),pygame.image.load('main_hero/hero_walk_left2.png'),pygame.image.load('main_hero/hero_walk_left3.png'),pygame.image.load('main_hero/hero_walk_left4.png'),pygame.image.load('main_hero/hero_walk_left5.png'),pygame.image.load('main_hero/hero_walk_left6.png'),pygame.image.load('main_hero/hero_walk_left7.png'),pygame.image.load('main_hero/hero_walk_left8.png'),]
heroAttack = [pygame.image.load('main_hero/hero_attack1.png'),pygame.image.load('main_hero/hero_attack2.png'),pygame.image.load('main_hero/hero_attack3.png'),pygame.image.load('main_hero/hero_attack4.png'),pygame.image.load('main_hero/hero_attack5.png'),pygame.image.load('main_hero/hero_attack6.png'),pygame.image.load('main_hero/hero_attack7.png'),]
bg = pygame.image.load('main_hero/background.png')
stand = pygame.image.load('main_hero/hero_stand.png')

bulletSound = pygame.mixer.Sound('music/bullet.wav')
hitSound = pygame.mixer.Sound("music/hit.wav")
victorySound = pygame.mixer.Sound("music/victory.wav")

music = pygame.mixer.music.load("music/main_theme.mp3")
pygame.mixer.music.play(-1)


###############################################################################

score = 0

#################### Создание класса персонажа ################################

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x # координата по x на карте
        self.y = y # координата по y на карте
        self.width = width # ширина персонажа
        self.height = height # высота персонажа
        self.vel = 5 # коэффициент движения
        self.isJump = False # Пока пробел не нажат прыжок ложное значение
        self.jumpCount = 10 # Насколько вверх мы прыгаем
        self.attack = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 20, self.y, 28,60)

    def draw(self,windows):
        if self.walkCount + 1 >= 21: # 8 типов движения влево/вправо * 3 фрейма = 24
            self.walkCount = 0 

        if not(self.standing):    
            if self.left:
                windows.blit(walkLeft[self.walkCount//3], (self.x,self.y)) 
                self.walkCount += 1
            elif self.right:
                windows.blit(walkRight[self.walkCount//3], (self.x,self.y)) 
                self.walkCount += 1
            
        else:
            if self.right:
                windows.blit(walkRight[7], (self.x,self.y)) 
            else:
                windows.blit(walkLeft[7], (self.x,self.y))
        self.hitbox = (self.x + 20, self.y, 28,60)
        pygame.draw.rect(windows, (255,0,0), self.hitbox, 2) 

    

######################### Класс для пули #################################

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color 
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,windows):
        pygame.draw.circle(windows, self.color, (self.x,self.y), self.radius, )    

######################### Класс врага ###################################

class enemy(object):
    walkLeft = [pygame.image.load('enemy_hero/L1E.png'),pygame.image.load('enemy_hero/L2E.png'),pygame.image.load('enemy_hero/L3E.png'),pygame.image.load('enemy_hero/L4E.png'),pygame.image.load('enemy_hero/L5E.png'),pygame.image.load('enemy_hero/L6E.png'),pygame.image.load('enemy_hero/L7E.png'),pygame.image.load('enemy_hero/L8E.png'),pygame.image.load('enemy_hero/L9E.png'),pygame.image.load('enemy_hero/L10E.png'),pygame.image.load('enemy_hero/L11E.png')]
    walkRight = [pygame.image.load('enemy_hero/R1E.png'),pygame.image.load('enemy_hero/R2E.png'),pygame.image.load('enemy_hero/R3E.png'),pygame.image.load('enemy_hero/R4E.png'),pygame.image.load('enemy_hero/R5E.png'),pygame.image.load('enemy_hero/R6E.png'),pygame.image.load('enemy_hero/R7E.png'),pygame.image.load('enemy_hero/R8E.png'),pygame.image.load('enemy_hero/R9E.png'),pygame.image.load('enemy_hero/R10E.png'),pygame.image.load('enemy_hero/R11E.png')]
    
    def __init__(self, x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 20, self.y, 28,60)
        self.health = 10
        self.visible = True

    def draw(self, windows):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                windows.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            else:
                windows.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        
            pygame.draw.rect(windows, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20,50, 10 ))
            pygame.draw.rect(windows, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20,50 - (5 * (10 - self.health)), 10 ))
            self.hitbox = (self.x + 20, self.y, 28,60)
            pygame.draw.rect(windows, (255,0,0), self.hitbox, 2)
           
       

    def move(self):
        if self.vel > 0:
            if self.x + self.vel< self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print("hit")
        pass

font = pygame.font.SysFont('comicsans', 30, True)
elf_woman = player(200,850,70,70)
goblin = enemy(200,850, 64, 64, 450)
goblin2 = enemy(400,850, 64, 64, 650)
goblin3 = enemy(600,850, 64, 64, 850)
shootLoop = 0
bullets = []


def redrawGameWindow():

    windows.blit(bg, (0,0))
    text = font.render('Score' + str(score), 1, (255,255,255))
    windows.blit(text, (1400, 10))
    elf_woman.draw(windows)
    
    goblin.draw(windows)
    goblin2.draw(windows)
    goblin3.draw(windows)
    for bullet in bullets:
        bullet.draw(windows)
    pygame.display.flip()  # Полное обновление экрана
    


while running: # Пока не нажали кнопку quit программа будет работать
    clock.tick(24)

   


    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for bullet in bullets:
        if bullet.y - bullet.radius< goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                hitSound.play()
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
        

        if bullet.x < 1536 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    for bullet in bullets:
        if bullet.y - bullet.radius< goblin2.hitbox[1] + goblin2.hitbox[3] and bullet.y + bullet.radius > goblin2.hitbox[1]:
            if bullet.x + bullet.radius > goblin2.hitbox[0] and bullet.x - bullet.radius < goblin2.hitbox[0] + goblin2.hitbox[2]:
                hitSound.play()
                goblin2.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
        

        if bullet.x < 1536 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    for bullet in bullets:
        if bullet.y - bullet.radius< goblin3.hitbox[1] + goblin3.hitbox[3] and bullet.y + bullet.radius > goblin3.hitbox[1]:
            if bullet.x + bullet.radius > goblin3.hitbox[0] and bullet.x - bullet.radius < goblin3.hitbox[0] + goblin3.hitbox[2]:
                hitSound.play()
                goblin3.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
        

        if bullet.x < 1536 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        elf_woman.attack = True
        if elf_woman.left:    
                facing = -1
        else:
                facing = 1
        if len(bullets) < 5:
            
           bullets.append(projectile(round(elf_woman.x+elf_woman.width//2), round(elf_woman.y+elf_woman.height//2), 6, (0,0,0), facing))
        
        shootLoop = 1

    if keys[pygame.K_LEFT] and elf_woman.x > elf_woman.vel: 
        elf_woman.x -= elf_woman.vel
        elf_woman.left = True
        elf_woman.right = False
        elf_woman.standing = False
    elif keys[pygame.K_RIGHT] and elf_woman.x < 1536 - elf_woman.vel - elf_woman.width:  
        elf_woman.x += elf_woman.vel
        elf_woman.left = False
        elf_woman.right = True
        elf_woman.standing = False
    else: 
        elf_woman.standing = True
        elf_woman.walkCount = 0
        
    if not(elf_woman.isJump):
        if keys[pygame.K_UP]:
            elf_woman.isJump = True
            elf_woman.left = False
            elf_woman.right = False
            elf_woman.walkCount = 0
    else:
        if elf_woman.jumpCount >= -10:
            elf_woman.y -= (elf_woman.jumpCount * abs(elf_woman.jumpCount)) * 0.5
            elf_woman.jumpCount -= 1
        else: 
            elf_woman.jumpCount = 10
            elf_woman.isJump = False

    redrawGameWindow()


pygame.quit() # Для корректного завершения работы
