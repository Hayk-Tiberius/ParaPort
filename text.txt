import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()

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

# Создаем слои с правильными z_index (меньше - дальше, больше - ближе)
layers = [
    ParallaxLayer("Pygame_Final/parallax/desert/desert_1.png", 0, 0.2, 2),     
    ParallaxLayer("Pygame_Final/parallax/desert/desert_2.png", 0, 0.3, 5),    
    ParallaxLayer("Pygame_Final/parallax/desert/desert_3.png", 0, 0.5, 4), 
    ParallaxLayer("Pygame_Final/parallax/desert/desert_4.png", 0, 0.7, 1), 
    ParallaxLayer("Pygame_Final/parallax/desert/desert_5.png", 0, 0.9, 3),   
    ParallaxLayer("Pygame_Final/parallax/desert/desert_6.png", 0, 1.0, 0)    
]

# Сортируем по z_index (обязательно)
layers.sort(key=lambda layer: layer.z_index)

camera_offset = 0
world_shift = 0  # Глобальное смещение мира

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Управление камерой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_offset += 3
        world_shift -= 3
    if keys[pygame.K_RIGHT]:
        camera_offset -= 3
        world_shift += 3
    
    # Очистка экрана
    screen.fill((0, 0, 0))
    
    # Обновляем и рисуем все слои
    for layer in layers:
        layer.update(camera_offset)
        layer.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()