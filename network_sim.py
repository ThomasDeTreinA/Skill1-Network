import pygame
import math
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WIDTH, HEIGHT = 1000, 700
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 50)
GRAY = (150, 150, 150)
CYAN = (100, 255, 255)

# --- TAAL SYSTEEM ---
current_lang = 'nl' # Standaard Nederlands

LANGS = {
    'nl': {
        'play': 'START SPEL',
        'quit': 'AFSLUITEN',
        'select_lang': 'KIES JE TAAL',
        'back': 'Terug',
        'go': 'Go!',
        'enter_house': 'HUIS BETREDEN',
        'to_world': 'NAAR WERELDKAART',
        'ip_settings': 'IP Instellingen',
        'web_browsing': 'Web Browsing',
        'terminal': 'Terminal',
        'restart': 'Herstarten',
        'reset': 'Factory Reset',
        'save': 'Opslaan',
        'select_cable': 'Kies Kabel:',
        'cat5_label': 'Cat 5 Kabel',
        'cat5e_label': 'Cat 5e Kabel',
        'wan_label': 'WAN Fiber',
        'error_len': 'Kabel te lang!',
        'error_ip': 'Fout: Router IP of Subnet incorrect.',
        'error_route': 'Fout: Geen route naar een Router.',
        'error_no_ip': 'Fout: PC heeft geen IP-adres.',
        'error_404': 'Fout: 404 Website niet gevonden.',
        'connecting': 'Verbinding maken...',
        'free_mode': 'Vrij Spel / Sandbox Mode',
        'intro_title': 'Welkom bij de Netwerk Simulator!',
        'intro_body': [
            "In deze game leer je de basisprincipes van netwerken stap voor stap.",
            "Je bouwt je eigen lokale netwerk (LAN), verbindt apparaten via fysieke",
            "kabels, en leert hoe Routers je naar het echte internet tillen.",
            "",
            "Wat kun je allemaal doen?",
            "- Plaats PC's, Laptops, Switches en Routers (linksboven).",
            "- Verbind apparaten met Cat 5 of snellere Cat 5e kabels (rechts).",
            "- Configureer IP-adressen via het besturingssysteem van elk apparaat.",
            "- Test je netwerk door data-pakketjes of webverkeer te sturen!",
            "",
            "Klik hier ergens in het vak om aan Level 1 te beginnen!"
        ],
        'l1_exp_mouse': "TIP: Houd de linkermuisknop ingedrukt om kabels te trekken!",
        'trans_zoom_in': "Inzoomen op...",
        'trans_zoom_out': "Uitzoomen naar de buitenwereld...",
        'trans_back_world': "Terug naar het overzicht...",
        'spacebar': 'SPATIE'
    },
    'en': {
        'play': 'START GAME',
        'quit': 'QUIT',
        'select_lang': 'CHOOSE YOUR LANGUAGE',
        'back': 'Back',
        'go': 'Go!',
        'enter_house': 'ENTER HOUSE',
        'to_world': 'TO WORLD MAP',
        'ip_settings': 'IP Settings',
        'web_browsing': 'Web Browsing',
        'terminal': 'Terminal',
        'restart': 'Restart',
        'reset': 'Factory Reset',
        'save': 'Save',
        'select_cable': 'Choose Cable:',
        'cat5_label': 'Cat 5 Cable',
        'cat5e_label': 'Cat 5e Cable',
        'wan_label': 'WAN Fiber',
        'error_len': 'Cable too long!',
        'error_ip': 'Error: Router IP or Subnet incorrect.',
        'error_route': 'Error: No route to a Router.',
        'error_no_ip': 'Error: PC has no IP address.',
        'error_404': 'Error: 404 Website not found.',
        'connecting': 'Connecting...',
        'free_mode': 'Free Play / Sandbox Mode',
        'intro_title': 'Welcome to the Network Simulator!',
        'intro_body': [
            "In this game you will learn the basics of networking step by step.",
            "Build your own local network (LAN), connect devices with physical",
            "cables, and learn how Routers take you to the real internet.",
            "",
            "What can you do?",
            "- Place PCs, Laptops, Switches and Routers (top left).",
            "- Connect devices with Cat 5 or faster Cat 5e cables (right).",
            "- Configure IP addresses via each device's OS.",
            "- Test your network by sending data packets or web traffic!",
            "",
            "Click anywhere in this box to start Level 1!"
        ],
        'l1_exp_mouse': "TIP: Hold left mouse button to drag and connect cables!",
        'trans_zoom_in': "Zooming in on...",
        'trans_zoom_out': "Zooming out to the world...",
        'trans_back_world': "Back to overview...",
        'spacebar': 'SPACE'
    },
    'fr': {
        'play': 'COMMENCER',
        'quit': 'QUITTER',
        'select_lang': 'CHOISISSEZ VOTRE LANGUE',
        'back': 'Retour',
        'go': 'Go!',
        'enter_house': 'ENTRER MAISON',
        'to_world': 'CARTE DU MONDE',
        'ip_settings': 'Paramètres IP',
        'web_browsing': 'Navigation Web',
        'terminal': 'Terminal',
        'restart': 'Redémarrer',
        'reset': 'Réinitialiser',
        'save': 'Sauvegarder',
        'select_cable': 'Choisir Câble:',
        'cat5_label': 'Câble Cat 5',
        'cat5e_label': 'Câble Cat 5e',
        'wan_label': 'Fibre WAN',
        'error_len': 'Câble trop long!',
        'error_ip': 'Erreur: IP du routeur ou masque incorrect.',
        'error_route': 'Erreur: Pas de route vers un routeur.',
        'error_no_ip': "Erreur: Le PC n'a pas d'adresse IP.",
        'error_404': 'Erreur: 404 Site non trouvé.',
        'connecting': 'Connexion en cours...',
        'free_mode': 'Mode libre / Bac à sable',
        'intro_title': 'Bienvenue dans le Simulateur Réseau!',
        'intro_body': [
            "Dans ce jeu, vous apprendrez les bases du réseau étape par étape.",
            "Créez votre propre LAN, connectez des appareils avec des câbles",
            "physiques et découvrez comment les routeurs ouvrent l'accès à Internet.",
            "",
            "Que pouvez-vous faire?",
            "- Placez des PC, portables, switchs et routeurs (en haut à gauche).",
            "- Connectez avec des câbles Cat 5 ou Cat 5e plus rapides (à droite).",
            "- Configurez les adresses IP via le système de chaque appareil.",
            "- Testez votre réseau en envoyant des paquets ou du trafic web!",
            "",
            "Cliquez n'importe où dans ce cadre pour commencer le niveau 1!"
        ],
        'l1_exp_mouse': "ASTUCE: Maintenez le bouton gauche de la souris pour glisser et connecter!",
        'trans_zoom_in': "Zoom sur...",
        'trans_zoom_out': "Retour au monde...",
        'trans_back_world': "Retour à l'aperçu...",
        'spacebar': 'ESPACE'
    }
}

def get_text(key):
    return LANGS.get(current_lang, LANGS['nl']).get(key, key)

CABLES = {
    'Cat 5': {'color': GREEN, 'max_dist': 400, 'max_m': 100},
    'Cat 5e': {'color': BLUE, 'max_dist': 800, 'max_m': 200},
    'WAN Fiber': {'color': YELLOW, 'max_dist': 2000, 'max_m': 10000},
    'Wi-Fi': {'color': CYAN, 'max_dist': 250, 'max_m': 30}
}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Network Simulation")
font = pygame.font.SysFont("Arial", 20, bold=True)
mission_font = pygame.font.SysFont("Arial", 24, bold=True)
small_font = pygame.font.SysFont("Arial", 16)

bg_img = None
try:
    bg_img = pygame.image.load(os.path.join(BASE_DIR, "background.png")).convert()
    bg_img = pygame.transform.smoothscale(bg_img, (WIDTH, HEIGHT))
except Exception as e:
    pass

gc_img = None
try:
    gc_img = pygame.image.load(os.path.join(BASE_DIR, "GreenCircle.png")).convert_alpha()
except Exception as e:
    pass

arrow_img = None
try:
    img = pygame.image.load(os.path.join(BASE_DIR, "arrow.png")).convert_alpha()
    arrow_img = pygame.transform.smoothscale(img, (80, 80))
except Exception as e:
    pass

# Global Game State
devices = []
connections = []
packets = []
mission_sys = None
current_mode = 'PC' 
current_cable = 'Cat 5'
sm = None

data_img = None
try:
    img = pygame.image.load(os.path.join(BASE_DIR, "data.png")).convert_alpha()
    data_img = pygame.transform.smoothscale(img, (35, 35))
except Exception as e:
    pass

tm_img = None
try:
    img = pygame.image.load(os.path.join(BASE_DIR, "thomasmore.png")).convert_alpha()
    tm_img = pygame.transform.smoothscale(img, (500, 270))
except Exception as e:
    try:
        img = pygame.image.load(os.path.join(BASE_DIR, "thomasmore.jpg")).convert_alpha()
        tm_img = pygame.transform.smoothscale(img, (500, 270))
    except Exception as e2:
        pass

