import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

#################### Добавления анимации и музыки главному герою ########################

walkRight = [pygame.image.load('Pygame_Final/Samurai/Samurai_r1.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r2.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r3.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r4.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r5.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r6.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r7.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r8.png')]
walkLeft = [pygame.image.load('Pygame_Final/Samurai/Samurai_r1.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r2.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r3.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r4.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r5.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r6.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r7.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r8.png')]
Jump = [pygame.image.load('Pygame_Final/Samurai/Samurai_jump1.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_jump2.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_jump3.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_jump4.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_jump5.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_jump6.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_jump7.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_jump8.png')]
Attack = [pygame.image.load('Pygame_Final/Samurai/Samurai_attack1.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_attack2.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_attack3.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_attack4.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_attack5.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_attack6.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_attack7.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_attack8.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_attack9.png')]
ultraAttack = [pygame.image.load('Pygame_Final/Samurai/Samurai_ultraAttack1.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_ultraAttack2.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_ultraAttack3.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_ultraAttack4.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_ultraAttack5.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_ultraAttack6.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_ultraAttack7.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_ultraAttack8.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_ultraAttack9.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_ultraAttack10.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_ultraAttack11.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_ultraAttack12.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_ultraAttack13.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_ultraAttack14.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_ultraAttack15.png')]


##################### Класс для создания параллакса #######################

class ParallaxLayer:
    def __init__(self, image_path, base_x, speed, z_index):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.width = self.image.get_width()
        self.base_x = base_x
        self.speed = speed
        self.z_index = z_index
        self.x_pos = base_x  # Текущая позиция
        
    def update(self, camera_offset):
        """Обновляем позицию с учетом параллакса"""
        self.x_pos = self.base_x + camera_offset * self.speed
        
        # Зацикливание для бесконечности
        if self.x_pos <= -self.width:
            self.x_pos += self.width
            self.base_x += self.width  # Важно: обновляем базовую позицию
        elif self.x_pos >= self.width:
            self.x_pos -= self.width
            self.base_x -= self.width
    
    def draw(self, screen):
        """Рисуем слой с учетом зацикливания"""
        # Рисуем основное изображение
        screen.blit(self.image, (self.x_pos, 0))
        
        # Рисуем дополнительное слева или справа для бесшовности
        if self.x_pos > 0:
            # Если уехали вправо, рисуем копию слева
            screen.blit(self.image, (self.x_pos - self.width, 0))
        elif self.x_pos < 0:
            # Если уехали влево, рисуем копию справа
            screen.blit(self.image, (self.x_pos + self.width, 0))

################################################################################

