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

###############################################################################

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

    def draw(self, windows):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:
            windows.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        else:
            windows.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1

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



elf_woman = player(200,850,70,70)
goblin = enemy(200,850, 64, 64, 450)
bullets = []


def redrawGameWindow():

    windows.blit(bg, (0,0))
    elf_woman.draw(windows)
    goblin.draw(windows)
    for bullet in bullets:
        bullet.draw(windows)
    pygame.display.flip()  # Полное обновление экрана
    


while running: # Пока не нажали кнопку quit программа будет работать
    clock.tick(24)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for bullet in bullets:
        if bullet.x < 1536 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        elf_woman.attack = True
        if elf_woman.left:    
                facing = -1
        else:
                facing = 1
        if len(bullets) < 5:
            
            bullets.append(projectile(round(elf_woman.x+elf_woman.width//2), round(elf_woman.y+elf_woman.height//2), 6, (0,0,0), facing))


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