def load_icon(filename, size=(50, 50)):
    if '.' not in filename:
        for ext in ['.png', '.jpg', '.jpeg', '.webp']:
            filepath = os.path.join(BASE_DIR, filename + ext)
            if os.path.exists(filepath):
                filename += ext
                break
                
    filepath = os.path.join(BASE_DIR, filename)
    try:
        img = pygame.image.load(filepath).convert_alpha()
        return pygame.transform.smoothscale(img, size)
    except Exception as e:
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(surf, WHITE, (size[0]//2, size[1]//2), size[0]//2)
        return surf

ICONS = {
    'PC': load_icon("pc.png"),
    'Laptop': load_icon("laptop.webp"),
    'Switch': load_icon("switch.png"),
    'Router': load_icon("router.webp"),
    'DELETE': load_icon("delete"),
    'House1': load_icon("huis1.png", size=(80, 80)),
    'House2': load_icon("huis2.png", size=(80, 80)),
}

EXT_ICONS = {}
def get_ext_icon(name):
    if name not in EXT_ICONS:
        filename = name
        if '.' not in filename:
            for ext in ['.png', '.jpg']:
                if os.path.exists(os.path.join(BASE_DIR, filename + ext)):
                    filename += ext
                    break
        try:
            img = pygame.image.load(os.path.join(BASE_DIR, filename)).convert_alpha()
            EXT_ICONS[name] = pygame.transform.smoothscale(img, (60, 60))
        except:
            surf = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.rect(surf, GRAY, (0,0,60,60))
            EXT_ICONS[name] = surf
    return EXT_ICONS[name]

class Device:
    device_count = 0
    def __init__(self, x, y, device_type, decorative=False):
        self.x = x
        self.y = y
        self.type = device_type
        self.decorative = decorative
        self.id = Device.device_count + 1
        if not decorative: Device.device_count += 1
        self.radius = 25
        self.ip = ""
        self.subnet = ""

    @property
    def cable_c(self):
        # Return a slightly offset visual center point for cables to originate from
        if self.type == 'Router':
            return (self.x, self.y + 10)
        return (self.x, self.y)
        
    def cable_dist(self, angle):
        # Return the bounding intersection distance based on device type
        if self.type == 'Router':
            return 17 / max(abs(math.cos(angle)), abs(math.sin(angle)))
        elif self.type == 'PC':
            return 18 / max(abs(math.cos(angle)), abs(math.sin(angle)))
        elif self.type in ('House1', 'House2'):
            return 40 / max(abs(math.cos(angle)), abs(math.sin(angle))) + 2
        else:
            return 25 / max(abs(math.cos(angle)), abs(math.sin(angle))) + 2

    def draw(self, surface, current_scene='Level1'):
        if self.type == 'PC': label = f"PC {self.id}"
        elif self.type == 'Laptop': label = f"LAP {self.id}"
        elif self.type == 'Switch': label = f"SW {self.id}"
        elif self.type == 'House1': 
            label = ("Huis 1" if current_lang == 'nl' else "House 1" if current_lang == 'en' else "Maison 1") if not self.decorative else f"Huis {self.id}"
        elif self.type == 'House2': 
            label = ("Huis 2" if current_lang == 'nl' else "House 2" if current_lang == 'en' else "Maison 2") if not self.decorative else f"Huis {self.id}"
        else: label = f"RT {self.id}"
            
        icon = ICONS.get(self.type)
        if icon:
            rect = icon.get_rect(center=(self.x, self.y))
            surface.blit(icon, rect.topleft)
        else:
            pygame.draw.circle(surface, GRAY, (self.x, self.y), self.radius)
            pygame.draw.circle(surface, WHITE, (self.x, self.y), self.radius, 2)
        
        text = font.render(label, True, WHITE)
        surface.blit(text, (self.x - text.get_width()//2, self.y - self.radius - 25))
        
        # Wi-Fi connecting animation (blinking arcs to the LEFT of laptop)
        if self.type == 'Laptop' and mission_sys.wifi_timer > 0:
            if (pygame.time.get_ticks() // 250) % 2 == 0:
                for i in range(3):
                    r = 15 + i*8
                    rect = pygame.Rect(self.x - self.radius - 40 - r, self.y - r, r*2, r*2)
                    pygame.draw.arc(surface, CYAN, rect, 3*math.pi/4, 5*math.pi/4, 3) 
        
        # Highlight Huis 1 & 2 in World Map for mission
        if current_scene == 'World' and self.type in ['House1', 'House2'] and not self.decorative:
            # Check if mission is active and NO WAN connection yet
            m = mission_sys.get_current() if mission_sys else None
            if m and m.type in ["L3_CONNECT_WAN", "L3_SEND_P_WAN"]:
                # Check for WAN connection
                connected = False
                for c in connections:
                    if (c.d1.type == 'House1' and c.d2.type == 'House2') or (c.d1.type == 'House2' and c.d2.type == 'House1'):
                        if c.cable_type == 'WAN Fiber':
                            connected = True
                            break
                if not connected:
                    s = abs(math.sin(pygame.time.get_ticks() * 0.005))
                    pygame.draw.circle(surface, YELLOW, (self.x, self.y), self.radius + 10 + s*5, 3)
                    # Arrow above
                    ay = self.y - self.radius - 50 - s*10
                    pygame.draw.polygon(surface, YELLOW, [(self.x, ay+20), (self.x-10, ay), (self.x+10, ay)])
                    t = font.render("HUIS 2 (Target)", True, YELLOW)
                    surface.blit(t, (self.x - t.get_width()//2, ay - 25))
        
        if self.ip:
            ip_txt = small_font.render(self.ip, True, CYAN)
            surface.blit(ip_txt, (self.x - ip_txt.get_width()//2, self.y + self.radius + 5))

class TextInput:
    def __init__(self, x, y, w, h, default=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = default
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                pass
            else:
                if len(self.text) < 30:
                    self.text += event.unicode

    def draw(self, surface):
        color = BLUE if self.active else GRAY
        pygame.draw.rect(surface, WHITE, self.rect)
        pygame.draw.rect(surface, color, self.rect, 2)
        txt = font.render(self.text, True, BLACK)
        surface.blit(txt, (self.rect.x + 5, self.rect.y + 2))

class Connection:
    def __init__(self, d1, d2, cable_type='Cat 5'):
        self.d1 = d1
        self.d2 = d2
        self.cable_type = cable_type
        self.update_validity()

    def update_validity(self):
        c1x, c1y = self.d1.cable_c
        c2x, c2y = self.d2.cable_c
        self.distance = math.hypot(c1x - c2x, c1y - c2y)
        self.is_valid = self.distance <= CABLES[self.cable_type]['max_dist']

    def draw(self, surface):
        # Don't draw Wi-Fi line while connecting animation is playing
        if self.cable_type == 'Wi-Fi' and mission_sys.wifi_timer > 0:
            return

        color = CABLES[self.cable_type]['color'] if self.is_valid else RED
        
        c1x, c1y = self.d1.cable_c
        c2x, c2y = self.d2.cable_c
        
        angle = math.atan2(c2y - c1y, c2x - c1x)
        d1_dist = self.d1.cable_dist(angle)
        d2_dist = self.d2.cable_dist(angle)
        
        if self.distance > (d1_dist + d2_dist):
            start_x = c1x + math.cos(angle) * d1_dist
            start_y = c1y + math.sin(angle) * d1_dist
            end_x = c2x - math.cos(angle) * d2_dist
            end_y = c2y - math.sin(angle) * d2_dist
            
            if self.cable_type == 'Wi-Fi':
                # Draw 3-4 arcs (radio waves) centered on the midpoint
                mid_x, mid_y = (start_x + end_x) / 2, (start_y + end_y) / 2
                angle = math.atan2(end_y - start_y, end_x - start_x)
                perp_angle = angle + math.pi/2
                
                # Draw small circles or arcs repeating along the line
                # Let's draw 3 arcs in the middle of the connection
                for i in range(1, 4):
                    r = i * 8
                    # Draw arc segment
                    points = []
                    for a in range(-30, 31, 10):
                        rad = math.radians(a)
                        px = mid_x + math.cos(angle + rad) * r
                        py = mid_y + math.sin(angle + rad) * r
                        points.append((px, py))
                    if len(points) > 1:
                        pygame.draw.lines(surface, color, False, points, 2)
                
                # Also a small dot in the center
                pygame.draw.circle(surface, color, (int(mid_x), int(mid_y)), 3)
            else:
                pygame.draw.line(surface, color, (start_x, start_y), (end_x, end_y), 4)

class PacketPath:
    def __init__(self, path, speed=4.0):
        self.path = path
        self.target_pc = path[-1]
        self.curr_idx = 0
        self.progress = 0.0
        self.speed = speed
        self.reached = False
        self.dist = 0
        self.pause_frames = 0
        self.update_dist()

    def update_dist(self):
        if self.curr_idx < len(self.path) - 1:
            c1x, c1y = self.path[self.curr_idx].cable_c
            c2x, c2y = self.path[self.curr_idx+1].cable_c
            self.dist = math.hypot(c1x - c2x, c1y - c2y)
        else:
            self.dist = 0

    def update(self):
        if self.reached: return
        
        if self.pause_frames > 0:
            self.pause_frames -= 1
            return
            
        if self.dist == 0:
            self.progress = 1.0
        else:
            self.progress += self.speed / self.dist
            
        if self.progress >= 1.0:
            self.progress = 0.0
            self.curr_idx += 1
            if self.curr_idx >= len(self.path) - 1:
                self.reached = True
            else:
                self.pause_frames = 12 # 0.2s at 60fps
                self.update_dist()

    def draw(self, surface):
        if self.reached or self.curr_idx >= len(self.path) - 1: return
        
        c1x, c1y = self.path[self.curr_idx].cable_c
        c2x, c2y = self.path[self.curr_idx+1].cable_c
        
        x = c1x + (c2x - c1x) * self.progress
        y = c1y + (c2y - c1y) * self.progress
        
        if data_img:
            rect = data_img.get_rect(center=(int(x), int(y)))
            surface.blit(data_img, rect.topleft)
        else:
            pygame.draw.circle(surface, YELLOW, (int(x), int(y)), 10)
            pygame.draw.circle(surface, BLACK, (int(x), int(y)), 10, 2)

class SceneManager:
    def __init__(self):
        self.scenes = {
            'Start': {'devices': [], 'connections': [], 'packets': []},
            'Level1': {'devices': [], 'connections': [], 'packets': []},
            'House1': {'devices': [], 'connections': [], 'packets': []},
            'House2': {'devices': [], 'connections': [], 'packets': []},
            'World': {'devices': [], 'connections': [], 'packets': []}
        }
        self.current = 'Start'
        self.transition_alpha = 0
        self.transition_state = "NONE" # NONE, FADE_OUT, FADE_IN
        self.target_scene = None
        self.trans_text = ""
        
    def start_transition(self, target, text):
        self.transition_state = "FADE_OUT"
        self.target_scene = target
        self.trans_text = text

    def get_current(self):
        return self.scenes[self.current]

    def draw_start_screen(self, surface):
        surface.fill((30, 30, 40))
        # Title
        title_font = pygame.font.SysFont('Arial', 60, bold=True)
        t_surf = title_font.render("NETWORK SIMULATOR", True, CYAN)
        surface.blit(t_surf, (WIDTH//2 - t_surf.get_width()//2, 100))
        
        # Subtitle / Select Lang
        lang_text = get_text('select_lang')
        l_surf = font.render(lang_text, True, WHITE)
        surface.blit(l_surf, (WIDTH//2 - l_surf.get_width()//2, 220))
        
        # Language Buttons
        langs = [('nl', 'NEDERLANDS'), ('en', 'ENGLISH'), ('fr', 'FRANÇAIS')]
        bx = WIDTH//2 - 250
        for code, name in langs:
            rect = pygame.Rect(bx, 260, 150, 40)
            color = CYAN if current_lang == code else (60, 60, 70)
            pygame.draw.rect(surface, color, rect, border_radius=5)
            pygame.draw.rect(surface, WHITE, rect, 2, border_radius=5)
            txt = font.render(name, True, WHITE)
            surface.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
            bx += 175
            
        # Play / Quit Buttons
        btn_play = pygame.Rect(WIDTH//2 - 100, 400, 200, 60)
        pygame.draw.rect(surface, (100, 200, 100), btn_play, border_radius=10)
        pygame.draw.rect(surface, WHITE, btn_play, 3, border_radius=10)
        p_txt = font.render(get_text('play'), True, WHITE)
        surface.blit(p_txt, (btn_play.centerx - p_txt.get_width()//2, btn_play.centery - p_txt.get_height()//2))
        
        btn_quit = pygame.Rect(WIDTH//2 - 100, 500, 200, 60)
        pygame.draw.rect(surface, (200, 100, 100), btn_quit, border_radius=10)
        pygame.draw.rect(surface, WHITE, btn_quit, 3, border_radius=10)
        q_txt = font.render(get_text('quit'), True, WHITE)
        surface.blit(q_txt, (btn_quit.centerx - q_txt.get_width()//2, btn_quit.centery - q_txt.get_height()//2))

    def update(self):
        if self.transition_state == "FADE_OUT":
            self.transition_alpha += 5
            if self.transition_alpha >= 255:
                self.current = self.target_scene
                self.transition_state = "FADE_IN"
        elif self.transition_state == "FADE_IN":
            self.transition_alpha -= 5
            if self.transition_alpha <= 0:
                self.transition_state = "NONE"

    def draw(self, surface):
        if self.transition_alpha > 0:
            s = pygame.Surface((1000, 700), pygame.SRCALPHA)
            s.fill((0,0,0, min(255, max(0, self.transition_alpha))))
            if self.transition_alpha > 100:
                t = font.render(self.trans_text, True, (255,255,255))
                s.blit(t, (500 - t.get_width()//2, 350))
            surface.blit(s, (0,0))

class Mission:
    def __init__(self, text, m_type, target_pos=None, dev_type=None, radius=50):
        self.text = text
        self.type = m_type 
        self.target_pos = target_pos
        self.dev_type = dev_type
        self.radius = radius

class MissionSystem:
    def __init__(self):
        self.level = 1
        self.fail_msg = ""
        self.fail_timer = 0
        self.surf_success = False
        self.popup_text = ""
        self.packets_delivered = 0
        self.overlay_alpha = 0
        self.wifi_timer = 0
        self.setup_level()
        
    def setup_level(self):
        L = current_lang
        if self.level == 1:
            if L == 'en':
                self.missions = [
                    Mission("Read the start introduction on the screen.", "INTRO"),
                    Mission("This is a PC. Use it for fixed workstations.\nClick to continue.", "L1_EXP_PC", target_pos=(51, 40)),
                    Mission("This is a Laptop. Can connect via cable or wireless!\nClick to continue.", "L1_EXP_LAP", target_pos=(121, 40)),
                    Mission("This is a Switch. Use it to connect multiple devices.\nClick to continue.", "L1_EXP_SW", target_pos=(191, 40)),
                    Mission("This is a Router. The gateway to the rest of the world!\nClick to continue.", "L1_EXP_RT", target_pos=(261, 40)),
                    Mission("Mission 1: Place a PC in the left circle.", "PLACE", target_pos=(100, 350), dev_type="PC"),
                    Mission("Mission 2: Place a 2nd PC nearby.", "PLACE", target_pos=(300, 350), dev_type="PC"),
                    Mission("TIP: Hold the left mouse button to drag and connect cables!\nClick to continue.", "L1_EXP_MOUSE"),
                    Mission("Mission 3: Connect the two PCs (Cat 5 is 100m max).", "CONNECT"),
                    Mission("Mission 4: Place a 3rd PC far away.", "PLACE", target_pos=(750, 350), dev_type="PC"),
                    Mission("Mission 5: Connect PC2 and PC3.", "TRY_CONNECT"),
                    Mission("Oops! Cable too short. Read the explanation.", "EXPLANATION_CAT5"),
                    Mission("Mission 6: Pick the Cat 5e cable on the right.", "PICK_CAT5E"),
                    Mission("Mission 7: Connect PC2 and PC3 with the Cat 5e cable.", "CONNECT_CAT5E"),
                    Mission("Mission 8: Press SPACE (or data icon) to send data!", "PACKET"),
                    Mission("Level 1 complete! Read the explanation and click 'Next'.", "EXPLANATION_1")
                ]
            elif L == 'fr':
                self.missions = [
                    Mission("Lisez l'introduction au début sur l'écran.", "INTRO"),
                    Mission("C'est un PC. Utilisez-le pour les postes fixes.\nCliquez pour continuer.", "L1_EXP_PC", target_pos=(51, 40)),
                    Mission("C'est un portable. Connexion filaire ou sans fil !\nCliquez pour continuer.", "L1_EXP_LAP", target_pos=(121, 40)),
                    Mission("C'est un Switch. Pour connecter plusieurs appareils.\nCliquez pour continuer.", "L1_EXP_SW", target_pos=(191, 40)),
                    Mission("C'est un Routeur. La porte vers le reste du monde !\nCliquez pour continuer.", "L1_EXP_RT", target_pos=(261, 40)),
                    Mission("Mission 1: Placez un PC dans le cercle gauche.", "PLACE", target_pos=(100, 350), dev_type="PC"),
                    Mission("Mission 2: Placez un 2ème PC à proximité.", "PLACE", target_pos=(300, 350), dev_type="PC"),
                    Mission("ASTUCE: Maintenez le bouton gauche pour tirer des câbles !\nCliquez pour continuer.", "L1_EXP_MOUSE"),
                    Mission("Mission 3: Connectez les deux PC (Cat 5 est 100m max).", "CONNECT"),
                    Mission("Mission 4: Placez un 3ème PC au loin.", "PLACE", target_pos=(750, 350), dev_type="PC"),
                    Mission("Mission 5: Connectez PC2 et PC3.", "TRY_CONNECT"),
                    Mission("Oups ! Câble trop court. Lisez l'explication.", "EXPLANATION_CAT5"),
                    Mission("Mission 6: Prenez le câble Cat 5e à droite.", "PICK_CAT5E"),
                    Mission("Mission 7: Connectez PC2 et PC3 avec le câble Cat 5e.", "CONNECT_CAT5E"),
                    Mission("Mission 8: Appuyez sur ESPACE pour envoyer des données !", "PACKET"),
                    Mission("Niveau 1 terminé ! Lisez l'explication et cliquez sur 'Suivant'.", "EXPLANATION_1")
                ]
            else: # nl
                self.missions = [
                    Mission("Lees de start-introductie op het scherm.", "INTRO"),
                    Mission("Dit is een PC. Gebruik deze voor vaste werkstations.\nKlik om door te gaan.", "L1_EXP_PC", target_pos=(51, 40)),
                    Mission("Dit is een Laptop. Kan zowel met kabel als draadloos!\nKlik om door te gaan.", "L1_EXP_LAP", target_pos=(121, 40)),
                    Mission("Dit is een Switch. Hiermee verbind je meerdere apparaten.\nKlik om door te gaan.", "L1_EXP_SW", target_pos=(191, 40)),
                    Mission("Dit is een Router. De poort naar de rest van de wereld!\nKlik om door te gaan.", "L1_EXP_RT", target_pos=(261, 40)),
                    Mission("Missie 1: Plaats een PC in de linkercirkel.", "PLACE", target_pos=(100, 350), dev_type="PC"),
                    Mission("Missie 2: Plaats een 2e PC dichtbij.", "PLACE", target_pos=(300, 350), dev_type="PC"),
                    Mission("TIP: Houd de linkermuisknop ingedrukt om kabels te trekken!\nKlik om door te gaan.", "L1_EXP_MOUSE"),
                    Mission("Missie 3: Verbind de twee PC's (Cat 5 is 100m max).", "CONNECT"),
                    Mission("Missie 4: Plaats een 3e PC ver weg.", "PLACE", target_pos=(750, 350), dev_type="PC"),
                    Mission("Missie 5: Verbind PC2 en PC3.", "TRY_CONNECT"),
                    Mission("Oeps! Kabel te kort. Lees de uitleg.", "EXPLANATION_CAT5"),
                    Mission("Missie 6: Pak rechts de Cat 5e kabel.", "PICK_CAT5E"),
                    Mission("Missie 7: Verbind PC2 en PC3 met de Cat 5e kabel.", "CONNECT_CAT5E"),
                    Mission("Missie 8: Druk op SPATIE (of data icoon) om data te sturen!", "PACKET"),
                    Mission("Level 1 voltooid! Lees de uitleg en klik op 'Volgende'.", "EXPLANATION_1")
                ]
        elif self.level == 2:
            if L == 'en':
                self.missions = [
                    Mission("Level 2: Place a Router in the center of the network.", "PLACE", target_pos=(500, 200), dev_type="Router"),
                    Mission("Click the Router. In IP Settings set IP: 192.168.1.1, Subnet: 255.255.255.0\nThen click Save.", "CONF_ROUTER"),
                    Mission("Good! Now close the window by clicking the red dot top left.", "CLOSE_WINDOW"),
                    Mission("Place a PC below left of the Router.", "PLACE", target_pos=(300, 400), dev_type="PC"),
                    Mission("Connect the PC to the Router.", "CONNECT_R"),
                    Mission("Click the PC. In IP Settings set IP: 192.168.1.2, Subnet: 255.255.255.0\nThen click Save.", "CONF_PC"),
                    Mission("Click 'Back' at the top, then choose 'Web Browsing'.\nType 'www.thomasmore.be' and click Go!", "SURF"),
                    Mission("Close the browser window by clicking the red dot.", "CLOSE_WINDOW"),
                    Mission("Well done! Read the explanation and go to Level 3.", "EXPLANATION_2")
                ]
            elif L == 'fr':
                self.missions = [
                    Mission("Niveau 2: Placez un routeur au centre du réseau.", "PLACE", target_pos=(500, 200), dev_type="Router"),
                    Mission("Cliquez sur le routeur. Réglez IP: 192.168.1.1, Masque: 255.255.255.0\nCliquez sur Sauvegarder.", "CONF_ROUTER"),
                    Mission("Bien ! Fermez la fenêtre en cliquant sur le point rouge.", "CLOSE_WINDOW"),
                    Mission("Placez un PC en bas à gauche du routeur.", "PLACE", target_pos=(300, 400), dev_type="PC"),
                    Mission("Connectez le PC au routeur.", "CONNECT_R"),
                    Mission("Cliquez sur le PC. Réglez IP: 192.168.1.2, Masque: 255.255.255.0\nCliquez sur Sauvegarder.", "CONF_PC"),
                    Mission("Cliquez sur 'Retour', puis 'Navigation Web'.\nTapez 'www.thomasmore.be' et Go !", "SURF"),
                    Mission("Fermez le navigateur en cliquant sur le point rouge.", "CLOSE_WINDOW"),
                    Mission("Bravo ! Lisez l'explication et passez au niveau 3.", "EXPLANATION_2")
                ]
            else: # nl
                self.missions = [
                    Mission("Level 2: Plaats een Router centraal in het netwerk.", "PLACE", target_pos=(500, 200), dev_type="Router"),
                    Mission("Klik op de Router. In IP Instellingen zet IP: 192.168.1.1, Subnet: 255.255.255.0\nKlik daarna op Opslaan.", "CONF_ROUTER"),
                    Mission("Goed zo! Sluit nu het venster door op het rode bolletje linksboven te klikken.", "CLOSE_WINDOW"),
                    Mission("Plaats een PC links onder de Router.", "PLACE", target_pos=(300, 400), dev_type="PC"),
                    Mission("Verbind de PC met de Router.", "CONNECT_R"),
                    Mission("Klik op de PC. In IP Instellingen zet IP: 192.168.1.2, Subnet: 255.255.255.0\nKlik daarna op Opslaan.", "CONF_PC"),
                    Mission("Klik bovenaan op 'Terug', kies dan 'Web Browsing'.\nTyp 'www.thomasmore.be' en klik Go!", "SURF"),
                    Mission("Sluit het browser venster door op het rode bolletje te klikken.", "CLOSE_WINDOW"),
                    Mission("Goed gedaan! Lees de uitleg en ga naar Level 3.", "EXPLANATION_2")
                ]
        elif self.level == 3:
            global sm
            if 'sm' in globals() and sm is not None:
                sm.current = 'House1'
                for s in sm.scenes.values():
                    s['devices'].clear()
                    s['connections'].clear()
                    s['packets'].clear()
            
            if L == 'en':
                self.missions = [
                    Mission("L3: Place a Router and a Switch in House 1.", "L3_PLACE_RS"),
                    Mission("Place 2 PCs around the Switch.", "L3_PLACE_PC"),
                    Mission("Connect: Router->Switch and Switch->2x PC.", "L3_CONNECT_LAN"),
                    Mission("Place a Laptop near the Router's blue circle.\nIt connects wirelessly (Wi-Fi)!", "L3_WIFI"),
                    Mission("House 1 is ready! Zooming out to the World Map...", "L3_TO_WORLD_1"),
                    Mission("This is the World Map. Click this box to enter House 2.", "L3_WORLD_1"),
                    Mission("House 2: Place a Router, Switch, 1 PC.\nConnect: Router->Switch and Switch->PC.", "L3_BUILD_H2"),
                    Mission("House 2 complete! Zooming out to World Map...", "L3_TO_WORLD_2"),
                    Mission("World Map: Choose the WAN Fiber cable on the right.", "L3_PICK_WAN"),
                    Mission("On the map: Connect House 1 and House 2 with the WAN cable!", "L3_CONNECT_WAN"),
                    Mission("Congratulations! Test the connection by sending a packet\nbetween the houses (Space)", "L3_SEND_P_WAN"),
                    Mission("WAN Network Complete! You are now in Free Mode.", "EXPLANATION_FIN"),
                    Mission("Level 3 Complete! You are now in Free Mode.", "DONE")
                ]
            elif L == 'fr':
                self.missions = [
                    Mission("L3: Placez un routeur et un switch dans la Maison 1.", "L3_PLACE_RS"),
                    Mission("Placez 2 PC autour du switch.", "L3_PLACE_PC"),
                    Mission("Connectez : Routeur->Switch et Switch->2x PC.", "L3_CONNECT_LAN"),
                    Mission("Placez un portable près du cercle bleu du routeur.\nIl se connecte sans fil (Wi-Fi) !", "L3_WIFI"),
                    Mission("Maison 1 prête ! Retour à la carte du monde...", "L3_TO_WORLD_1"),
                    Mission("C'est la carte du monde. Cliquez ici pour entrer Maison 2.", "L3_WORLD_1"),
                    Mission("Maison 2: Placez routeur, switch, 1 PC.\nConnectez : Routeur->Switch et Switch->PC.", "L3_BUILD_H2"),
                    Mission("Maison 2 terminée ! Retour à la carte...", "L3_TO_WORLD_2"),
                    Mission("Carte : Choisissez le câble Fibre WAN à droite.", "L3_PICK_WAN"),
                    Mission("Connectez Maison 1 et Maison 2 avec le câble WAN !", "L3_CONNECT_WAN"),
                    Mission("Félicitations ! Testez en envoyant un paquet\nentre les maisons (Espace)", "L3_SEND_P_WAN"),
                    Mission("Réseau WAN complet ! Vous êtes en mode libre.", "EXPLANATION_FIN"),
                    Mission("Niveau 3 terminé ! Vous êtes en mode libre.", "DONE")
                ]
            else: # nl
                self.missions = [
                    Mission("L3: Plaats in Huis 1 een Router én een Switch.", "L3_PLACE_RS"),
                    Mission("Plaats 2 PC's rondom de Switch.", "L3_PLACE_PC"),
                    Mission("Verbind: Router->Switch en Switch->2x PC.", "L3_CONNECT_LAN"),
                    Mission("Plaats een Laptop in de buurt van de Routers blauwe cirkel.\nHij verbindt draadloos (Wi-Fi)!", "L3_WIFI"),
                    Mission("Huis 1 is lokaal klaar! We zoomen uit naar de Wereldkaart...", "L3_TO_WORLD_1"),
                    Mission("Dit is de Wereldkaart. Klik in dit vlak om Huis 2 binnen te gaan.", "L3_WORLD_1"),
                    Mission("Huis 2: Plaats hier ook een Router, Switch, 1 PC.\nVerbind: Router->Switch en Switch->PC.", "L3_BUILD_H2"),
                    Mission("Huis 2 compleet! Uitzoomen naar Wereldkaart...", "L3_TO_WORLD_2"),
                    Mission("Wereldkaart: Kies de WAN Fiber kabel rechts.", "L3_PICK_WAN"),
                    Mission("Op de kaart: Verbind Huis 1 en Huis 2 met de WAN kabel!", "L3_CONNECT_WAN"),
                    Mission("Gefeliciteerd! Test de verbinding door een pakketje\ntussen de huizen te sturen (Spatie)", "L3_SEND_P_WAN"),
                    Mission("WAN Netwerk voltooid! Je bent nu in Free Mode.", "EXPLANATION_FIN"),
                    Mission("Level 3 Compleet! Je bent nu in Free Mode.", "DONE")
                ]
        self.current_idx = 0
        self.packets_delivered = 0
        self.surf_success = False
        
    def get_current(self):
        if self.current_idx < len(self.missions):
            return self.missions[self.current_idx]
        return None

    def advance(self):
        self.current_idx += 1
        self.overlay_alpha = 0

    def draw_mission_text(self, surface):
        if self.wifi_timer > 0:
            t = font.render("Verbinding maken...", True, YELLOW)
            surface.blit(t, (WIDTH//2 - t.get_width()//2, 120))
            
        mission = self.get_current()
        if not mission or mission.type == "DONE":
            text = get_text('free_mode') if not mission else mission.text
            t_surf = mission_font.render(text, True, CYAN)
            surface.blit(t_surf, (WIDTH//2 - t_surf.get_width()//2, 80))
            return

        lines = mission.text.split('\n')
        if mission.type == "L3_BUILD_H2" and sm.current != "House2":
            lines = ["Klik op 'HUIS BETREDEN' en selecteer Huis 2", "om daar apparatuur te plaatsen."]
            
        y = HEIGHT - 80 # Move mission text to bottom
        for l in lines:
            t_surf = mission_font.render(l, True, YELLOW)
            surface.blit(t_surf, (WIDTH//2 - t_surf.get_width()//2, y))
            y += 28

        if mission.type == "L1_EXP_MOUSE":
            # Point to the area between devices
            s = abs(math.sin(pygame.time.get_ticks() * 0.01))
            pygame.draw.circle(surface, YELLOW, (200, 350), 30 + s*10, 2)

        if mission.type == "PLACE" and mission.target_pos:
            if gc_img:
                scaled_gc = pygame.transform.smoothscale(gc_img, (mission.radius*2, mission.radius*2))
                rect = scaled_gc.get_rect(center=mission.target_pos)
                surface.blit(scaled_gc, rect.topleft)
            else:
                pygame.draw.circle(surface, (100, 255, 100), mission.target_pos, mission.radius, 3)

        if mission.type == "PICK_CAT5E":
            if arrow_img:
                surface.blit(arrow_img, (720, 130))
            else:
                pygame.draw.line(surface, YELLOW, (700, 170), (790, 170), 6)
                pygame.draw.polygon(surface, YELLOW, [(790, 170), (770, 150), (770, 190)])

        # Icon explanations in Level 1
        if mission.type.startswith("L1_EXP_") and mission.target_pos:
             px, py = mission.target_pos
             s = abs(math.sin(pygame.time.get_ticks() * 0.01))
             pygame.draw.polygon(surface, YELLOW, [(px, py + 35 + s*10), (px-10, py+55+s*10), (px+10, py+55+s*10)])

    def draw_overlays(self, surface):
        if self.fail_timer > 0:
            surf = mission_font.render(self.fail_msg, True, RED, BLACK)
            surface.blit(surf, (WIDTH//2 - surf.get_width()//2, HEIGHT//2))
            self.fail_timer -= 1

        mission = self.get_current()
        
        if mission and mission.type == "INTRO":
            if self.overlay_alpha < 255: self.overlay_alpha = min(255, self.overlay_alpha + 15)
            ov_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            box = pygame.Rect(WIDTH//2 - 400, HEIGHT//2 - 200, 800, 400)
            pygame.draw.rect(ov_surf, (40, 40, 50), box)
            pygame.draw.rect(ov_surf, CYAN, box, 3)
            
            lines = [get_text('intro_title'), ""] + LANGS[current_lang]['intro_body']
            y = box.y + 20
            for l in lines:
                surf = font.render(l, True, WHITE)
                ov_surf.blit(surf, (box.x + 400 - surf.get_width()//2, y))
                y += 25
                
            ov_surf.set_alpha(self.overlay_alpha)
            surface.blit(ov_surf, (0,0))
            
        elif mission and mission.type == "EXPLANATION_CAT5":
            if self.overlay_alpha < 255: self.overlay_alpha = min(255, self.overlay_alpha + 15)
            ov_surf = pygame.Surface((1000, 700), pygame.SRCALPHA)
            box = pygame.Rect(500 - 350, 350 - 180, 700, 360)
            pygame.draw.rect(ov_surf, (40, 40, 50), box)
            pygame.draw.rect(ov_surf, RED, box, 3)
            
            text_lines = {
                'nl': ["Oeps! De verbinding is mislukt...", "", "Je probeert data over een te grote afstand te sturen met een Cat 5 kabel.", "Een standaard Cat 5 (koper)kabel is maar geschikt voor maximaal 100 meter.", "Hoe langer de kabel, hoe zwakker je signaal wordt. Dit noemt men 'attenuatie'.", "", "Gelukkig is er de Cat 5e (enhanced) kabel! Deze kan data beter en sneller", "sturen doordat de koperdraadjes strakker in elkaar gedraaid zitten tegen storingen.", "", "Klik hier ergens in dit vak om verder te gaan"],
                'en': ["Oops! The connection failed...", "", "You are trying to send data over too long a distance with a Cat 5 cable.", "A standard Cat 5 (copper) cable is only suitable for a maximum of 100 meters.", "The longer the cable, the weaker your signal becomes. This is called 'attenuation'.", "", "Fortunately, there is the Cat 5e (enhanced) cable! It can send data better and faster", "because the copper wires are twisted tighter against interference.", "", "Click anywhere in this box to continue"],
                'fr': ["Oups ! La connexion a échoué...", "", "Vous essayez d'envoyer des données sur une trop longue distance avec un câble Cat 5.", "Un câble Cat 5 standard n'est adapté que pour un maximum de 100 mètres.", "Plus le câble est long, plus le signal s'affaibit. C'est ce qu'on appelle 'l'atténuation'.", "", "Heureusement, il existe le câble Cat 5e ! Il envoie les données mieux et plus vite", "car les fils de cuivre sont torsadés plus serrés contre les interférences.", "", "Cliquez ici pour continuer"]
            }
            lines = text_lines.get(current_lang, text_lines['nl'])
            y = box.y + 20
            for l in lines:
                surf = font.render(l, True, WHITE)
                ov_surf.blit(surf, (box.x + 350 - surf.get_width()//2, y))
                y += 28
                
            ov_surf.set_alpha(self.overlay_alpha)
            surface.blit(ov_surf, (0,0))
            
        elif mission and mission.type == "L3_TO_WORLD_1":
            if self.overlay_alpha < 255: self.overlay_alpha = min(255, self.overlay_alpha + 15)
            ov_surf = pygame.Surface((1000, 700), pygame.SRCALPHA)
            box = pygame.Rect(500 - 350, 350 - 100, 700, 200)
            pygame.draw.rect(ov_surf, (40, 40, 50), box)
            pygame.draw.rect(ov_surf, GREEN, box, 3)
            
            text_lines = {
                'nl': ["Huis 1 is nu lokaal volledig verbonden!", "", "Klik hier om uit te zoomen naar de buitenwereld..."],
                'en': ["House 1 is now fully connected locally!", "", "Click here to zoom out to the outside world..."],
                'fr': ["La Maison 1 est maintenant entièrement connectée !", "", "Cliquez ici pour dézoomer sur le monde extérieur..."]
            }
            lines = text_lines.get(current_lang, text_lines['nl'])
            y = box.y + 50
            for l in lines:
                surf = font.render(l, True, WHITE)
                ov_surf.blit(surf, (box.x + 350 - surf.get_width()//2, y))
                y += 35
                
            ov_surf.set_alpha(self.overlay_alpha)
            surface.blit(ov_surf, (0,0))

        elif mission and mission.type == "L3_WORLD_1":
            if sm and sm.transition_state != "NONE": return
            if self.overlay_alpha < 255: self.overlay_alpha = min(255, self.overlay_alpha + 15)
            ov_surf = pygame.Surface((1000, 700), pygame.SRCALPHA)
            box = pygame.Rect(500 - 400, 350 - 150, 800, 300)
            pygame.draw.rect(ov_surf, (40, 40, 50), box)
            pygame.draw.rect(ov_surf, CYAN, box, 3)
            
            text_lines = {
                'nl': ["Je bevindt je nu op de Wereldkaart!", "", "Hier zie je de buitenkant van de lokale netwerken die je bouwt.", "In de verte staat een tweede huis (Huis 2) met een leeg netwerk.", "", "Klik eerst in dit vak om door te gaan", "Klik daarna op de knop 'HUIS BETREDEN' links om in te gaan!"],
                'en': ["You are now on the World Map!", "", "Here you see the outside of the local networks you build.", "In the distance is a second house (House 2) with an empty network.", "", "Click this box to continue", "Then click 'ENTER HOUSE' on the left to zoom in on House 2!"],
                'fr': ["Vous êtes maintenant sur la carte du monde !", "", "Ici, vous voyez l'extérieur des réseaux locaux que vous construisez.", "Au loin se trouve une deuxième maison (Maison 2) avec un réseau vide.", "", "Cliquez ici pour continuer", "Ensuite click sur 'ENTRER MAISON' à gauche pour zoomer sur la Maison 2 !"]
            }
            lines = text_lines.get(current_lang, text_lines['nl'])
            y = box.y + 30
            for l in lines:
                surf = font.render(l, True, WHITE)
                ov_surf.blit(surf, (box.x + 400 - surf.get_width()//2, y))
                y += 30
                
            ov_surf.set_alpha(self.overlay_alpha)
            surface.blit(ov_surf, (0,0))

        elif mission and mission.type == "L3_TO_WORLD_2":
            if self.overlay_alpha < 255: self.overlay_alpha = min(255, self.overlay_alpha + 15)
            ov_surf = pygame.Surface((1000, 700), pygame.SRCALPHA)
            box = pygame.Rect(500 - 350, 350 - 100, 700, 200)
            pygame.draw.rect(ov_surf, (40, 40, 50), box)
            pygame.draw.rect(ov_surf, GREEN, box, 3)
            
            lines = [
                "Ook Huis 2 is nu klaar!",
                "",
                "Klik hier om terug te keren naar de wereldkaart."
            ]
            y = box.y + 50
            for l in lines:
                surf = font.render(l, True, WHITE)
                ov_surf.blit(surf, (box.x + 350 - surf.get_width()//2, y))
                y += 35
                
            ov_surf.set_alpha(self.overlay_alpha)
            surface.blit(ov_surf, (0,0))

        elif mission and mission.type == "EXPLANATION_1":
            if self.overlay_alpha < 255: self.overlay_alpha = min(255, self.overlay_alpha + 15)
            ov_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            box = pygame.Rect(WIDTH//2 - 350, HEIGHT//2 - 180, 700, 360)
            pygame.draw.rect(ov_surf, (40, 40, 50), box)
            pygame.draw.rect(ov_surf, CYAN, box, 3)
            
            text_lines = {
                'nl': ["Je hebt zojuist een eigen lokaal netwerk (LAN) gemaakt!", "Door 3 computers te verbinden via ethernet kabels,", "kon je lokaal (binnen je eigen bereik) data-pakketjes rondsturen.", "", "Echter... Wat als je een website wilt bezoeken?", "Je kunt nu nog NIET op internet surfen!", "Je netwerk is gelimiteerd tot je eigen PCs.", "Daarvoor hebben we een *Router* nodig. Een router", "verbindt jouw lokale netwerk met het grote internet.", "", "Klik hier ergens in het vak om naar Level 2 te gaan!"],
                'en': ["You have just created your own local area network (LAN)!", "By connecting 3 computers via ethernet cables,", "you could send data packets locally (within your range).", "", "However... What if you want to visit a website?", "You can NOT surf the internet yet!", "Your network is limited to your own PCs.", "For that we need a *Router*. A router", "connects your local network to the big internet.", "", "Click anywhere in this box to go to Level 2!"],
                'fr': ["Vous venez de créer votre propre réseau local (LAN) !", "En connectant 3 ordinateurs via des câbles Ethernet,", "vous avez pu envoyer des paquets localement.", "", "Cependant... Et si vous vouliez visiter un site web ?", "Vous ne pouvez PAS encore surfer sur Internet !", "Votre réseau est limité à vos propres PC.", "Pour cela, nous avons besoin d'un *Routeur*. Un routeur", "connecte votre réseau local au vaste Internet.", "", "Cliquez ici pour passer au niveau 2 !"]
            }
            lines = text_lines.get(current_lang, text_lines['nl'])
            y = box.y + 20
            for l in lines:
                surf = font.render(l, True, WHITE)
                ov_surf.blit(surf, (box.x + 350 - surf.get_width()//2, y))
                y += 28
                
            ov_surf.set_alpha(self.overlay_alpha)
            surface.blit(ov_surf, (0,0))

        elif mission and mission.type == "EXPLANATION_2":
            if self.overlay_alpha < 255: self.overlay_alpha = min(255, self.overlay_alpha + 15)
            ov_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            box = pygame.Rect(WIDTH//2 - 400, HEIGHT//2 - 200, 800, 400)
            pygame.draw.rect(ov_surf, (40, 40, 50), box)
            pygame.draw.rect(ov_surf, CYAN, box, 3)
            
            text_lines = {
                'nl': ["Geweldig gedaan! Je hebt zojuist je eerste netwerk geconfigureerd.", "", "Een PC en Router hebben een IP-adres en Subnetmasker nodig", "om elkaar te kunnen vinden en netwerkverkeer te sturen.", "Anders weten de data pakketjes letterlijk niet waar naartoe!", "", "De Router fungeert als de voordeur naar de buitenwereld:", "het Wide Area Network (WAN), beter bekend als het Internet.", "", "Een Internet Service Provider (ISP), geeft een verbinding en IP", "aan jouw Router. Daardoor kon je netwerk met succes", "de website van Thomas More lokaal inladen en bereiken!", "", "Klik hier ergens in het vak om naar Level 3 te gaan."],
                'en': ["Great job! You have just configured your first network.", "", "A PC and Router need an IP address and Subnet mask", "to find each other and send network traffic.", "Otherwise, the data packets literally don't know where to go!", "", "The Router acts as the front door to the outside world:", "the Wide Area Network (WAN), better known as the Internet.", "", "An Internet Service Provider (ISP) gives a connection and IP", "to your Router. This allowed your network to successfully", "load and reach the Thomas More website locally!", "", "Click anywhere in this box to go to Level 3."],
                'fr': ["Excellent travail ! Vous venez de configurer votre premier réseau.", "", "Un PC et un routeur ont besoin d'une adresse IP et d'un masque", "pour se trouver et envoyer du trafic réseau.", "Sinon, les paquets ne savent littéralement pas où aller !", "", "Le routeur agit comme la porte d'entrée vers le monde extérieur :", "le Wide Area Network (WAN), mieux connu sous le nom d'Internet.", "", "Un fournisseur d'accès (ISP) donne une connexion et une IP", "à votre routeur. C'est ce qui a permis à votre réseau de", "charger le site de Thomas More avec succès !", "", "Cliquez ici pour passer au niveau 3."]
            }
            lines = text_lines.get(current_lang, text_lines['nl'])
            y = box.y + 20
            for l in lines:
                surf = font.render(l, True, WHITE)
                ov_surf.blit(surf, (box.x + 400 - surf.get_width()//2, y))
                y += 25
                
            ov_surf.set_alpha(self.overlay_alpha)
            surface.blit(ov_surf, (0,0))

        elif mission and mission.type == "EXPLANATION_FIN":
            if self.overlay_alpha < 255: self.overlay_alpha = min(255, self.overlay_alpha + 15)
            ov_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            box = pygame.Rect(WIDTH//2 - 400, HEIGHT//2 - 200, 800, 400)
            pygame.draw.rect(ov_surf, (20, 40, 20), box)
            pygame.draw.rect(ov_surf, GREEN, box, 3)
            
            text_lines = {
                'nl': ["PROFICIAT! Je hebt het WAN netwerk voltooid!", "", "Je hebt nu alle levels van de simulator doorlopen.", "Je weet hoe je apparaten plaatst, kabels trekt, IP's instelt", "en verbinding maakt tussen afgelegen locaties.", "", "Vanaf nu zit je in de FREE MODE / ENDLESS MODE.", "Je kunt nu vrij alle huizen verkennen, extra apparatuur bouwen", "en het hele wegennetwerk bekabelen zoals jij dat wilt!", "", "Klik hier om de sandbox mode te starten."],
                'en': ["CONGRATULATIONS! You have completed the WAN network!", "", "You have finished all levels of the simulator.", "You know how to place devices, pull cables, set IPs", "and connect remote locations.", "", "From now on you are in FREE MODE / ENDLESS MODE.", "You can freely explore all houses, build extra equipment", "and wire the entire road network as you wish!", "", "Click here to start sandbox mode."],
                'fr': ["FÉLICITATIONS ! Vous avez terminé le réseau WAN !", "", "Vous avez terminé tous les niveaux du simulateur.", "Vous savez placer des appareils, tirer des câbles, régler des IP", "et connecter des sites distants.", "", "Désormais, vous êtes en MODE LIBRE / MODE INFINI.", "Vous pouvez explorer toutes les maisons, construire du matériel", "et câbler tout le réseau routier comme vous le souhaitez !", "", "Cliquez ici pour lancer le mode bac à sable."]
            }
            lines = text_lines.get(current_lang, text_lines['nl'])
            y = box.y + 20
            for l in lines:
                surf = font.render(l, True, WHITE)
                ov_surf.blit(surf, (box.x + 400 - surf.get_width()//2, y))
                y += 25
                
            ov_surf.set_alpha(self.overlay_alpha)
            surface.blit(ov_surf, (0,0))

    def check_conditions(self, devices, connections, packets):
        mission = self.get_current()
        if not mission: return

        if mission.type == "PLACE":
            for d in devices:
                if d.type == mission.dev_type:
                    dist = math.hypot(d.x - mission.target_pos[0], d.y - mission.target_pos[1])
                    if dist <= mission.radius:
                        self.advance()
                        return
                        
        elif mission.type == "CONNECT":
            for c in connections:
                if c.is_valid and c.d1.type == 'PC' and c.d2.type == 'PC':
                    self.advance()
                    return
                    
        elif mission.type == "TRY_CONNECT":
            for c in connections:
                if c.is_valid and c.d1.type == 'PC' and c.d2.type == 'PC':
                    if c.distance > 400 and c.cable_type == 'Cat 5e':
                        self.advance()
                        self.advance()
                        self.advance()
                        return
                    
        elif mission.type == "CONNECT_CAT5E":
            for c in connections:
                if c.is_valid and c.d1.type == 'PC' and c.d2.type == 'PC':
                    if c.distance > 400 and c.cable_type == 'Cat 5e':
                        self.advance()
                        return
                        
        elif mission.type == "CONNECT_R":
            for c in connections:
                if c.is_valid and ((c.d1.type == 'PC' and c.d2.type == 'Router') or (c.d1.type == 'Router' and c.d2.type == 'PC')):
                    self.advance()
                    return
                    
        elif mission.type == "CONF_ROUTER":
            for d in devices:
                if d.type == 'Router' and d.ip == "192.168.1.1" and d.subnet in ("255.255.255.0", "24"):
                    self.advance()
                    return
                    
        elif mission.type == "CONF_PC":
            for d in devices:
                if d.type == 'PC' and d.ip == "192.168.1.2" and d.subnet in ("255.255.255.0", "24"):
                    self.advance()
                    return
                        
        elif mission.type == "L3_PLACE_RS":
            has_r = sum(1 for d in devices if d.type == 'Router')
            has_s = sum(1 for d in devices if d.type == 'Switch')
            if has_r >= 1 and has_s >= 1: self.advance()
            
        elif mission.type == "L3_PLACE_PC":
            if sum(1 for d in devices if d.type == 'PC') >= 2: self.advance()
            
        elif mission.type == "L3_CONNECT_LAN":
            r_s = False
            s_p = 0
            for c in connections:
                if not c.is_valid: continue
                types = {c.d1.type, c.d2.type}
                if types == {'Router', 'Switch'}: r_s = True
                if types == {'Switch', 'PC'}: s_p += 1
            if r_s and s_p >= 2: self.advance()
            
        elif mission.type == "L3_WIFI":
            connected = False
            for c in connections:
                if c.cable_type == 'Wi-Fi' and c.is_valid:
                    connected = True
                    break
            
            if connected:
                if self.wifi_timer <= 0:
                    self.wifi_timer = 270 # 4.5 seconds (requested)
                
                self.wifi_timer -= 1
                if self.wifi_timer <= 1: # 1 to avoid re-triggering 240 logic above next frame
                    self.advance()
                    self.wifi_timer = 0
            else:
                self.wifi_timer = 0
                    
        elif mission.type == "L3_BUILD_H2":
            has_r = sum(1 for d in devices if d.type == 'Router')
            has_s = sum(1 for d in devices if d.type == 'Switch')
            has_p = sum(1 for d in devices if d.type == 'PC')
            if has_r >= 1 and has_s >= 1 and has_p >= 1:
                r_s = False
                s_p = False
                for c in connections:
                    if not c.is_valid: continue
                    types = {c.d1.type, c.d2.type}
                    if types == {'Router', 'Switch'}: r_s = True
                    if types == {'Switch', 'PC'}: s_p = True
                if r_s and s_p:
                    self.advance()
                    
        elif mission.type == "L3_CONNECT_WAN":
            for c in connections:
                if c.is_valid and c.cable_type == 'WAN Fiber':
                    if {c.d1.type, c.d2.type} == {'House1', 'House2'}:
                        self.advance()
                        return
                        
        elif mission.type == "L3_SEND_P_WAN":
            # Check if a packet has travelled between House 1 and House 2
            # For simplicity, we can check delivered packets if they were across WAN
            if self.packets_delivered >= 1 and len(packets) == 0:
                self.advance()
                return
                        
        elif mission.type == "PACKET":
            if self.packets_delivered > 0 and len(packets) == 0:
                self.advance()
                return

def find_path(devices, connections, start_dev, target_dev):
    adj = {d.id: [] for d in devices}
    for c in connections:
        if c.is_valid:
            adj[c.d1.id].append(c.d2)
            adj[c.d2.id].append(c.d1)
    
    queue = [[start_dev]]
    visited = set([start_dev.id])
    while queue:
        path = queue.pop(0)
        curr = path[-1]
        
        if curr.id == target_dev.id:
            return path
            
        for neighbor in adj[curr.id]:
            if neighbor.id not in visited:
                visited.add(neighbor.id)
                queue.append(path + [neighbor])
    return None

def find_path_to_type(devices, connections, start_dev, dev_type='Router'):
    adj = {d.id: [] for d in devices}
    for c in connections:
        if c.is_valid:
            adj[c.d1.id].append(c.d2)
            adj[c.d2.id].append(c.d1)
    
    queue = [[start_dev]]
    visited = set([start_dev.id])
    while queue:
        path = queue.pop(0)
        curr = path[-1]
        
        if curr.type == dev_type:
            return path
            
        for neighbor in adj[curr.id]:
            if neighbor.id not in visited:
                visited.add(neighbor.id)
                queue.append(path + [neighbor])
    return None

def main():
    global sm, mission_sys, devices, connections, packets, current_mode, current_cable
    sm = SceneManager()
    mission_sys = MissionSystem()
    
    btn_cat5 = pygame.Rect(810, 90, 180, 40)
    btn_cat5e = pygame.Rect(810, 150, 180, 40)
    btn_wan = pygame.Rect(810, 210, 180, 40)
    
    btn_modi = {
        'PC': pygame.Rect(20, 10, 60, 60),
        'Laptop': pygame.Rect(90, 10, 60, 60),
        'Switch': pygame.Rect(160, 10, 60, 60),
        'Router': pygame.Rect(230, 10, 60, 60),
        'DELETE': pygame.Rect(300, 10, 80, 60)
    }
    btn_enter_house = pygame.Rect(20, 120, 180, 50)
    btn_data = pygame.Rect(390, 10, 80, 60)
    
    error_msg = ""
    error_timer = 0
    
    dragging = False
    drag_start_dev = None
    mouse_pos = (0, 0)
    
    active_device = None
    active_window = None # "MENU", "IP", "WEB"
    ui_alpha = 0
    
    debug_skip_timer = 0
    
    ip_input = TextInput(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 30)
    subnet_input = TextInput(WIDTH//2 - 100, HEIGHT//2 + 30, 200, 30)
    url_input = TextInput(WIDTH//2 - 200, HEIGHT//2 + 5, 300, 30, default="www.")
    
    clock = pygame.time.Clock()
    
    while True:
        curr = sm.get_current()
        devices = curr['devices']
        connections = curr['connections']
        packets = curr['packets']
        
        # DEBUG SKIP (F + K for 2s)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and keys[pygame.K_k]:
            debug_skip_timer += 1
            if debug_skip_timer >= 120:
                mission_sys.level = 3
                devices.clear()
                connections.clear()
                packets.clear()
                mission_sys.setup_level()
                sm.current = "House1"
                current_mode = "PC"
                debug_skip_timer = 0
        else:
            debug_skip_timer = 0
            
        sm.update()
        if sm.transition_state == "FADE_IN" and sm.target_scene == "World":
            current_mode = None
            current_cable = None # Reset kabel bij binnenkomst Wereldkaart voor 'Huis Betreden' modus
            
        m = mission_sys.get_current()
                
        if bg_img and sm.current != 'World' and sm.current != 'Start':
            screen.blit(bg_img, (0, 0))
        elif sm.current == 'World':
            screen.fill((40, 80, 40)) # Donkerder groen
            # Een weg / horizon
            pygame.draw.rect(screen, (60, 60, 60), (0, 300, 1000, 100))
            pygame.draw.line(screen, YELLOW, (0, 350), (1000, 350), 2)
        elif sm.current == 'Start':
            sm.draw_start_screen(screen)
        else:
            screen.fill(BLACK)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if active_device and active_window in ("IP", "WEB"):
                    if active_window == "IP":
                        ip_input.handle_event(event)
                        subnet_input.handle_event(event)
                    elif active_window == "WEB" and not mission_sys.surf_success:
                        url_input.handle_event(event)
                else:
                    if event.key == pygame.K_1: current_mode = 'PC'
                    elif event.key == pygame.K_2: current_mode = 'Laptop'
                    elif event.key == pygame.K_3: current_mode = 'Switch'
                    elif event.key == pygame.K_4: current_mode = 'Router'
                    elif event.key == pygame.K_d: current_mode = 'DELETE'
                    elif event.key == pygame.K_SPACE:
                        mission = mission_sys.get_current()
                        if sm.current == 'World':
                            # Send packet between House 1 and House 2
                            h1 = next((d for d in devices if d.type == 'House1'), None)
                            h2 = next((d for d in devices if d.type == 'House2'), None)
                            if h1 and h2:
                                path = find_path(devices, connections, h1, h2)
                                if path and len(path) > 1:
                                    packets.append(PacketPath(path))
                                    m = mission_sys.get_current()
                                    if m and m.type == "L3_SEND_P_WAN":
                                        mission_sys.advance()
                        else:
                            endpoints = [d for d in devices if d.type in ('PC', 'Laptop')]
                            if len(endpoints) >= 2:
                                start_pc = endpoints[0]
                                target_pc = endpoints[-1]
                                for d in endpoints:
                                    if d.x > target_pc.x: target_pc = d
                                
                                if target_pc != start_pc:
                                    path = find_path(devices, connections, start_pc, target_pc)
                                    if path and len(path) > 1:
                                        packets.append(PacketPath(path))
                                        if mission and mission.type == "PACKET":
                                            # Wait for delivery in check_conditions
                                            pass
                                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    # START SCREEN CLICKS
                    if sm.current == 'Start':
                        # Langs
                        bx = WIDTH//2 - 250
                        for code, name in [('nl', 'NEDERLANDS'), ('en', 'ENGLISH'), ('fr', 'FRANÇAIS')]:
                            r = pygame.Rect(bx, 260, 150, 40)
                            if r.collidepoint(event.pos):
                                global current_lang
                                current_lang = code
                                mission_sys.setup_level() # Re-setup missions for new lang
                            bx += 175
                        
                        # Play / Quit
                        btn_play = pygame.Rect(WIDTH//2 - 100, 400, 200, 60)
                        if btn_play.collidepoint(event.pos):
                            sm.start_transition("Level1", get_text('trans_zoom_in'))
                        
                        btn_quit = pygame.Rect(WIDTH//2 - 100, 500, 200, 60)
                        if btn_quit.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                        continue
                        
                    # OS WINDOW CLICKS
                    if active_device:
                        box = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 150, 500, 300)
                        dist_to_red = math.hypot(event.pos[0] - (box.x + 15), event.pos[1] - (box.y + 15))
                        if dist_to_red <= 12:
                            active_device = None
                            active_window = None
                            mission = mission_sys.get_current()
                            if mission and mission.type == "CLOSE_WINDOW":
                                mission_sys.advance()
                            continue
                            
                        btn_back = pygame.Rect(box.x + 75, box.y + 4, 60, 22)
                        if active_window != "MENU" and btn_back.collidepoint(event.pos):
                            if active_window == "WEB" and mission_sys.surf_success:
                                pass # allow back to menu if successful
                            active_window = "MENU"
                            ui_alpha = 0
                            continue
                            
                        if active_window == "MENU":
                            bx, by = box.x + 50, box.y + 70
                            options = []
                            if active_device.type in ('PC', 'Laptop'):
                                options = [(get_text('ip_settings'), "ip_instellingen.png"), (get_text('web_browsing'), "web_browsing.png"), (get_text('terminal'), "terminal.png")]
                            else:
                                options = [(get_text('ip_settings'), "ip_instellingen.png"), (get_text('restart'), "restart.png"), (get_text('reset'), "factory_reset.png")]
                            
                            for name, icon_file in options:
                                r = pygame.Rect(bx, by, 100, 100)
                                if r.collidepoint(event.pos):
                                    if name == "IP Instellingen":
                                        active_window = "IP"
                                        ui_alpha = 0
                                        ip_input.text = active_device.ip
                                        subnet_input.text = active_device.subnet
                                    elif name == "Web Browsing" and active_device.type in ('PC', 'Laptop'):
                                        active_window = "WEB"
                                        ui_alpha = 0
                                        url_input.text = "www."
                                        mission_sys.surf_success = False
                                        mission_sys.popup_text = ""
                                    elif name == "Restart":
                                        active_device = None
                                        active_window = None
                                    elif name == "Factory Reset":
                                        active_device.ip = ""
                                        active_device.subnet = ""
                                    break
                                bx += 130
                                
                        elif active_window == "IP":
                            ip_input.handle_event(event)
                            subnet_input.handle_event(event)
                            btn_save = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 + 90, 100, 30)
                            if btn_save.collidepoint(event.pos):
                                active_device.ip = ip_input.text
                                active_device.subnet = subnet_input.text
                                
                        elif active_window == "WEB":
                            if not mission_sys.surf_success:
                                url_input.handle_event(event)
                                btn_go = pygame.Rect(WIDTH//2 + 150, HEIGHT//2, 80, 40)
                                if btn_go.collidepoint(event.pos):
                                    if url_input.text == "www.thomasmore.be":
                                        if active_device.ip:
                                            path = find_path_to_type(devices, connections, active_device, 'Router')
                                            if path:
                                                router = path[-1]
                                                if router.ip:
                                                    mission_sys.surf_success = True
                                                    mission_sys.popup_text = ""
                                                    m = mission_sys.get_current()
                                                    if m and m.type == "SURF":
                                                        mission_sys.advance()
                                                else:
                                                    mission_sys.popup_text = "Fout: Router IP of Subnet incorrect."
                                            else:
                                                mission_sys.popup_text = "Fout: Geen route naar een Router."
                                        else:
                                            mission_sys.popup_text = "Fout: PC heeft geen IP-adres."
                                    else:
                                        mission_sys.popup_text = "Fout: 404 Website niet gevonden."
                        
                        continue # Block world clicks when OS is open
                        
                    # Educational Overlays dismissal (World Map fix)
                    mission = mission_sys.get_current()
                    if mission and sm.transition_state == "NONE":
                        if mission.type == "L3_WORLD_1":
                            box = pygame.Rect(100, 150, 800, 300)
                            if box.collidepoint(event.pos):
                                mission_sys.overlay_alpha = 0
                                mission_sys.advance() # Advances to L3_BUILD_H2
                                continue
                        if mission.type == "L3_TO_WORLD_1":
                            box = pygame.Rect(150, 250, 700, 200)
                            if box.collidepoint(event.pos):
                                sm.start_transition("World", "Uitzoomen naar de Wereldkaart...")
                                if not any(d.type == 'House1' and not d.decorative for d in sm.scenes['World']['devices']):
                                    # Place real houses beside the road (y=250 or y=450)
                                    # Place real houses closer to the road (y=258 or y=442)
                                    sm.scenes['World']['devices'].append(Device(300, 258, 'House1'))
                                    sm.scenes['World']['devices'].append(Device(700, 442, 'House2'))
                                    # Decorative houses
                                    sm.scenes['World']['devices'].append(Device(100, 442, 'House1', decorative=True))
                                    sm.scenes['World']['devices'].append(Device(500, 258, 'House2', decorative=True))
                                    sm.scenes['World']['devices'].append(Device(900, 442, 'House1', decorative=True))
                                mission_sys.advance()
                            continue
                        if mission.type == "L3_TO_WORLD_2":
                            box = pygame.Rect(150, 250, 700, 200)
                            if box.collidepoint(event.pos):
                                sm.start_transition("World", "Uitzoomen naar de Wereldkaart...")
                                mission_sys.advance()
                            continue
                    
                    # Entering houses from World Map
                    if sm.current == 'World' and sm.transition_state == "NONE":
                        # VERBETERING: Alleen huizen binnen als we geen kabel vasthebben (Huis Betreden modus)
                        if mission_sys.overlay_alpha == 0 and current_cable is None:
                            for d in devices:
                                if d.type in ['House1', 'House2'] and not d.decorative:
                                    dist = math.hypot(event.pos[0] - d.x, event.pos[1] - d.y)
                                    if dist < d.radius + 10:
                                        scene_name = "House1" if d.type == 'House1' else "House2"
                                        sm.start_transition(scene_name, f"Inzoomen op {scene_name}...")
                                        current_cable = 'Cat 5' # Reset naar standaard kabel bij binnengaan
                                        break
            
                    # Terug naar Wereldknop (Alleen in Huis 2!)
                    if sm.current == 'House2' and mission_sys.level == 3:
                        btn_to_world = pygame.Rect(20, HEIGHT//2 - 20, 220, 40)
                        if btn_to_world.collidepoint(event.pos):
                            sm.start_transition("World", "Terug naar het overzicht...")
            
                    # INTRO popup click handler (General)
                    if mission and mission.type in ("INTRO", "L1_EXP_PC", "L1_EXP_LAP", "L1_EXP_SW", "L1_EXP_RT", "L1_EXP_MOUSE"):
                        box = pygame.Rect(WIDTH//2 - 400, HEIGHT//2 - 200, 800, 400)
                        if mission.type == "INTRO":
                            if box.collidepoint(event.pos):
                                mission_sys.advance()
                        else:
                            # Advance icon explanation on ANY click
                            mission_sys.advance()
                        continue

                    if mission and mission.type == "EXPLANATION_CAT5":
                        box = pygame.Rect(WIDTH//2 - 350, HEIGHT//2 - 180, 700, 360)
                        if box.collidepoint(event.pos):
                            mission_sys.advance()
                        continue
                    if mission and mission.type == "EXPLANATION_1":
                        box = pygame.Rect(WIDTH//2 - 350, HEIGHT//2 - 180, 700, 360)
                        if box.collidepoint(event.pos):
                            mission_sys.level = 2
                            devices.clear()
                            connections.clear()
                            packets.clear()
                            mission_sys.setup_level()
                            current_mode = 'Router'
                        continue
                    if mission and mission.type == "EXPLANATION_2":
                        box = pygame.Rect(WIDTH//2 - 400, HEIGHT//2 - 200, 800, 400)
                        if box.collidepoint(event.pos):
                            mission_sys.level = 3
                            devices.clear()
                            connections.clear()
                            packets.clear()
                            mission_sys.setup_level()
                            current_mode = 'PC'
                        continue

                    # UI Cables
                    if btn_cat5.collidepoint(event.pos):
                        current_cable = 'Cat 5'
                        continue
                    if btn_cat5e.collidepoint(event.pos):
                        current_cable = 'Cat 5e'
                        mission = mission_sys.get_current()
                        if mission and mission.type == "PICK_CAT5E":
                            mission_sys.advance()
                        continue
                    if btn_wan.collidepoint(event.pos):
                        current_cable = 'WAN Fiber'
                        mission = mission_sys.get_current()
                        if mission and mission.type == "L3_PICK_WAN":
                            mission_sys.advance()
                        continue
                                            
                    if btn_data.collidepoint(event.pos):
                        # Trigger Spatie logic
                        if sm.current == 'World':
                            h1 = next((d for d in devices if d.type == 'House1'), None)
                            h2 = next((d for d in devices if d.type == 'House2'), None)
                            if h1 and h2:
                                path = find_path(devices, connections, h1, h2)
                                if path and len(path) > 1:
                                    packets.append(PacketPath(path))
                                    m = mission_sys.get_current()
                                    if m and m.type == "L3_SEND_P_WAN":
                                        mission_sys.advance()
                        else:
                            # Standard send packet logic
                            endpoints = [d for d in devices if d.type in ('PC', 'Laptop')]
                            if len(endpoints) >= 2:
                                start_pc = endpoints[0]
                                target_pc = endpoints[-1]
                                for d in endpoints:
                                    if d.x > target_pc.x: target_pc = d
                                if target_pc != start_pc:
                                    path = find_path(devices, connections, start_pc, target_pc)
                                    if path and len(path) > 1:
                                        packets.append(PacketPath(path))
                                        if m and m.type == "PACKET":
                                            # Wait for delivery
                                            pass
                        continue
                        
                    # Top Modes (Toolbar)
                    if sm.current != 'World':
                        clicked_menu = False
                        for m_t, r in btn_modi.items():
                            if r.collidepoint(event.pos):
                                current_mode = m_t
                                clicked_menu = True
                                break
                        if clicked_menu:
                            continue
                        
                        if event.pos[1] < 100: # Blokkering van bovenste balk
                            continue
                    else:
                        # Op de wereldkaart is alles behalve WAN Fiber geblokkeerd
                        if btn_enter_house.collidepoint(event.pos):
                            current_cable = None
                            current_mode = None
                            continue
                        
                        if btn_wan.collidepoint(event.pos):
                            current_cable = 'WAN Fiber'
                            current_mode = None
                            continue
                        
                        if event.pos[1] < 100 or (event.pos[0] > 800 and event.pos[1] < 300):
                            # Strikte blokkering van onzichtbare toolbar en kabels
                            continue

                    # UI Cables (Binnenshuis)
                    if sm.current != 'World':
                        if btn_cat5.collidepoint(event.pos):
                            current_cable = 'Cat 5'
                            continue
                        if btn_cat5e.collidepoint(event.pos):
                            current_cable = 'Cat 5e'
                            continue
                    else:
                        # WAN Fiber al hierboven afgehandeld
                        pass
                        
                    # Devices
                    clicked_dev = None
                    for d in reversed(devices):
                        if math.hypot(d.x - event.pos[0], d.y - event.pos[1]) < d.radius:
                            clicked_dev = d
                            break
                            
                    if current_mode == 'DELETE':
                        if clicked_dev:
                             # FIX: Huizen mogen niet verwijderd worden!
                             if clicked_dev.type not in ['House1', 'House2']:
                                 devices.remove(clicked_dev)
                                 connections = [c for c in connections if c.d1 != clicked_dev and c.d2 != clicked_dev]
                                 packets = [p for p in packets if clicked_dev not in getattr(p, 'path', [])]
                                 curr['connections'] = connections
                                 curr['packets'] = packets
                        else:
                            for c in connections:
                                mx, my = (c.d1.x + c.d2.x) / 2, (c.d1.y + c.d2.y) / 2
                                if math.hypot(mx - event.pos[0], my - event.pos[1]) < 20:
                                    connections.remove(c)
                                    break
                    else:
                        if clicked_dev:
                            drag_start_dev = clicked_dev
                            dragging = True
                        else:
                            mission = mission_sys.get_current()
                            if mission and mission.type == "PLACE":
                                if current_mode != mission.dev_type:
                                    mission_sys.fail_msg = f"FOUT: Plaats een {mission.dev_type}, geen {current_mode}."
                                    mission_sys.fail_timer = 240
                                    devices.clear()
                                    connections.clear()
                                    packets.clear()
                                    mission_sys.setup_level()
                                    continue
                            
                            # Restrictions: Geen apparaten op de wereldkaart
                            if sm.current == 'World':
                                continue
                                
                            new_dev = Device(event.pos[0], event.pos[1], current_mode)
                            devices.append(new_dev)
                            
                            if current_mode == 'Laptop':
                                for d in devices:
                                   if d.type == 'Router':
                                    dist = math.hypot(d.x - new_dev.x, d.y - new_dev.y)
                                    if dist < CABLES['Wi-Fi']['max_dist']:
                                        connections.append(Connection(new_dev, d, 'Wi-Fi'))
                                        mission_sys.wifi_timer = 90 # 1.5 sec delay
                                        break
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if dragging and drag_start_dev:
                        target_dev = None
                        for d in devices:
                            if math.hypot(d.x - event.pos[0], d.y - event.pos[1]) < d.radius:
                                target_dev = d
                                break
                                
                        if target_dev == drag_start_dev:
                            # Opende het OS (Niet op de Wereldkaart!)
                            if sm.current != 'World':
                                active_device = drag_start_dev
                                active_window = "MENU"
                                ui_alpha = 0
                        elif target_dev:
                            # Verbinding
                            dist = math.hypot(drag_start_dev.cable_c[0] - target_dev.cable_c[0], drag_start_dev.cable_c[1] - target_dev.cable_c[1])
                            mission = mission_sys.get_current()
                            if mission and mission.type == "TRY_CONNECT":
                                if dist > CABLES['Cat 5']['max_dist'] and current_cable == 'Cat 5':
                                    mission_sys.advance() 
                                    
                            exists = False
                            for c in connections:
                                if (c.d1 == drag_start_dev and c.d2 == target_dev) or (c.d2 == drag_start_dev and c.d1 == target_dev):
                                    exists = True
                                    c.cable_type = current_cable
                                    c.update_validity()
                                    break
                            if not exists and current_cable in CABLES:
                                 if dist <= CABLES[current_cable]['max_dist']:
                                     connections.append(Connection(drag_start_dev, target_dev, current_cable))
                                     error_timer = 0 
                                     error_msg = "" # Explicitly clear the text
                                 else:
                                     miss = mission_sys.get_current()
                                     if miss and miss.type == "TRY_CONNECT" and current_cable == 'Cat 5':
                                         mission_sys.advance()
                                     else:
                                         error_msg = f"{get_text('error_len')} {CABLES[current_cable]['max_m']}m"
                                         error_timer = 1200
                                
                    dragging = False
                    drag_start_dev = None
                    
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                
        for c in connections: c.draw(screen)
            
        if dragging and drag_start_dev and current_cable in CABLES:
            c1x, c1y = drag_start_dev.cable_c
            drag_dist = math.hypot(c1x - mouse_pos[0], c1y - mouse_pos[1])
            if drag_dist > drag_start_dev.radius:
                max_dist = CABLES[current_cable]['max_dist']
                max_m = CABLES[current_cable]['max_m']
                dist_m = int(drag_dist / 4)
                
                color = CABLES[current_cable]['color'] if drag_dist <= max_dist else RED
                
                angle = math.atan2(mouse_pos[1] - c1y, mouse_pos[0] - c1x)
                d1_dist = drag_start_dev.cable_dist(angle)
                start_x = c1x + math.cos(angle) * d1_dist
                start_y = c1y + math.sin(angle) * d1_dist
                
                pygame.draw.line(screen, color, (start_x, start_y), mouse_pos, 4)
                
                if drag_dist > max_dist:
                    msg_too_long = "Too long!" if current_lang == 'en' else "Trop long!" if current_lang == 'fr' else "Te lang!"
                    text = small_font.render(f"{msg_too_long} {dist_m}m / {max_m}m", True, RED)
                else:
                    msg_max = "Max" if current_lang != 'nl' else "Max" # Same for all?
                    text = small_font.render(f"{dist_m}m ({msg_max} {max_m}m)", True, WHITE)
                screen.blit(text, (mouse_pos[0] + 10, mouse_pos[1] + 10))
            
        new_packets = []
        for p in packets:
            p.update()
            p.draw(screen)
            if not p.reached:
                new_packets.append(p)
            else:
                mission_sys.packets_delivered += 1
                
        packets = new_packets
        curr['packets'] = packets

        for d in devices: d.draw(screen, sm.current)
        
        # World Map extra visuals
        if sm.current == 'World':
            # Street Name
            st_font = pygame.font.SysFont(None, 40, bold=True)
            st_txt = st_font.render("Stationsstraat", True, (200, 200, 200))
            screen.blit(st_txt, (30, 640))

        # Laptop Wi-Fi Placement Guide
        if current_mode == 'Laptop' and sm.current != 'World':
            for d in devices:
                if d.type == 'Router':
                    # Best placement zone (80px to 200px)
                    # Use transparency
                    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    pygame.draw.circle(s, (0, 255, 255, 30), (d.x, d.y), 200)
                    pygame.draw.circle(s, (0, 0, 0, 0), (d.x, d.y), 80)
                    screen.blit(s, (0,0))
                    pygame.draw.circle(screen, CYAN, (d.x, d.y), 200, 1)
                    pygame.draw.circle(screen, CYAN, (d.x, d.y), 80, 1)

        # UI overlays
        for m_t, r in btn_modi.items():
            # Restriction: No devices placement on World Map
            if sm.current == 'World' and m_t != 'DELETE':
                continue
                
            bgcolor = (100, 200, 100) if current_mode == m_t else (60, 60, 60)
            if m_t == 'DELETE':
                bgcolor = RED if current_mode == 'DELETE' else (60, 60, 60)
            pygame.draw.rect(screen, bgcolor, r)
            pygame.draw.rect(screen, WHITE, r, 2)
            
            icon = ICONS.get(m_t)
            if icon:
                scaled_icon = pygame.transform.smoothscale(icon, (30, 30))
                icon_x = r.x + 25 if m_t == 'DELETE' else r.x + 15
                screen.blit(scaled_icon, (icon_x, r.y + 25))
            
            if m_t == 'DELETE':
                dt2 = small_font.render("[D]", True, WHITE)
                screen.blit(dt2, (r.x + 30, r.y + 5))
            else:
                num_map = {'PC': '1', 'Laptop': '2', 'Switch': '3', 'Router': '4'}
                t = font.render(num_map.get(m_t, ''), True, WHITE)
                screen.blit(t, (r.x + 5, r.y + 2))
                
        # Space button (only show/enable in appropriate phases)
        pygame.draw.rect(screen, (60, 60, 60), btn_data)
        pygame.draw.rect(screen, WHITE, btn_data, 2)
        if data_img:
            scaled_data = pygame.transform.smoothscale(data_img, (30, 30))
            screen.blit(scaled_data, (btn_data.x + 25, btn_data.y + 5))
        dt = small_font.render(f"[{get_text('spacebar')}]", True, WHITE)
        screen.blit(dt, (btn_data.x + 10, btn_data.y + 35))

        menu_title = font.render(get_text('select_cable') if 'select_cable' in LANGS[current_lang] else ("Choose Cable:" if current_lang == 'en' else "Choisir Câble:" if current_lang == 'fr' else "Kies Kabel:"), True, WHITE)
        screen.blit(menu_title, (810, 50))
        
        for btn, name in [(btn_cat5, 'Cat 5'), (btn_cat5e, 'Cat 5e'), (btn_wan, 'WAN Fiber')]:
            # Restriction: Only WAN Fiber on World map, No WAN Fiber in House
            if sm.current == 'World' and name != 'WAN Fiber': continue
            if sm.current != 'World' and name == 'WAN Fiber': continue
            
            btn_color = (60, 60, 60) if current_cable != name else (100, 200, 100)
            pygame.draw.rect(screen, btn_color, btn)
            pygame.draw.rect(screen, WHITE, btn, 2)
            lbl_key = 'cat5_label' if name == 'Cat 5' else 'cat5e_label' if name == 'Cat 5e' else 'wan_label'
            t = font.render(get_text(lbl_key), True, WHITE)
            screen.blit(t, (btn.x + 10, btn.y + 10))
        # Terug naar Wereldknop tekenen (Alleen in Huis 2!)
        if sm.current == 'House2' and mission_sys.level == 3:
            btn_w = pygame.Rect(20, HEIGHT//2 - 20, 220, 40)
            pygame.draw.rect(screen, (70, 70, 90), btn_w)
            pygame.draw.rect(screen, CYAN, btn_w, 2)
            tw = font.render(get_text('to_world'), True, WHITE)
            screen.blit(tw, (btn_w.x + btn_w.width//2 - tw.get_width()//2, btn_w.y + 10))

        # Huis Betreden Knop op Wereldkaart
        if sm.current == 'World':
            color = GREEN if current_cable is None else (60, 60, 80)
            pygame.draw.rect(screen, color, btn_enter_house, 0, 5)
            pygame.draw.rect(screen, WHITE, btn_enter_house, 2, 5)
            tt = font.render(get_text('enter_house'), True, WHITE)
            screen.blit(tt, (btn_enter_house.x + btn_enter_house.width//2 - tt.get_width()//2, btn_enter_house.y + 15))
            
            # Pijl naar knop bij missie naar H2 (PAS ALS POPUP WEG IS)
            m = mission_sys.get_current()
        if active_device:
            if ui_alpha < 255:
                ui_alpha = min(255, ui_alpha + 25)
                
            os_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            box = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 150, 500, 300)
            
            if active_window == "WEB" and mission_sys.surf_success and tm_img:
                pygame.draw.rect(os_surf, (230, 230, 230), box)
                os_surf.blit(tm_img, (box.x, box.y + 30))
            else:
                pygame.draw.rect(os_surf, (240, 240, 240), box)
            
            pygame.draw.rect(os_surf, (200, 200, 200), (box.x, box.y, box.width, 30))
            pygame.draw.line(os_surf, GRAY, (box.x, box.y + 30), (box.x + box.width, box.y + 30), 2)
            pygame.draw.rect(os_surf, GRAY, box, 3)
            
            pygame.draw.circle(os_surf, RED, (box.x + 15, box.y + 15), 6)
            pygame.draw.circle(os_surf, YELLOW, (box.x + 35, box.y + 15), 6)
            pygame.draw.circle(os_surf, GREEN, (box.x + 55, box.y + 15), 6)
            
            if active_window != "MENU":
                btn_back = pygame.Rect(box.x + 75, box.y + 4, 60, 22)
                pygame.draw.rect(os_surf, GRAY, btn_back)
                pygame.draw.rect(os_surf, BLACK, btn_back, 1)
                t = small_font.render(get_text('back'), True, BLACK)
                os_surf.blit(t, (btn_back.x + 10, btn_back.y + 2))
                
            title_text = ""
            if active_window == "MENU":
                title_text = f"Console - {active_device.type} {active_device.id}"
            elif active_window == "IP":
                title_text = f"{get_text('ip_settings')} - {active_device.type}"
            elif active_window == "WEB":
                title_text = f"{get_text('web_browsing')} - {active_device.type}"
                
            tx = box.x + 150 if active_window != "MENU" else box.x + 80
            t = font.render(title_text, True, BLACK)
            os_surf.blit(t, (tx, box.y + 3))

            # Inner content
            if active_window == "MENU":
                bx, by = box.x + 50, box.y + 70
                options = []
                if active_device.type in ('PC', 'Laptop'):
                    options = [("IP Instellingen", "ip_instellingen.png"), ("Web Browsing", "web_browsing.png"), ("Terminal", "terminal.png")]
                else:
                    options = [("IP Instellingen", "ip_instellingen.png"), ("Restart", "restart.png"), ("Factory Reset", "factory_reset.png")]
                
                for name, icon_file in options:
                    r = pygame.Rect(bx, by, 100, 100)
                    pygame.draw.rect(os_surf, (220, 220, 220), r)
                    pygame.draw.rect(os_surf, GRAY, r, 2)
                    
                    icon = get_ext_icon(icon_file)
                    if icon:
                        os_surf.blit(icon, (bx + 20, by + 10))
                        
                    t = small_font.render(name, True, BLACK)
                    os_surf.blit(t, (bx + 50 - t.get_width()//2, by + 80))
                    bx += 130
                    
            elif active_window == "IP":
                t1 = font.render("IP Adres:", True, BLACK)
                os_surf.blit(t1, (WIDTH//2 - 200, HEIGHT//2 - 35))
                ip_input.draw(os_surf)
                
                t2 = font.render("Subnet:", True, BLACK)
                os_surf.blit(t2, (WIDTH//2 - 200, HEIGHT//2 + 35))
                subnet_input.draw(os_surf)
                
                btn_save = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 + 90, 100, 30)
                pygame.draw.rect(os_surf, (100, 200, 100), btn_save)
                pygame.draw.rect(os_surf, BLACK, btn_save, 2)
                st = font.render(get_text('save'), True, BLACK)
                os_surf.blit(st, (btn_save.x + 10, btn_save.y + 3))
                
            elif active_window == "WEB":
                if not mission_sys.surf_success:
                    t = font.render("URL:", True, BLACK)
                    os_surf.blit(t, (WIDTH//2 - 200, HEIGHT//2 - 25))
                    url_input.draw(os_surf)
                    
                    btn_go = pygame.Rect(WIDTH//2 + 150, HEIGHT//2, 80, 40)
                    pygame.draw.rect(os_surf, BLUE, btn_go)
                    pygame.draw.rect(os_surf, BLACK, btn_go, 2)
                    gt = font.render(get_text('go'), True, WHITE)
                    os_surf.blit(gt, (btn_go.x + 25, btn_go.y + 10))
                    
                    if mission_sys.popup_text:
                        color = (0, 150, 0) if mission_sys.surf_success else RED
                        txt = font.render(mission_sys.popup_text, True, color)
                        os_surf.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 + 70))
            
            os_surf.set_alpha(ui_alpha)
            screen.blit(os_surf, (0, 0))
        
        if sm.current != 'Start':
            mission_sys.check_conditions(devices, connections, packets)
            mission_sys.draw_mission_text(screen)
            mission_sys.draw_overlays(screen)
        sm.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