################ Класс для создания нашего главного героя ######################

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x # координата по x на карте
        self.y = y # координата по y на карте
        self.width = width # ширина персонажа
        self.height = height # высота персонажа
        self.vel = 5 # коэффициент движения
        self.isJump = False # Пока вверх не нажат прыжок ложное значение
        self.jumpCount = 10 # Насколько вверх мы прыгаем
        self.attack = False # загрузка анимации атаки
        self.attackCount = 0  
        self.ultraAttack = False # загрузка анимации ультра
        self.ultraAttackCount = 0  
        self.left = False # загрузка анимации влево
        self.right = False # загрузка анимации вправо
        self.walkCount = 0 # счётчик движения
        self.standing = True # загрузка анимации стояния

    def draw(self,screen):
        if self.walkCount + 1 >= 24:
            self.walkCount = 0
        if self.attackCount + 1 >= 27:
            self.attackCount = 0
            self.attack = False
        if self.ultraAttackCount + 1 >= 45:
            self.ultraAttackCount = 0
            self.ultraAttack = False


        if self.attack:
            screen.blit(Attack[self.attackCount//3], (self.x,self.y))
            self.attackCount += 1

        if self.ultraAttack:
            screen.blit(ultraAttack[self.ultraAttackCount//3], (self.x,self.y))
            self.ultraAttackCount += 1


        if self.isJump:
                screen.blit(Jump[self.walkCount//3], (self.x,self.y)) 
                self.walkCount += 1
        elif not(self.standing): # если не стоим, значит двигаем
            if self.left:
                screen.blit(walkLeft[self.walkCount//3], (self.x,self.y)) 
            elif self.right:
                screen.blit(walkRight[self.walkCount//3], (self.x,self.y)) 
            self.walkCount += 1
            
            
        else:
            if self.right:
                screen.blit(walkRight[7], (self.x,self.y)) 
            else:
                screen.blit(walkLeft[7], (self.x,self.y))
        self.hitbox = (self.x + 20, self.y, 28,60)
        pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)  # прорисовка хитбокса


#############################################################################

######################### Класс врага ###################################
class enemy(object):
    # загружаем анимацию врага влево или вправа
    Ronin = [pygame.image.load('Pygame_Final/Enemy/Ronin.png')]


    def __init__(self, x,y,width,height):
        self.x = x # координаты врага по х
        self.y = y # координаты врага по y
        self.width = width # ширина персонажа
        self.height = height # высота персонажа
        self.spawned = False
        self.walkCount = 0 # счётчик движения
        self.vel = 3 # коэффициент движения
        self.hitbox = (self.x + 20, self.y, 28,60) # хитбокс врага
        self.health = 10 # здоровье врага
        self.visible = True # видимость врага

    def draw(self, screen,world_shift):
        screen_x = self.x - world_shift
        screen.blit(self.Ronin[0], (screen_x, self.y))

#############################################################################
Ronin1 = enemy(2000,850, 70,70)
enemis = [
    Ronin1
]

# Создаем слои с правильными z_index (меньше - дальше, больше - ближе)
layers = [
    ParallaxLayer("Pygame_Final/parallax/desert/desert_1.png", 0, 0.2, 2),     
    ParallaxLayer("Pygame_Final/parallax/desert/desert_2.png", 0, 0.3, 5),    
    ParallaxLayer("Pygame_Final/parallax/desert/desert_3.png", 0, 0.5, 4), 
    ParallaxLayer("Pygame_Final/parallax/desert/desert_4.png", 0, 0.7, 1), 
    ParallaxLayer("Pygame_Final/parallax/desert/desert_5.png", 0, 0.9, 3),   
    ParallaxLayer("Pygame_Final/parallax/desert/desert_6.png", 0, 1.0, 0)    
]

samurai = player(200,850,70,70) # создание главного героя

# Сортируем по z_index (обязательно)
layers.sort(key=lambda layer: layer.z_index)

camera_offset = 0
world_shift = 0  # Глобальное смещение мира

def redrawGameWindow(): # функция прорисовки персонажа и фона

    for enemy in enemis:
        enemy.draw(screen, world_shift)
    samurai.draw(screen) # прорисовка героя
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Управление камерой
    keys = pygame.key.get_pressed()

    if keys[pygame.K_z] and not samurai.ultraAttack:
        samurai.ultraAttack = True
        samurai.standing = False
        samurai.left = False
        samurai.right = False
        samurai.walkCount = 0
        samurai.ultraAttackCount = 0
    
    if keys[pygame.K_SPACE] and not samurai.attack:
        samurai.attack = True
        samurai.left = False
        samurai.right = False
        samurai.standing = False
        samurai.walkCount = 0
        samurai.attackCount = 0
    
    # ДВИЖЕНИЕ - только если не атакуем
    if not samurai.attack and not samurai.ultraAttack:  
        if keys[pygame.K_LEFT] and samurai.x > samurai.vel: 
            samurai.x -= samurai.vel
            samurai.left = True
            samurai.right = False
            samurai.standing = False
            camera_offset += 3
            world_shift -= 3
        elif keys[pygame.K_RIGHT]:
            if samurai.x < 1200 - samurai.width - samurai.vel:
                samurai.x += samurai.vel
                samurai.left = False
                samurai.right = True
                samurai.standing = False 
            else:     
                camera_offset -= 3
                world_shift += 3
        else: 
            if not samurai.attack:  # не сбрасываем в стояние если атакуем
                samurai.standing = True
                samurai.walkCount = 0   


    if not(samurai.isJump):
        if keys[pygame.K_UP]:
            samurai.isJump = True
            samurai.walkCount = 0
    else:
        if samurai.jumpCount >= -10:
            samurai.y -= (samurai.jumpCount * abs(samurai.jumpCount)) * 0.4
            samurai.jumpCount -= 0.5
        else: 
            samurai.jumpCount = 10
            samurai.isJump = False
    
    # Очистка экрана
    screen.fill((0, 0, 0))
    
    # Обновляем и рисуем все слои
    for layer in layers:
        layer.update(camera_offset)
        layer.draw(screen)
    
    redrawGameWindow()
    clock.tick(60)

pygame.quit()