import pygame
import pygame.font

class ContentDisplay:
    def __init__(self, main_screen):
        self.screen = main_screen
        self.is_visible = False
        self.content = None
        
        # Dimensions de la fenêtre de contenu
        self.width = 600
        self.height = 400
        
        # Position de la fenêtre (centrée)
        screen_width, screen_height = main_screen.get_size()
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2
        
        # Initialiser la police
        pygame.font.init()
        self.font = pygame.font.Font(None, 32)
        
        # Bouton fermer
        self.close_btn = pygame.Rect(self.x + self.width - 40, self.y + 10, 30, 30)
        
    def show(self, content):
        self.is_visible = True
        self.content = content
        
    def hide(self):
        self.is_visible = False
        
    def handle_click(self, pos):
        if self.is_visible and self.close_btn.collidepoint(pos):
            self.hide()
            return True
        return False
        
    def draw(self):
        if not self.is_visible:
            return
            
        # Dessiner le fond
        content_surface = pygame.Surface((self.width, self.height))
        content_surface.fill((240, 240, 240))  # Fond gris clair
        
        # Dessiner le titre
        title = self.font.render(self.content.get('title', ''), True, (0, 0, 0))
        content_surface.blit(title, (20, 20))
        
        # Dessiner le contenu
        text = self.font.render(self.content.get('text', ''), True, (0, 0, 0))
        content_surface.blit(text, (20, 70))
        
        # Dessiner le bouton fermer
        pygame.draw.rect(content_surface, (200, 200, 200), (self.width - 40, 10, 30, 30))
        close_text = self.font.render('X', True, (0, 0, 0))
        content_surface.blit(close_text, (self.width - 35, 15))
        
        # Ajouter une bordure
        pygame.draw.rect(content_surface, (100, 100, 100), (0, 0, self.width, self.height), 2)
        
        # Afficher sur l'écran principal
        self.screen.blit(content_surface, (self.x, self.y))

class WallClickHandler:
    def __init__(self, window_width, window_height, map_data, screen):
        self.window_width = window_width
        self.window_height = window_height
        self.map_data = map_data
        self.screen = screen
        self.content_display = ContentDisplay(screen)
        
        # Contenu pour chaque mur
        self.wall_content = {
            (1, 1): {
                'title': 'Mur #1',
                'text': 'Contenu pour le mur 1'
            },
            (2, 2): {
                'title': 'Mur #2',
                'text': 'Contenu pour le mur 2'
            }
            # Ajoutez d'autres contenus ici
        }
        
    def handle_click(self, mouse_pos, ray_casting_info):
        # D'abord, vérifier si on clique sur la fenêtre de contenu
        if self.content_display.handle_click(mouse_pos):
            return True
            
        # Si la fenêtre de contenu est visible, ignorer les clics sur les murs
        if self.content_display.is_visible:
            return False
            
        if ray_casting_info:
            map_x = int(ray_casting_info['hit_x'])
            map_y = int(ray_casting_info['hit_y'])
            
            if (map_x, map_y) in self.wall_content:
                self.content_display.show(self.wall_content[(map_x, map_y)])
                return True
        return False
        
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    mouse_pos = pygame.mouse.get_pos()
                    ray_info = self.get_ray_info(mouse_pos[0], mouse_pos[1])
                    # self.handle_click(mouse_pos, ray_info)
                    
        # Dessiner la fenêtre de contenu si elle est visible
        self.content_display.draw()
        
    def get_ray_info(self, mouse_x, mouse_y):
        """
        À adapter selon votre implémentation du raycasting
        """
        # Exemple simplifié
        return {
            'hit_x': mouse_x // 64,  # Adapte à la taille de vos tuiles
            'hit_y': mouse_y // 64
        }