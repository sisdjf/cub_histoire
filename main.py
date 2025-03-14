import pygame as pg
import webbrowser
import sys
import time
from settings import *
from map import *
from player import *
from ray_casting import *
from object_rendering import *
from sprite_object import *
from sprite_object2 import *
from sprite_object3 import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(True)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.last_popup_time = 0
        self.new_game()

        self.wall_info = {
            2: {"text": "Saladin", "link": "https://www.histoire-et-civilisations.com/thematiques/moyen-age/saladin-le-sultan-qui-a-repris-jerusalem-aux-croises-83239.php"},
            3: {"text": "Croise et Troubadour", "link": "https://chanterac.fr/DocumentsPDF/Conferences%20Gareyte%20%20Flyer%20simple.pdf"},
            4: {"text": "Reconquista", "link": "https://essentiels.bnf.fr/fr/histoire/moyen-age/87b4fb85-e398-4fb1-88a9-8d1ca35a8a48-mediterranee-medievale/article/e26ce9f1-3610-4a86-92e2-68b1ec83bea7-croisades-et-reconquista"},
            5: {"text": "King Richard", "link": "https://artuk.org/discover/artworks/king-richard-i-of-england-and-soldan-saladin-97955"},
            6: {"text": "Podcast", "link": "https://www.radiofrance.fr/franceinter/podcasts/2000-ans-d-histoire/saladin-et-les-croisades-9481787"},
        }

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.static_sprite = SpriteObject(self)
        self.static_sprite2 = SpriteObjectMedieval(self)
        self.static_sprite3 = SpriteObjectEpee(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.static_sprite.update()
        self.static_sprite2.update()
        self.static_sprite3.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def draw(self):
        self.object_renderer.draw()

    def check_events(self):
        current_time = time.time()
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                # Only process click if enough time has passed since last popup
                if current_time - self.last_popup_time > 0.5:  # 500ms delay
                    a = self.raycasting.get_target()
                    self.handle_click(a['texture'])
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

    def handle_click(self, texture):
        if texture in self.wall_info:
            self.show_popup(self.wall_info[texture])

    def show_popup(self, info):
        # Clear any pending events
        pg.event.clear()
        
        popup_width, popup_height = 600, 250
        popup_rect = pg.Rect((WIDTH - popup_width) // 2, (HEIGHT - popup_height) // 2, popup_width, popup_height)

        # Draw popup
        pg.draw.rect(self.screen, (200, 200, 200), popup_rect)
        pg.draw.rect(self.screen, (0, 0, 0), popup_rect, 3)

        font = pg.font.Font(None, 36)
        text = font.render(info["text"], True, (0, 0, 0))
        text_rect = text.get_rect(center=(popup_rect.centerx, popup_rect.centery - 50))
        self.screen.blit(text, text_rect)

        if "link" in info:
            link_button_rect = pg.Rect(popup_rect.centerx - 100, popup_rect.centery + 10, 200, 40)
            pg.draw.rect(self.screen, (1, 244, 255), link_button_rect)
            pg.draw.rect(self.screen, (0, 0, 0), link_button_rect, 2)
            link_button_text = font.render("Visiter le lien", True, (255, 255, 255))
            link_button_text_rect = link_button_text.get_rect(center=link_button_rect.center)
            self.screen.blit(link_button_text, link_button_text_rect)

        ok_button_rect = pg.Rect(popup_rect.centerx - 50, popup_rect.centery + 60, 100, 40)
        pg.draw.rect(self.screen, (255, 255, 0), ok_button_rect)
        pg.draw.rect(self.screen, (0, 0, 0), ok_button_rect, 2)
        ok_button_text = font.render("OK", True, (255, 255, 255))
        ok_button_text_rect = ok_button_text.get_rect(center=ok_button_rect.center)
        self.screen.blit(ok_button_text, ok_button_text_rect)

        pg.display.flip()

        waiting_for_click = True
        while waiting_for_click:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if "link" in info and link_button_rect.collidepoint(event.pos):
                        webbrowser.open(info["link"])
                    elif ok_button_rect.collidepoint(event.pos):
                        waiting_for_click = False
        
        # Update last popup time when closing
        self.last_popup_time = time.time()
        # Clear any remaining events
        pg.event.clear()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()