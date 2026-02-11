import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

#################### Добавления анимации и музыки главному герою ########################

walkRight = [pygame.image.load('Pygame_Final/Samurai/Samurai_r1.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r2.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r3.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r4.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r5.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r6.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r7.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r8.png')]
walkLeft = [pygame.image.load('Pygame_Final/Samurai/Samurai_r1.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r2.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r3.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r4.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r5.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r6.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r7.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_r8.png')]
Jump = [pygame.image.load('Pygame_Final/Samurai/Samurai_jump1.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_jump2.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_jump3.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_jump4.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_jump5.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_jump6.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_jump7.png'),pygame.image.load('Pygame_Final/Samurai/Samurai_jump8.png')]


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
        self.left = False # загрузка анимации влево
        self.right = False # загрузка анимации вправо
        self.walkCount = 0 # счётчик движения
        self.standing = True # загрузка анимации стояния

    def draw(self,screen):
        if self.walkCount + 1 >= 24: # 8 типов движения влево/вправо * 3 фрейма = 24
            self.walkCount = 0 

        if self.isJump:
                screen.blit(Jump[self.walkCount//3], (self.x,self.y)) 
                self.walkCount += 1
        elif not(self.standing): # если не стоим, значит двигаем
            if self.left: # а если двигаемся например влево то внизу прогружаем анимацию движения влево
                screen.blit(walkLeft[self.walkCount//3], (self.x,self.y)) 
                self.walkCount += 1
            elif self.right: # тоже самое, но вправо
                screen.blit(walkRight[self.walkCount//3], (self.x,self.y)) 
                self.walkCount += 1
            
            
        else:
            if self.right: # начинаем движение вправо с 7 индекса
                screen.blit(walkRight[7], (self.x,self.y)) 
            else: # начинаем движение влево с 7 индекса
                screen.blit(walkLeft[7], (self.x,self.y))
        self.hitbox = (self.x + 20, self.y, 28,60)
        pygame.draw.rect(screen, (255,0,0), self.hitbox, 2)  # прорисовка хитбокса


#############################################################################

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

    samurai.draw(screen) # прорисовка героя
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Управление камерой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and samurai.x > samurai.vel: 
        samurai.x -= samurai.vel
        samurai.left = True
        samurai.right = False
        samurai.standing = False
        camera_offset += 3
        world_shift -= 3
    elif keys[pygame.K_RIGHT]:
        samurai.x += samurai.vel
        samurai.left = False
        samurai.right = True
        samurai.standing = False  
        camera_offset -= 3
        world_shift += 3
    else: 
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