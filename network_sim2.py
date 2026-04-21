import pygame
import math
import sys
import os
import random

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Sprites V2")

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
current_lang = 'nl' # Alleen Nederlands

LANGS = {
    'nl': {
        'play': 'START SPEL',
        'quit': 'AFSLUITEN',
        'select_lang': 'TAAL: NEDERLANDS',
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
        'cat_straight': 'Straight-Through',
        'cat_cross': 'Crossover',
        'cat5e_label': 'Cat 5e Kabel',
        'wan_label': 'WAN Fiber',
        'error_len': 'Kabel te lang!',
        'error_ip': 'Fout: Router IP of Subnet incorrect.',
        'error_route': 'Fout: Geen route naar een Router.',
        'error_no_ip': 'Fout: PC heeft geen IP-adres.',
        'error_404': 'Fout: 404 Website niet gevonden.',
        'connecting': 'Verbinding maken...',
        'free_mode': 'Vrij Spel / Sandbox Mode',
        'extra_info': 'EXTRA UITLEG',
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
        'spacebar': 'SPATIE',
        'isp_provider': 'Internet Provider'
    }
}

def get_text(key):
    return LANGS['nl'].get(key, key)

CABLES = {
    'Cat 5':    {'color': (100, 200, 100), 'max_dist': 400, 'max_m': 100},
    'Cat 5e':   {'color': BLUE,            'max_dist': 800, 'max_m': 200},
    'Straight': {'color': GREEN,           'max_dist': 4000, 'max_m': 1000},
    'Crossover':{'color': (255, 128, 0),   'max_dist': 4000, 'max_m': 1000}, # Orange
    'WAN Fiber':{'color': YELLOW,          'max_dist': 2000,'max_m': 10000},
    'Wi-Fi':    {'color': CYAN,            'max_dist': 250, 'max_m': 30}
}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Network Simulation")
font = pygame.font.SysFont("Arial", 20, bold=True)
mission_font = pygame.font.SysFont("Arial", 24, bold=True)
small_font = pygame.font.SysFont("Arial", 16)

bg_road = None
try:
    bg_road = pygame.image.load(os.path.join(BASE_DIR, "Background", "background2.png")).convert()
    bg_road = pygame.transform.smoothscale(bg_road, (WIDTH, HEIGHT))
except Exception as e:
    pass

bg_level = None
try:
    bg_level = pygame.image.load(os.path.join(BASE_DIR, "Background", "background.png")).convert()
    bg_level = pygame.transform.smoothscale(bg_level, (WIDTH, HEIGHT))
except Exception as e:
    pass

gc_img = None
try:
    gc_img = pygame.image.load(os.path.join(BASE_DIR, "Icons", "GreenCircle.png")).convert_alpha()
except Exception as e:
    pass

arrow_img = None
try:
    img = pygame.image.load(os.path.join(BASE_DIR, "Icons", "arrow.png")).convert_alpha()
    arrow_img = pygame.transform.smoothscale(img, (80, 80))
except Exception as e:
    pass

# Global Game State
devices = []
connections = []
packets = []
mission_sys = None
current_mode = 'PC' 
current_cable = 'Straight'
sm = None

data_img = None
try:
    img = pygame.image.load(os.path.join(BASE_DIR, "Icons", "data.png")).convert_alpha()
    data_img = pygame.transform.smoothscale(img, (35, 35))
except Exception as e:
    pass

tm_img = None
try:
    img = pygame.image.load(os.path.join(BASE_DIR, "WebPages", "thomasmore.png")).convert_alpha()
    tm_img = pygame.transform.smoothscale(img, (500, 270))
except Exception as e:
    print(f"ERROR loading thomasmore.png: {e}")
    pass

def load_icon(folder, filename, size=(50, 50)):
    if '.' not in filename:
        for ext in ['.png', '.jpg', '.jpeg', '.webp']:
            filepath = os.path.join(BASE_DIR, folder, filename + ext)
            if os.path.exists(filepath):
                filename += ext
                break
                
    filepath = os.path.join(BASE_DIR, folder, filename)
    try:
        img = pygame.image.load(filepath).convert_alpha()
        return pygame.transform.smoothscale(img, size)
    except Exception as e:
        print(f"ERROR loading {filepath}: {e}")
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(surf, WHITE, (size[0]//2, size[1]//2), size[0]//2)
        return surf

ICONS = {
    'PC': load_icon("Gear", "pc.png"),
    'Laptop': load_icon("Gear", "laptop.png"),
    'Switch': load_icon("Gear", "switch.png"),
    'Router': load_icon("Gear", "router.png"),
    'Hub': load_icon("Gear", "hub.png"),
    'DELETE': load_icon("Icons", "delete.png"),
    'House1': load_icon("Houses", "huis1.png", size=(80, 80)),
    'House2': load_icon("Houses", "huis2.png", size=(80, 80)),
    'House3': load_icon("Houses", "huis3.png", size=(80, 80)),
    'House4': load_icon("Houses", "huis4.png", size=(80, 80)),
}

# --- GLOBAL UI BUTTONS ---
btn_modi = {
    'PC': pygame.Rect(10, 10, 80, 80),
    'Laptop': pygame.Rect(100, 10, 80, 80),
    'Switch': pygame.Rect(190, 10, 80, 80),
    'Hub': pygame.Rect(280, 10, 80, 80),
    'Router': pygame.Rect(370, 10, 80, 80),
    'DELETE': pygame.Rect(460, 10, 80, 80)
}
btn_data = pygame.Rect(550, 10, 80, 80)
btn_straight = pygame.Rect(820, 100, 170, 40)
btn_cross = pygame.Rect(820, 150, 170, 40)
btn_wan = pygame.Rect(820, 200, 170, 40)
btn_enter_house = pygame.Rect(10, 110, 180, 45) 
btn_to_world = pygame.Rect(20, HEIGHT//2 - 20, 220, 40)

EXT_ICONS = {}
def get_ext_icon(name):
    if name not in EXT_ICONS:
        filename = name
        if '.' not in filename:
            for ext in ['.png', '.jpg', '.webp']:
                if os.path.exists(os.path.join(BASE_DIR, "Icons", filename + ext)):
                    filename += ext
                    break
        try:
            img = pygame.image.load(os.path.join(BASE_DIR, "Icons", filename)).convert_alpha()
            EXT_ICONS[name] = pygame.transform.smoothscale(img, (60, 60))
        except Exception as e:
            print(f"ERROR loading ext icon {name}: {e}")
            surf = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.rect(surf, GRAY, (0,0,60,60))
            EXT_ICONS[name] = surf
    return EXT_ICONS[name]

class Device:
    counts = {"PC": 0, "Laptop": 0, "Switch": 0, "Router": 0, "Hub": 0, "House": 0}
    
    @classmethod
    def reset_counts(cls):
        cls.counts = {"PC": 0, "Laptop": 0, "Switch": 0, "Router": 0, "Hub": 0, "House": 0}

    def __init__(self, x, y, device_type, decorative=False):
        self.x = x
        self.y = y
        self.type = device_type
        self.decorative = decorative
        self.dhcp = False # DHCP state
        if not decorative:
            # Type-specifiek nummeren (PC1, RT1, etc)
            key = "House" if device_type.startswith("House") else device_type
            Device.counts[key] = Device.counts.get(key, 0) + 1
            self.name_idx = Device.counts[key]
        else:
            # Ook decoratieve huizen een nummer geven
            if device_type.startswith("House"):
                Device.counts["House"] = Device.counts.get("House", 0) + 1
                self.name_idx = Device.counts["House"]
            else:
                self.name_idx = 0
            
        self.id = random.randint(1000, 9999) # Unique ID for internal logic
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
        if self.type == 'PC': label = f"PC {self.name_idx}"
        elif self.type == 'Laptop': label = f"LAP {self.name_idx}"
        elif self.type == 'Switch': label = f"SW {self.name_idx}"
        elif self.type == 'Router': label = f"RT {self.name_idx}"
        elif self.type == 'Hub': label = f"HB {self.name_idx}"
        elif self.type.startswith('House'):
            # Geef alle huizen namen gebaseerd op hun positie (met int() voor robuustheid)
            ix, iy = int(self.x), int(self.y)
            if ix == 100: label = "Huis 1"
            elif ix == 300: label = "Huis 1" # Zoals gevraagd bovenste
            elif ix == 500: label = "Huis 3" # Zoals gevraagd bovenste
            elif ix == 700: label = "Huis 2" 
            elif ix == 900: label = "Huis 5"
            else: label = f"Huis {self.name_idx}"
            
            # Specifieke overschrijving voor Missie-huizen op top rij
            if iy == 280:
                if ix == 300: label = "Huis 1"
                elif ix == 500: label = "Huis 3"
        else: label = f"DEV {self.name_idx}"
            
        icon = ICONS.get(self.type)
        if icon:
            rect = icon.get_rect(center=(self.x, self.y))
            surface.blit(icon, rect.topleft)
        else:
            pygame.draw.circle(surface, GRAY, (self.x, self.y), self.radius)
            pygame.draw.circle(surface, WHITE, (self.x, self.y), self.radius, 2)
        
        text = font.render(label, True, WHITE)
        # Bovenste rij (y=280) label boven, onderste rij (y=415) label beneden om de weg te ontwijken
        if int(self.y) == 280:
            surface.blit(text, (self.x - text.get_width()//2, self.y - self.radius - 25))
        else:
            surface.blit(text, (self.x - text.get_width()//2, self.y + self.radius + 10))
        
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
        self.just_reached_node = False
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
                self.just_reached_node = True
                self.pause_frames = 12 # 0.2s at 60fps
                self.update_dist()

    def draw(self, surface):
        if self.reached or self.curr_idx >= len(self.path) - 1: return
        
        c1x, c1y = self.path[self.curr_idx].cable_c
        c2x, c2y = self.path[self.curr_idx+1].cable_c
        
        x = c1x + (c2x - c1x) * self.progress
        y = c1y + (c2y - c1y) * self.progress
        
        # Wi-Fi pulse effect: check if current segment uses Wi-Fi
        alpha = 255
        from_dev = self.path[self.curr_idx]
        to_dev = self.path[self.curr_idx + 1]
        for c in connections:
            if ((c.d1 == from_dev and c.d2 == to_dev) or
                (c.d2 == from_dev and c.d1 == to_dev)):
                if c.cable_type == 'Wi-Fi':
                    alpha = int(80 + 175 * abs(math.sin(pygame.time.get_ticks() * 0.008)))
                break
        
        if data_img:
            tmp = data_img.copy()
            tmp.set_alpha(alpha)
            rect = tmp.get_rect(center=(int(x), int(y)))
            surface.blit(tmp, rect.topleft)
        else:
            s = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 220, 0, alpha), (10, 10), 10)
            surface.blit(s, (int(x)-10, int(y)-10))

class SceneManager:
    def __init__(self):
        self.scenes = {
            'Start': {'devices': [], 'connections': [], 'packets': []},
            'Level1': {'devices': [], 'connections': [], 'packets': [], 'bg_img': 'lab_bg.png'},
            'House1': {'devices': [], 'connections': [], 'packets': [], 'bg_img': 'lab_bg.png'},
            'House2': {'devices': [], 'connections': [], 'packets': [], 'bg_img': 'lab_bg.png'},
            'World': {'devices': [], 'connections': [], 'packets': [], 'bg_img': 'wereldkaart_bg.png'},
            'Uitleg_Menu': {'devices': [], 'connections': [], 'packets': []}
        }
        self.current = 'Start'
        self.transition_alpha = 0
        self.transition_state = "NONE" # NONE, FADE_OUT, FADE_IN
        self.target_scene = None
        self.trans_text = ""
        self.uitleg_page = 0
        self.uitleg_pages = [
            ("Eindapparaten (End Devices)", "PC", [
                "PC & Laptop zijn de werkstations van gebruikers.",
                "Hier begint en eindigt het meeste dataverkeer.",
                "Laptops kunnen ook draadloos verbinden via Wi-Fi."
            ]),
            ("De Switch", "Switch", [
                "Verbindt apparaten binnen hetzelfde netwerk (LAN).",
                "Is 'slim': onthoudt welk apparaat op welke poort zit.",
                "Dit gebeurt op basis van unieke MAC-adressen."
            ]),
            ("De Router", "Router", [
                "Is de 'poortwachter' tussen verschillende netwerken.",
                "Verbindt jouw thuisnetwerk met het grote internet.",
                "Gebruikt IP-adressen om data de juiste weg te wijzen."
            ]),
            ("De Hub", "Hub", [
                "Een Hub is een dom apparaat dat alles doorstuurt naar iedereen.",
                "Het verdeelt de bandbreedte en veroorzaakt meer botsingen.",
                "Wordt tegenwoordig bijna niet meer gebruikt, we gebruiken nu Switches."
            ]),
            ("Kabels (Straight-Through)", "cat5e_straight", [
                "Straight-Through (Recht) gebruik je voor VERSCHILLENDE types.",
                "Bijvoorbeeld: PC naar Switch of Switch naar Router.",
                "Kleur in de game: Groen."
            ]),
            ("Kabels (Crossover)", "cat5_cross", [
                "Crossover (Gekruist) gebruik je voor DEZELFDE types.",
                "- Bijvoorbeeld: PC naar PC of Router naar Router.",
                "Kleur in de game: Oranje."
            ]),
            ("Data Pakketten", "data", [
                "De 'envelop' waarin jouw digitale bericht zit.",
                "Bevat o.a. de IP-adressen van verzender en ontvanger.",
                "Netwerkapparatuur leest dit om te weten waar het heen moet."
            ]),
            ("Broadcast", "broadcast", [
                "Een bericht dat naar ALLE apparaten wordt gestuurd.",
                "Nodig om onbekende apparaten te vinden in het netwerk.",
                "Een Switch stuurt dit door naar elke actieve poort."
            ]),
            ("Topologie (Ster vs Boom)", "topologie", [
                "Ster (Star): Alles zit op één centrale Switch.",
                "Boom (Tree): Meerdere Switches onderling verbonden.",
                "Boom-structuur kan veel meer apparaten aan."
            ]),
            ("IP Adres", "ip", [
                "Een unieke identificatie voor elk apparaat.",
                "Voorbeeld: 192.168.1.5",
                "Zonder IP kan een apparaat niet communiceren op internet."
            ]),
            ("Subnet Mask", "subnet", [
                "Bepaalt welk deel van het IP het netwerk is.",
                "Apparaten in hetzelfde subnet kunnen elkaar direct zien.",
                "Voorbeeld: 255.255.255.0"
            ]),
            ("Web Browsing", "web", [
                "Het bezoeken van websites via een browser.",
                "Werkt via URL's zoals www.thomasmore.be",
                "De router zorgt dat je de weg naar de website vindt."
            ])
        ]
        
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
        surface.blit(t_surf, (WIDTH//2 - t_surf.get_width()//2, 120))
        
        # Play / Quit / Extra Info Buttons (Vertically stacked)
        btn_play = pygame.Rect(WIDTH//2 - 100, 280, 200, 60)
        pygame.draw.rect(surface, (100, 200, 100), btn_play, border_radius=10)
        pygame.draw.rect(surface, WHITE, btn_play, 3, border_radius=10)
        p_txt = font.render(get_text('play'), True, WHITE)
        surface.blit(p_txt, (btn_play.centerx - p_txt.get_width()//2, btn_play.centery - p_txt.get_height()//2))
        
        btn_quit = pygame.Rect(WIDTH//2 - 100, 360, 200, 60)
        pygame.draw.rect(surface, (200, 100, 100), btn_quit, border_radius=10)
        pygame.draw.rect(surface, WHITE, btn_quit, 3, border_radius=10)
        q_txt = font.render(get_text('quit'), True, WHITE)
        surface.blit(q_txt, (btn_quit.centerx - q_txt.get_width()//2, btn_quit.centery - q_txt.get_height()//2))

        # Extra Uitleg Button
        btn_uitleg = pygame.Rect(WIDTH//2 - 100, 440, 200, 60)
        pygame.draw.rect(surface, (100, 100, 200), btn_uitleg, border_radius=10)
        pygame.draw.rect(surface, WHITE, btn_uitleg, 3, border_radius=10)
        u_txt = font.render(get_text('extra_info'), True, WHITE)
        surface.blit(u_txt, (btn_uitleg.centerx - u_txt.get_width()//2, btn_uitleg.centery - u_txt.get_height()//2))

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
        if self.current == 'Start':
            self.draw_start_screen(surface)
            
        if self.current == 'Uitleg_Menu':
            surface.fill((20, 20, 30))
            box = pygame.Rect(WIDTH//2 - 400, HEIGHT//2 - 250, 800, 500)
            # Tablet look
            pygame.draw.rect(surface, (40, 40, 60), box, border_radius=20)
            pygame.draw.rect(surface, (150, 150, 180), box, 8, border_radius=20) # Frame
            
            # Close button (top right of tablet)
            close_btn = pygame.Rect(box.right - 50, box.top + 20, 30, 30)
            pygame.draw.circle(surface, RED, close_btn.center, 15)
            pygame.draw.circle(surface, WHITE, close_btn.center, 15, 2)
            cross = font.render("X", True, WHITE)
            surface.blit(cross, (close_btn.centerx - cross.get_width()//2, close_btn.centery - cross.get_height()//2))

            if self.uitleg_page >= len(self.uitleg_pages): self.uitleg_page = 0
            page_title, icon_key, page_lines = self.uitleg_pages[self.uitleg_page]
            
            # Title
            t_surf = pygame.font.SysFont('Arial', 36, bold=True).render(page_title, True, CYAN)
            surface.blit(t_surf, (WIDTH//2 - t_surf.get_width()//2, box.top + 40))
            
            # Icon
            icon = None
            if icon_key in ICONS:
                icon = ICONS[icon_key]
            elif icon_key == "data" and data_img:
                icon = pygame.transform.smoothscale(data_img, (80, 80))
            elif icon_key == "cat5e_straight":
                # Draw procedural straight cable
                cx, cy = WIDTH//2, box.top + 130
                pygame.draw.line(surface, GREEN, (cx - 40, cy), (cx + 40, cy), 8)
                pygame.draw.rect(surface, GRAY, (cx - 45, cy - 8, 10, 16))
                pygame.draw.rect(surface, GRAY, (cx + 35, cy - 8, 10, 16))
            elif icon_key == "cat5_cross":
                # Draw procedural crossover cable
                cx, cy = WIDTH//2, box.top + 130
                pygame.draw.line(surface, (255, 128, 0), (cx - 40, cy - 10), (cx + 40, cy + 10), 6)
                pygame.draw.line(surface, (255, 128, 0), (cx - 40, cy + 10), (cx + 40, cy - 10), 6)
                pygame.draw.rect(surface, GRAY, (cx - 45, cy - 15, 10, 10))
                pygame.draw.rect(surface, GRAY, (cx - 45, cy + 5, 10, 10))
                pygame.draw.rect(surface, GRAY, (cx + 35, cy - 15, 10, 10))
                pygame.draw.rect(surface, GRAY, (cx + 35, cy + 5, 10, 10))
            elif icon_key in ["ip", "subnet"]:
                 icon = load_icon("Icons", "ip_instellingen.png", (80, 80))
            elif icon_key == "web":
                 icon = load_icon("Icons", "web_browsing.png", (80, 80))
            elif icon_key == "topologie":
                 # Fallback for topology: draw a simple star?
                 pygame.draw.circle(surface, CYAN, (WIDTH//2, box.top + 130), 20, 2)
                 for angle in range(0, 360, 72):
                     rad = math.radians(angle)
                     pygame.draw.line(surface, CYAN, (WIDTH//2, box.top + 130), (WIDTH//2 + math.cos(rad)*40, box.top + 130 + math.sin(rad)*40), 2)
            elif icon_key == "broadcast":
                 pygame.draw.circle(surface, YELLOW, (WIDTH//2, box.top + 130), 10)
                 pygame.draw.circle(surface, YELLOW, (WIDTH//2, box.top + 130), 25, 2)
                 pygame.draw.circle(surface, YELLOW, (WIDTH//2, box.top + 130), 40, 1)

            if icon:
                surface.blit(icon, (WIDTH//2 - icon.get_width()//2, box.top + 90))

            # Lines - Centered
            y = box.top + 200
            for line in page_lines:
                rend = font.render(line, True, WHITE)
                surface.blit(rend, (WIDTH//2 - rend.get_width()//2, y))
                y += 50
                
            # Navigation Arrows
            left_arrow = pygame.Rect(box.left + 20, box.centery - 30, 40, 60)
            right_arrow = pygame.Rect(box.right - 60, box.centery - 30, 40, 60)
            
            if self.uitleg_page > 0:
                pygame.draw.polygon(surface, WHITE, [(left_arrow.right, left_arrow.top), (left_arrow.left, left_arrow.centery), (left_arrow.right, left_arrow.bottom)])
            if self.uitleg_page < len(self.uitleg_pages) - 1:
                pygame.draw.polygon(surface, WHITE, [(right_arrow.left, right_arrow.top), (right_arrow.right, right_arrow.centery), (right_arrow.left, right_arrow.bottom)])
                
            # Page Indicator
            ind = font.render(f"Pagina {self.uitleg_page + 1} / {len(self.uitleg_pages)}", True, GRAY)
            surface.blit(ind, (WIDTH//2 - ind.get_width()//2, box.bottom - 40))
            

            
        if self.transition_alpha > 0:
            s = pygame.Surface((1000, 700), pygame.SRCALPHA)
            s.fill((0,0,0, min(255, max(0, self.transition_alpha))))
            if self.transition_alpha > 100:
                t = font.render(self.trans_text, True, (255,255,255))
                s.blit(t, (500 - t.get_width()//2, 350))
            surface.blit(s, (0,0))

class Mission:
    def __init__(self, text, m_type, target_pos=None, dev_type=None, radius=50, target_count=1):
        self.text = text
        self.type = m_type 
        self.target_pos = target_pos
        self.dev_type = dev_type
        self.radius = radius
        self.target_count = target_count

class MissionSystem:
    def __init__(self):
        self.level = 1
        self.fail_msg = ""
        self.fail_timer = 0
        self.surf_success = False
        self.popup_text = ""
        self.packets_delivered = 0
        self.packets_sent = 0  # counts every SPACE press attempt
        self.overlay_alpha = 0
        self.wifi_timer = 0
        self.setup_level()
        
    def setup_level(self):
        global current_cable
        Device.reset_counts()
        L = current_lang
        # Automatisch de juiste kabel selecteren voor het level
        if self.level == 1:
            current_cable = 'Cat 5'
        elif self.level == 2:
            current_cable = 'Cat 5'
        else:
            current_cable = 'Straight'

        if self.level == 1:
            self.missions = [
                Mission("Lees de start-introductie op het scherm.", "INTRO"),
                Mission("Dit is een PC. Gebruik deze voor vaste werkstations.\nKlik om door te gaan.", "L1_EXP_PC", target_pos=(51, 40)),
                Mission("Dit is een Laptop. Kan zowel met kabel als draadloos!\nKlik om door te gaan.", "L1_EXP_LAP", target_pos=(121, 40)),
                Mission("Dit is een Switch. Hiermee verbind je meerdere apparaten.\nKlik om door te gaan.", "L1_EXP_SW", target_pos=(191, 40)),
                Mission("Dit is een Hub. Een simpel hulpmiddel om PC's te koppelen.\nKlik om door te gaan.", "L1_EXP_HUB", target_pos=(261, 40)),
                Mission("Dit is een Router. De poort naar de rest van de wereld!\nKlik om door te gaan.", "L1_EXP_RT", target_pos=(331, 40)),
                Mission("Missie 1: Plaats een Hub in de cirkel.", "PLACE", target_pos=(500, 350), dev_type="Hub"),
                Mission("Missie 2: Plaats een PC aan de linkerkant.", "PLACE", target_pos=(200, 350), dev_type="PC"),
                Mission("Missie 3: Plaats een tweede PC.", "PLACE", target_pos=(200, 550), dev_type="PC"),
                Mission("TIP: Houd de linkermuisknop ingedrukt om kabels te trekken!\nKlik om door te gaan.", "L1_EXP_MOUSE"),
                Mission("Missie 4: Verbind beide PC's met de Hub.", "CONNECT"),
                Mission("Missie 5: Plaats een 3e PC ver weg aan de rechterkant.", "PLACE", target_pos=(900, 550), dev_type="PC"),
                Mission("Missie 6: Probeer PC3 met de Hub te verbinden.", "TRY_CONNECT"),
                Mission("Oeps! Kabel te kort. Lees de uitleg.", "EXPLANATION_CAT5"),
                Mission("Missie 7: Pak rechts de Cat 5e kabel.", "PICK_CAT5E"),
                Mission("Missie 8: Verbind PC3 met de Hub met de Cat 5e kabel.", "CONNECT_CAT5E"),
                Mission("Missie 9: Druk op SPATIE om data te sturen tussen de PC's via de hub!", "PACKET"),
                Mission("Level 1 voltooid! Lees de uitleg en klik op 'Volgende'.", "EXPLANATION_1")
            ]
        elif self.level == 2:
            self.packets_sent = 0
            self.missions = [
                Mission("Intro: We gaan nu met Internet werken!\nKlik om door te gaan.", "INTRO_L2"),
                Mission("Plaats een Router om als poort naar buiten te dienen.", "PLACE", target_pos=(500, 200), dev_type="Router"),
                Mission("Een router heeft een provider (ISP) nodig.\nKlik Router -> IP Instellingen -> Kies Proximus of Telenet.", "CONF_ISP"),
                Mission("Stel nu de lokale IP in: 192.168.1.1, Subnet Mask: 255.255.255.0\nKlik op Opslaan.", "CONF_ROUTER"),
                Mission("Mooi! Sluit het venster met de rode bol linksboven.", "CLOSE_WINDOW"),
                Mission("Plaats een PC in het lokale netwerk.", "PLACE", target_pos=(300, 400), dev_type="PC"),
                Mission("Verbind de PC met de Router middels een Cat 5 kabel.", "CONNECT_R"),
                Mission("Stel PC IP in: 192.168.1.2, Subnet Mask: 255.255.255.0\nKlik op Opslaan.", "CONF_PC"),
                Mission("Testen: Terug -> Web Browsing -> Typ 'www.thomasmore.be' -> Go!", "SURF"),
                Mission("Sluit het browservenster met het rode bolletje.", "CLOSE_WINDOW"),
                Mission("Bonus: Plaats een extra PC maar geef hem GEEN IP.", "PLACE", dev_type="PC", target_count=2),
                Mission("Verbind de nieuwe PC ook met de Router.", "CONNECT_R2"),
                Mission("Stuur een pakketje (SPATIE). Hij bereikt PC zonder IP NIET!", "L2_TEST_IP_FAIL"),
                Mission("Geef de nieuwe PC nu ook een IP (192.168.1.3).", "CONF_3_PCS"),
                Mission("Level 2 voltooid! Je begrijpt nu ISP, Gateways en IP-beveiliging.", "EXPLANATION_2")
            ]
        elif self.level == 3:
            global sm
            if 'sm' in globals() and sm is not None:
                sm.current = 'World'
                # Reset all scenes for a clean Level 3 start
                for s in sm.scenes.values():
                    s['devices'].clear()
                    s['connections'].clear()
                    s['packets'].clear()
                
                # Setup World Map with Houses (Bovenste rij zijn Huis 1 en Huis 3)
                w_sc = sm.scenes['World']
                house_types = ['House1', 'House2', 'House3', 'House4']
                w_sc['devices'].append(Device(100, 415, random.choice(house_types), decorative=True))
                w_sc['devices'].append(Device(300, 280, 'House1')) # Huis 1 (Interactief)
                w_sc['devices'].append(Device(500, 280, 'House2')) # Huis 3 (Interactief, type House2 voor mission)
                w_sc['devices'].append(Device(700, 415, random.choice(house_types), decorative=True))
                w_sc['devices'].append(Device(900, 415, random.choice(house_types), decorative=True))
            
            self.missions = [
                Mission("Welkom bij Level 3: Het verbinden van de wereld!\nKlik op Huis 1 en daarna op de knipperende 'HUIS BETREDEN' knop.", "L3_START_WORLD"),
                Mission("Plaats de eerste Router in Server Ruimte A (links).", "PLACE", target_pos=(250, 350), dev_type="Router"),
                Mission("Plaats de redundante Router in Server Ruimte B (rechts).", "PLACE", target_pos=(750, 350), dev_type="Router"),
                Mission("Verbind de 2 Routers eerst met een Straight kabel.", "L3_TRY_STRAIGHT"),
                Mission("Foutmelding: Klik op de rode box voor uitleg.", "EXPLANATION_CROSS"),
                Mission("Verbind de 2 Routers nu met de Crossover kabel.", "L3_CONNECT_CROSS"),
                Mission("Top! Plaats nu een Switch in het kantoor.", "PLACE", dev_type="Switch"),
                Mission("Plaats 2 PC's rondom de Switch.", "PLACE", dev_type="PC", target_count=2),
                Mission("Verbind: Router 1->Switch (Straight) en Switch->2x PC.", "L3_CONNECT_LAN"),
                Mission("Stel Router 1 in met ISP Telenet/Proximus.", "CONF_ISP"),
                Mission("Stel Router 1 IP in: 192.168.1.1, Subnet Mask: 255.255.255.0", "CONF_ROUTER"),
                Mission("Klik voor uitleg over DHCP (Dynamic Host Configuration Protocol).", "L3_EXPLAIN_DHCP"),
                Mission("Zet de DHCP Server 'AAN' in de instellingen van Router 1.", "L3_ENABLE_DHCP_SRV"),
                Mission("Zet DHCP aan op BEIDE PC's in hun IP-instellingen.", "L3_USE_DHCP"),
                Mission("Plaats een Laptop in het kantoor nabij de routers.\nDeze verbindt automatisch draadloos (Wi-Fi)!", "L3_PLACE_LAPTOP"),
                Mission("Huis 1 is klaar! We gaan nu terug naar de kaart...", "L3_TO_WORLD_1"),
                Mission("Wereldkaart: Selecteer Huis 3 en klik op 'HUIS BETREDEN'.", "L3_WORLD_2_IN"),
                Mission("Huis 3: Plaats een Router, Switch, 1 PC.\nVerbind: Router->Switch en Switch->PC.", "L3_BUILD_H2"),
                Mission("Huis 3 voltooid! Terug naar de Wereldkaart...", "L3_TO_WORLD_2"),
                Mission("Kies nu rechts de 'WAN Fiber' kabel.", "L3_PICK_WAN"),
                Mission("Verbind op de kaart Huis 1 en Huis 2 met de WAN kabel!", "L3_CONNECT_WAN"),
                Mission("Gefeliciteerd! Test de verbinding door een pakketje te sturen\ntussen de huizen met SPATIE.", "L3_SEND_P_WAN"),
                Mission("WAN Netwerk voltooid! Je bent nu in Free Mode.", "EXPLANATION_FIN"),
                Mission("Level 3 voltooid! Je bent nu in Free Mode.", "DONE")
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

    def draw_mission_text(self, surface, devices):
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
            # Ghost cable animation between PC1 and Hub
            pcs = [d for d in devices if d.type == 'PC']
            hubs = [d for d in devices if d.type == 'Hub']
            pc1 = next((d for d in pcs if d.name_idx == 1), None)
            hub = hubs[0] if hubs else None
            if pc1 and hub:
                s = abs(math.sin(pygame.time.get_ticks() * 0.005))
                alpha = int(100 + s * 155)
                temp_s = pygame.Surface((1000, 700), pygame.SRCALPHA)
                pygame.draw.line(temp_s, (255, 255, 0, alpha), (pc1.x, pc1.y), (hub.x, hub.y), 5)
                surface.blit(temp_s, (0,0))

        if mission.type == "PLACE" and mission.target_pos:
            if gc_img:
                scaled_gc = pygame.transform.smoothscale(gc_img, (mission.radius*2, mission.radius*2))
                rect = scaled_gc.get_rect(center=mission.target_pos)
                surface.blit(scaled_gc, rect.topleft)
            else:
                pygame.draw.circle(surface, (100, 255, 100), mission.target_pos, mission.radius, 3)

        if mission.type == "PICK_CAT5E":
            s = abs(math.sin(pygame.time.get_ticks() * 0.008)) # Blinking effect
            alpha = int(100 + s * 155)
            if arrow_img:
                flipped = pygame.transform.rotate(arrow_img, 180)
                # Drawing with blinking alpha (Surface needed)
                arrow_surf = pygame.Surface(flipped.get_size(), pygame.SRCALPHA)
                arrow_surf.blit(flipped, (0,0))
                arrow_surf.set_alpha(alpha)
                surface.blit(arrow_surf, (720, 130))
            else:
                color = (255, 255, 0, alpha)
                temp_arr = pygame.Surface((1000, 700), pygame.SRCALPHA)
                pygame.draw.line(temp_arr, color, (790, 170), (700, 170), 6)
                pygame.draw.polygon(temp_arr, color, [(700, 170), (720, 150), (720, 190)])
                surface.blit(temp_arr, (0,0))

        # Icon explanations in Level 1
        if mission.type.startswith("L1_EXP_") and mission.target_pos:
             px, py = mission.target_pos
             s = abs(math.sin(pygame.time.get_ticks() * 0.01))
             pygame.draw.polygon(surface, YELLOW, [(px, py + 35 + s*10), (px-10, py+55+s*10), (px+10, py+55+s*10)])

        # Blinking arrow for Crossover or Router placement in Level 3
        if mission.type in ("EXPLANATION_CROSS", "L3_CONNECT_CROSS"):
            s = abs(math.sin(pygame.time.get_ticks() * 0.01))
            px, py = btn_cross.x - 40 - s*10, btn_cross.y + 15
            pygame.draw.polygon(surface, YELLOW, [(px, py), (px-20, py-10), (px-20, py+10)])
            pygame.draw.rect(surface, YELLOW, (px-40, py-5, 20, 10))
        elif mission and "PLACE" in mission.type and getattr(mission, 'dev_type', '') == "Router":
            # Point to Router icon
            rb = btn_modi['Router']
            s = abs(math.sin(pygame.time.get_ticks() * 0.01))
            px, py = rb.x + 35, rb.y + 100 + s*10
            pygame.draw.polygon(surface, YELLOW, [(px, py), (px-10, py+20), (px+10, py+20)])
            pygame.draw.rect(surface, YELLOW, (px-5, py+20, 10, 20))

    def draw_overlays(self, surface, devices):
        if self.fail_timer > 0:
            surf = mission_font.render(self.fail_msg, True, RED, BLACK)
            surface.blit(surf, (WIDTH//2 - surf.get_width()//2, 110))
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
            
        elif mission and mission.type == "INTRO_L2":
            if self.overlay_alpha < 255: self.overlay_alpha = min(255, self.overlay_alpha + 15)
            ov_surf = pygame.Surface((1000, 700), pygame.SRCALPHA)
            box = pygame.Rect(500 - 350, 350 - 150, 700, 300)
            pygame.draw.rect(ov_surf, (40, 40, 50), box)
            pygame.draw.rect(ov_surf, GREEN, box, 3)
            
            lines = ["WELKOM BIJ LEVEL 2: HET INTERNET", "", "In dit level leer je hoe we een lokaal netwerk verbinden", "met de buitenwereld middels een Internet Service Provider (ISP).", "Denk aan Belgische providers zoals Proximus of Telenet.", "", "Je gaat een Router plaatsen en deze de juiste poort instellen.", "", "Klik in dit vak om te beginnen!"]
            y = box.y + 25
            for l in lines:
                surf = font.render(l, True, WHITE)
                ov_surf.blit(surf, (box.x + 350 - surf.get_width()//2, y))
                y += 28
                
            ov_surf.set_alpha(self.overlay_alpha)
            surface.blit(ov_surf, (0,0))
            
        elif mission and mission.type == "EXPLANATION_2":
            if self.overlay_alpha < 255: self.overlay_alpha = min(255, self.overlay_alpha + 15)
            ov_surf = pygame.Surface((1000, 700), pygame.SRCALPHA)
            box = pygame.Rect(500 - 350, 350 - 180, 700, 360)
            pygame.draw.rect(ov_surf, (20, 20, 40), box)
            pygame.draw.rect(ov_surf, CYAN, box, 3)
            
            lines = ["GEWELDIG! Level 2 succesvol afgerond.", "", "Je hebt nu een PC verbonden met een Router (Gateway).", "Je hebt ook een provider gekozen (ISP). Nu kan de PC", "data versturen naar 'www.thomasmore.be' en terug.", "", "Dit is de basis van hoe internet bij jou thuis werkt!", "", "Klik hier om naar Level 3 (Wereldkaart) te gaan!"]
            y = box.y + 25
            for l in lines:
                surf = font.render(l, True, WHITE)
                ov_surf.blit(surf, (box.x + 350 - surf.get_width()//2, y))
                y += 32
                
            ov_surf.set_alpha(self.overlay_alpha)
            surface.blit(ov_surf, (0,0))
            
        elif mission and mission.type == "L3_TO_WORLD_1":
            if self.overlay_alpha < 255: self.overlay_alpha = min(255, self.overlay_alpha + 15)
            ov_surf = pygame.Surface((1000, 700), pygame.SRCALPHA)
            box = pygame.Rect(500 - 350, 350 - 100, 700, 200)
            pygame.draw.rect(ov_surf, (40, 40, 50), box)
            pygame.draw.rect(ov_surf, GREEN, box, 3)
            
            lines = ["Huis 1 is nu lokaal volledig verbonden!", "", "Klik hier om uit te zoomen naar de buitenwereld..."]
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
            
            lines = ["Je bevindt je nu op de Wereldkaart!", "", "Hier zie je de buitenkant van de lokale netwerken die je bouwt.", "In de verte staat een tweede huis (Huis 2) met een leeg netwerk.", "", "Klik eerst in dit vak om door te gaan", "Klik daarna op de knop 'HUIS BETREDEN' links om in te gaan!"]
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
                'nl': ["Geweldig gedaan! Je hebt zojuist je eerste netwerk gebouwd met een Hub.", "", "Een Hub is een centraal punt waar alle kabels samenkomen.", "In dit level heb je geleerd hoe je apparaten fysiek verbindt", "en dat de afstand van de kabel (100m vs 200m) een grote rol speelt.", "Zonder de juiste kabel kan het signaal niet over een grote afstand!", "", "In het volgende level gaan we kijken naar IP-adressen en Routers.", "Dan gaan we pas echt het internet op!", "", "Klik hier ergens in het vak om naar Level 2 te gaan."],
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
            
            lines = ["PROFICIAT! Je hebt het WAN netwerk voltooid!", "", "Je hebt nu alle levels van de simulator doorlopen.", "Je weet hoe je apparaten plaatst, kabels trekt, IP's instelt", "en verbinding maakt tussen afgelegen locaties.", "", "Vanaf nu zit je in de FREE MODE / ENDLESS MODE.", "Je kunt nu vrij alle huizen verkennen, extra apparatuur bouwen", "en het hele wegennetwerk bekabelen zoals jij dat wilt!", "", "Klik hier om de sandbox mode te starten."]
            y = box.y + 20
            for l in lines:
                surf = font.render(l, True, WHITE)
                ov_surf.blit(surf, (box.x + 400 - surf.get_width()//2, y))
                y += 25
                
            ov_surf.set_alpha(self.overlay_alpha)
            surface.blit(ov_surf, (0,0))

        elif mission and mission.type == "EXPLANATION_CROSS":
            if self.overlay_alpha < 255: self.overlay_alpha = min(255, self.overlay_alpha + 15)
            ov_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            box = pygame.Rect(WIDTH//2 - 350, HEIGHT//2 - 180, 700, 360)
            pygame.draw.rect(ov_surf, (30, 30, 40), box)
            pygame.draw.rect(ov_surf, (200, 50, 50), box, 4)
            
            lines = [
                "FOUT: Je probeert twee routers te verbinden met een Straight kabel!",
                "",
                "Het belangrijkste verschil zit in de interne draden en de apparatuur:",
                "",
                "1. Straight-through: Draden aan beide kanten in DEZELFDE volgorde.",
                "   GEBRUIK: Verschillende apparaten (PC naar Switch, Router naar Switch).",
                "",
                "2. Crossover: Verzend- en ontvangstlijnen (TX/RX) aan één kant omgedraaid.",
                "   GEBRUIK: Zelfde apparaten (Router naar Router, Switch naar Switch).",
                "",
                "Klik hier om het opnieuw te proberen met de Crossover kabel."
            ]
            y = box.y + 15
            for l in lines:
                surf = font.render(l, True, WHITE)
                ov_surf.blit(surf, (box.x + 350 - surf.get_width()//2, y))
                y += 26
                
            ov_surf.set_alpha(self.overlay_alpha)
            surface.blit(ov_surf, (0,0))

        elif mission and mission.type == "L3_EXPLAIN_DHCP":
            if self.overlay_alpha < 255: self.overlay_alpha = min(255, self.overlay_alpha + 15)
            ov_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            box = pygame.Rect(WIDTH//2 - 350, HEIGHT//2 - 190, 700, 380)
            pygame.draw.rect(ov_surf, (30, 45, 60), box)
            pygame.draw.rect(ov_surf, CYAN, box, 4)
            
            lines = [
                "NIEUW CONCEPT: DHCP",
                "",
                "Handmatig IP-adressen invullen voor honderden PC's is veel werk.",
                "DHCP (Dynamic Host Configuration Protocol) lost dit op!",
                "",
                "- Een Router met DHCP-server deelt automatisch IP's uit aan apparaten.",
                "- Het bespaart tijd en voorkomt fouten (zoals dubbele IP's).",
                "",
                "In deze missie hoef je alleen DHCP 'AAN' te zetten op de PC's.",
                "De Router (die al een IP heeft) doet de rest van het werk!",
                "",
                "Klik hier om verder te gaan."
            ]
            y = box.y + 20
            for l in lines:
                surf = font.render(l, True, WHITE)
                ov_surf.blit(surf, (box.x + 350 - surf.get_width()//2, y))
                y += 28
            ov_surf.set_alpha(self.overlay_alpha)
            surface.blit(ov_surf, (0,0))

    def check_conditions(self, devices, connections, packets):
        mission = self.get_current()
        if not mission: return

        if mission.type == "PLACE":
            # Count the existing devices of this type
            existing_count = sum(1 for d in devices if d.type == mission.dev_type)
            target_count = getattr(mission, 'target_count', 1)
            
            if existing_count >= target_count:
                # If target_pos is specified, we must check if THEY are inside. 
                # (Simple check: if at least target_count are in their zones)
                if hasattr(mission, 'target_pos') and mission.target_pos:
                    # Specific spot placement logic
                    in_zone_count = 0
                    for d in devices:
                        if d.type == mission.dev_type:
                            dist = math.hypot(d.x - mission.target_pos[0], d.y - mission.target_pos[1])
                            if dist <= mission.radius:
                                in_zone_count += 1
                    if in_zone_count >= target_count:
                        self.advance()
                        return
                else:
                    # Free placement mission - just check the count
                    self.advance()
                    return
                        
        elif mission.type == "CONNECT":
            # Check if 2 PCs are connected to a Hub
            pc_hub_count = 0
            for c in connections:
                if c.is_valid:
                    types = {c.d1.type, c.d2.type}
                    if types == {'PC', 'Hub'}:
                        pc_hub_count += 1
            if pc_hub_count >= 2:
                self.advance()
                return
                    
        elif mission.type == "TRY_CONNECT":
            # Check if PC3 tried to connect to Hub
            for c in connections:
                if {c.d1.type, c.d2.type} == {'PC', 'Hub'}:
                    if c.distance > 400:
                        if c.cable_type == 'Cat 5e' and c.is_valid:
                            self.advance() # EXPLANATION_CAT5
                            self.advance() # PICK_CAT5E
                            self.advance() # CONNECT_CAT5E
                        else:
                            self.advance()
                        return
        elif mission.type == "PICK_CAT5E":
            if current_cable == 'Cat 5e':
                self.advance()
                return
        elif mission.type == "CONNECT_CAT5E":
            for c in connections:
                if c.is_valid and {c.d1.type, c.d2.type} == {'PC', 'Hub'}:
                    if c.distance > 400 and c.cable_type == 'Cat 5e':
                        self.advance()
                        return
        elif mission.type == "L2_LEAVE_EMPTY":
            p4 = next((d for d in devices if d.type == 'PC' and d.name_idx == 3), None)
            if p4 and not p4.ip:
                self.advance()
                return
        elif mission.type == "L2_TEST_IP_FAIL":
            # Advance as soon as the player has sent a packet (even if it was dropped)
            if mission_sys.packets_sent > 0:
                self.advance()
                return
        elif mission.type == "CONF_3_PCS":
            count = sum(1 for d in devices if d.type == 'PC' and d.ip and d.subnet)
            if count >= 2: self.advance()
        elif mission.type == "L2_FINAL_PACKET":
            if self.packets_delivered >= 2: self.advance() # 1 from start, 1 now
            for d in devices:
                if d.type == 'Router' and getattr(d, 'isp', None) in ("Proximus", "Telenet"):
                    self.advance()
                    return
        elif mission.type == "CONF_ISP":
            for d in devices:
                if d.type == 'Router' and getattr(d, 'isp', None) in ("Proximus", "Telenet"):
                    self.advance()
                    return
                        
        elif mission.type == "CONNECT_R":
            for c in connections:
                if c.is_valid and ((c.d1.type == 'PC' and c.d2.type == 'Router') or (c.d1.type == 'Router' and c.d2.type == 'PC')):
                    self.advance()
                    return

        elif mission.type == "CONNECT_R2":
            # Count all PC<->Router connections (need at least 2 for the bonus PC)
            pc_router_count = sum(
                1 for c in connections
                if c.is_valid and {c.d1.type, c.d2.type} == {'PC', 'Router'}
            )
            if pc_router_count >= 2:
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
        elif mission.type == "L3_CONNECT_CROSS":
            for c in connections:
                if c.is_valid and c.d1.type == 'Router' and c.d2.type == 'Router':
                    if c.cable_type == 'Crossover':
                        self.advance()
                        return
        elif mission.type == "L3_PLACE_LAPTOP":
            laptops = [d for d in devices if d.type == 'Laptop']
            if laptops:
                for l in laptops:
                    for c in connections:
                        if c.cable_type == 'Wi-Fi' and (c.d1 == l or c.d2 == l):
                            self.advance()
                            return
        elif mission.type == "L3_START_WORLD":
            if sm.current == 'House1' and sm.transition_state == "NONE":
                self.advance()
                return
                
        elif mission.type == "L3_WORLD_2_IN":
             if sm.current == 'House2' and sm.transition_state == "NONE":
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

        elif mission.type == "L3_EXPLAIN_DHCP":
             # Dismissed via click logic in loop (handled by overlay_alpha check)
             pass

        elif mission.type == "L3_USE_DHCP":
            pcs = [d for d in devices if d.type == 'PC']
            if len(pcs) >= 2 and all(d.dhcp for d in pcs):
                self.advance()
                return
            
        elif mission.type == "L3_WIFI_PLACE":
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
    global sm, mission_sys, devices, connections, packets, current_mode, current_cable, btn_modi
    sm = SceneManager()
    mission_sys = MissionSystem()
    
    # OS Inputs
    ip_input = TextInput(WIDTH//2 - 100, HEIGHT//2 - 40, 200, 30)
    subnet_input = TextInput(WIDTH//2 - 100, HEIGHT//2 + 30, 200, 30)
    url_input = TextInput(WIDTH//2 - 200, HEIGHT//2 + 5, 300, 30, default="www.")
    
    error_msg = ""
    error_timer = 0
    
    dragging = False
    drag_start_dev = None
    selected_house = None
    mouse_pos = (0, 0)
    mouse_press_tick = 0  # For hold-to-drag safety
    HOLD_THRESHOLD_MS = 700  # ms before it's considered a 'hold'
    
    active_device = None
    active_window = None # "MENU", "IP", "WEB"
    ui_alpha = 0
    
    debug_skip_timer = 0
    
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
            selected_house = None # Reset selectie bij terugkomst op kaart
            
        m = mission_sys.get_current()
                
        # Scene drawing
        if sm.current == 'World':
            if bg_road: 
                screen.blit(bg_road, (0, 0))
            else:
                screen.fill((40, 80, 40))
                pygame.draw.rect(screen, (60, 60, 60), (0, 300, 1000, 100))
                pygame.draw.line(screen, YELLOW, (0, 350), (1000, 350), 2)
        elif sm.current == 'Start':
            sm.draw_start_screen(screen)
        else:
            # Alle andere scènes (Level 1, Level 2, Huizen) gebruiken de kamer-achtergrond
            if bg_level:
                screen.blit(bg_level, (0, 0))
            else:
                screen.fill(BLACK)
        
        # --- House 1 Special Layout: Ground Floor (Level 3) ---
        if sm.current == 'House1' and mission_sys.level == 3:
            # Blueprint-style ground floor
            wc = (100, 100, 110) # Wall color
            # Outer walls
            pygame.draw.rect(screen, wc, (40, 110, 920, 560), 5)
            
            # Internal partitions
            # Horizontal corridor wall
            pygame.draw.line(screen, wc, (40, 320), (960, 320), 4)
            
            # Vertical walls for Server Rooms (Top row)
            pygame.draw.line(screen, wc, (340, 110), (340, 320), 4)
            pygame.draw.line(screen, wc, (660, 110), (660, 320), 4)
            
            # Room Labels
            r_font = pygame.font.SysFont("Arial", 18, bold=True)
            
            # Server Rooms
            s1 = r_font.render("SERVER ROOM A (SECURE)", True, (130, 130, 150))
            screen.blit(s1, (190 - s1.get_width()//2, 130))
            
            s2 = r_font.render("SERVER ROOM B (BACKUP)", True, (130, 130, 150))
            screen.blit(s2, (500 - s2.get_width()//2, 130))
            
            s3 = r_font.render("OPSLAG / TECH ROOM", True, (130, 130, 150))
            screen.blit(s3, (810 - s3.get_width()//2, 130))
            
            # Main Area
            main_a = r_font.render("OPEN KANTOOR / WERKRUIMTE", True, (130, 130, 150))
            screen.blit(main_a, (500 - main_a.get_width()//2, 450))
            
            # Corridor label
            corr = small_font.render("GANG / CORRIDOR", True, (100, 100, 100))
            screen.blit(corr, (500 - corr.get_width()//2, 295))

            # Doors (Gaps)
            pygame.draw.rect(screen, (30, 30, 35), (140, 315, 60, 10)) # Door to Room A
            pygame.draw.rect(screen, (30, 30, 35), (470, 315, 60, 10)) # Door to Room B
            pygame.draw.rect(screen, (30, 30, 35), (780, 315, 60, 10)) # Door to Tech
        
        # --- Visual feedback for selected house (World Map) ---
        if sm.current == 'World' and selected_house:
            # Pulsing ring around selected house
            s = abs(math.sin(pygame.time.get_ticks() * 0.01))
            alpha = int(100 + s * 155)
            pulse_surf = pygame.Surface((120, 120), pygame.SRCALPHA)
            pygame.draw.circle(pulse_surf, (100, 255, 100, alpha), (60, 60), 55, 4)
            screen.blit(pulse_surf, (selected_house.x - 60, selected_house.y - 60))
            
            # Hint text near button
            hint = font.render(f"<<< KLIK HIER OM {selected_house.type.upper()} TE BETREDEN!", True, YELLOW)
            # Add blinking to hint
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                screen.blit(hint, (230, 25))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if active_device and active_window == "IP":
                    # Only route to input boxes, not SPACE etc.
                    is_dhcp_on = active_device.type in ('PC', 'Laptop') and getattr(active_device, 'dhcp', False)
                    if not is_dhcp_on:
                        ip_input.handle_event(event)
                        subnet_input.handle_event(event)
                elif active_device and active_window == "WEB" and not mission_sys.surf_success:
                    url_input.handle_event(event)
                else:
                    if event.key == pygame.K_1: current_mode = 'PC'
                    elif event.key == pygame.K_2: current_mode = 'Laptop'
                    elif event.key == pygame.K_3: current_mode = 'Switch'
                    elif event.key == pygame.K_4: current_mode = 'Hub'
                    elif event.key == pygame.K_5: current_mode = 'Router'
                    elif event.key == pygame.K_d: current_mode = 'DELETE'
                    elif event.key == pygame.K_F3:
                        # DEBUG SKIP TO LEVEL 3
                        mission_sys.level = 3
                        mission_sys.setup_level()
                        sm.current = 'World'
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
                            routers = [d for d in devices if d.type == 'Router']
                            
                            if mission_sys.level >= 2 and routers:
                                internet_source = routers[0]
                                for ep in endpoints:
                                    path = find_path(devices, connections, internet_source, ep)
                                    if path and len(path) > 1:
                                        packets.append(PacketPath(path))
                                        mission_sys.packets_sent += 1
                                if mission and mission.type == "PACKET": pass
                            elif len(endpoints) >= 2:
                                start_pc = endpoints[0]
                                target_pc = endpoints[-1]
                                for d in endpoints:
                                    if d.x > target_pc.x: target_pc = d
                                
                                if target_pc != start_pc:
                                    path = find_path(devices, connections, start_pc, target_pc)
                                    if path and len(path) > 1:
                                        packets.append(PacketPath(path))
                                        mission_sys.packets_sent += 1
                                        if mission and mission.type == "PACKET": pass
                                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    # --- WORLD MAP SELECTION PRIORITY ---
                    if sm.current == 'World':
                        # 1. Confirm Enter
                        if btn_enter_house.collidepoint(event.pos):
                            if selected_house:
                                scene_name = selected_house.type
                                sm.start_transition(scene_name, f"Inzoomen op {scene_name}...")
                                current_cable = None 
                                selected_house = None 
                                continue
                        
                        # 2. Select House
                        clicked_house = False
                        for d in devices:
                            if d.type in ('House1', 'House2'):
                                if math.hypot(d.x - event.pos[0], d.y - event.pos[1]) < d.radius + 20:
                                    selected_house = d
                                    current_cable = None # Clear cable mode when selecting
                                    clicked_house = True
                                    break
                        if clicked_house:
                            continue

                    # START SCREEN CLICKS
                    if sm.current == 'Start':
                        # Play / Quit
                        btn_play = pygame.Rect(WIDTH//2 - 100, 280, 200, 60)
                        if btn_play.collidepoint(event.pos):
                            sm.start_transition("Level1", get_text('trans_zoom_in'))
                        
                        btn_quit = pygame.Rect(WIDTH//2 - 100, 360, 200, 60)
                        if btn_quit.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()
                            
                        btn_uitleg = pygame.Rect(WIDTH//2 - 100, 440, 200, 60)
                        if btn_uitleg.collidepoint(event.pos):
                            sm.start_transition("Uitleg_Menu", "")
                        continue
                        
                    # UITLEG MENU CLICKS
                    if sm.current == 'Uitleg_Menu':
                        box = pygame.Rect(WIDTH//2 - 400, HEIGHT//2 - 250, 800, 500)
                        # Close Button
                        close_btn = pygame.Rect(box.right - 50, box.top + 20, 30, 30)
                        if close_btn.collidepoint(event.pos):
                            sm.start_transition("Start", "")
                            continue
                        
                        # Pagination Arrows
                        left_arrow = pygame.Rect(box.left + 20, box.centery - 30, 40, 60)
                        right_arrow = pygame.Rect(box.right - 60, box.centery - 30, 40, 60)
                        if left_arrow.collidepoint(event.pos) and sm.uitleg_page > 0:
                            sm.uitleg_page -= 1
                        if right_arrow.collidepoint(event.pos) and sm.uitleg_page < len(sm.uitleg_pages) - 1:
                            sm.uitleg_page += 1
                        continue
                        
                    # Educational Overlays dismissal (Highest Priority, above OS)
                    mission = mission_sys.get_current()
                    if mission and sm.transition_state == "NONE":
                        if mission.type == "L3_EXPLAIN_DHCP":
                            box = pygame.Rect(WIDTH//2 - 350, HEIGHT//2 - 190, 700, 380)
                            if box.collidepoint(event.pos):
                                mission_sys.overlay_alpha = 0
                                mission_sys.advance()
                                continue
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
                                    house_types = ['House1', 'House2', 'House3', 'House4']
                                    sm.scenes['World']['devices'].append(Device(100, 415, random.choice(house_types), decorative=True))
                                    sm.scenes['World']['devices'].append(Device(300, 280, 'House1'))
                                    sm.scenes['World']['devices'].append(Device(500, 280, 'House2'))
                                    sm.scenes['World']['devices'].append(Device(700, 415, random.choice(house_types), decorative=True))
                                    sm.scenes['World']['devices'].append(Device(900, 415, random.choice(house_types), decorative=True))
                                mission_sys.advance()
                            continue
                        if mission.type == "L3_TO_WORLD_2":
                            box = pygame.Rect(150, 250, 700, 200)
                            if box.collidepoint(event.pos):
                                sm.start_transition("World", "Uitzoomen naar de Wereldkaart...")
                                mission_sys.advance()
                            continue
                    
                    # INTRO popup click handler (General)
                    if mission and mission.type in ("INTRO", "INTRO_L2", "EXPLANATION_2", "L1_EXP_PC", "L1_EXP_LAP", "L1_EXP_SW", "L1_EXP_HUB", "L1_EXP_RT", "L1_EXP_MOUSE"):
                        box = pygame.Rect(WIDTH//2 - 400, HEIGHT//2 - 200, 800, 400)
                        if box.collidepoint(event.pos):
                            mission_sys.advance()
                            continue

                    # OS WINDOW CLICKS
                    if active_device:
                        box = pygame.Rect(WIDTH//2 - 250, HEIGHT//2 - 150, 500, 300)
                        dist_to_red = math.hypot(event.pos[0] - (box.x + 15), event.pos[1] - (box.y + 15))
                        if dist_to_red <= 12:
                            active_device = None
                            active_window = None
                            mission = mission_sys.get_current()
                            if mission and mission.type == "CLOSE_WINDOW": mission_sys.advance()
                            continue
                            
                        btn_back = pygame.Rect(box.x + 75, box.y + 4, 60, 22)
                        if active_window != "MENU" and btn_back.collidepoint(event.pos):
                            active_window = "MENU"
                            ui_alpha = 0
                            continue
                            
                        if active_window == "MENU":
                            bx, by = box.x + 50, box.y + 70
                            options = [('ip_settings', "ip_instellingen.png"), ('web_browsing', "web_browsing.png"), ('terminal', "terminal.png")] if active_device.type in ('PC', 'Laptop') else [('ip_settings', "ip_instellingen.png"), ('restart', "restart.png"), ('reset', "factory_reset.png")]
                            for key, icon_file in options:
                                r = pygame.Rect(bx, by, 130, 130) # Vergroten naar 130x130
                                if r.collidepoint(event.pos):
                                    if key == "ip_settings":
                                        active_window = "IP"
                                        ui_alpha = 0
                                        ip_input.text = active_device.ip
                                        subnet_input.text = active_device.subnet
                                    elif key == "web_browsing" and active_device.type in ('PC', 'Laptop'):
                                        active_window = "WEB"
                                        ui_alpha = 0
                                        url_input.text = "www."
                                        mission_sys.surf_success, mission_sys.popup_text = False, ""
                                    elif key == "restart": active_device = active_window = None
                                    elif key == "reset": active_device.ip = active_device.subnet = ""
                                    break
                                bx += 145 # Grotere spacing
                        elif active_window == "IP":
                            # --- Router ISP buttons ---
                            if active_device.type == 'Router':
                                isp_btns = [("Proximus", WIDTH//2 - 30), ("Telenet", WIDTH//2 + 100)]
                                for isp_name, ix in isp_btns:
                                    ibtn = pygame.Rect(ix - 55, HEIGHT//2 - 115, 110, 30)
                                    if ibtn.collidepoint(event.pos):
                                        active_device.isp = isp_name
                                        mission = mission_sys.get_current()
                                        if mission and mission.type == "CONF_ISP": mission_sys.advance()
                                
                                # --- Router DHCP Server toggle (Level 3+) ---
                                if mission_sys.level >= 3:
                                    dhcp_srv_btn = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 85, 140, 32)
                                    if dhcp_srv_btn.collidepoint(event.pos):
                                        active_device.dhcp_srv = not getattr(active_device, 'dhcp_srv', False)
                                        m = mission_sys.get_current()
                                        if m and m.type == "L3_ENABLE_DHCP_SRV" and active_device.dhcp_srv:
                                            mission_sys.advance()

                            # --- PC/Laptop DHCP toggle (Level 3+) ---
                            if active_device.type in ('PC', 'Laptop') and mission_sys.level >= 3:
                                pc_dhcp_btn = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 - 105, 140, 32)
                                if pc_dhcp_btn.collidepoint(event.pos):
                                    active_device.dhcp = not getattr(active_device, 'dhcp', False)
                                    if active_device.dhcp:
                                        ip_input.text = ""
                                        subnet_input.text = ""
                                    else:
                                        ip_input.text = active_device.ip if active_device.ip else ""
                                        subnet_input.text = active_device.subnet if active_device.subnet else ""

                            # --- IP / Subnet text input (always for Router; blocked for PC if DHCP on) ---
                            is_dhcp_on = active_device.type in ('PC', 'Laptop') and getattr(active_device, 'dhcp', False)
                            if not is_dhcp_on:
                                ip_input.handle_event(event)
                                subnet_input.handle_event(event)

                            # --- Save button ---
                            save_btn = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 + 130, 100, 30)
                            if save_btn.collidepoint(event.pos) and not is_dhcp_on:
                                active_device.ip = ip_input.text
                                active_device.subnet = subnet_input.text
                                mission = mission_sys.get_current()
                                if mission and mission.type in ("CONF_ROUTER", "CONF_PC"): mission_sys.advance()
                        elif active_window == "WEB":
                            if not mission_sys.surf_success:
                                url_input.handle_event(event)
                                btn_go = pygame.Rect(WIDTH//2 + 150, HEIGHT//2, 80, 40)
                                if btn_go.collidepoint(event.pos):
                                    if url_input.text == "www.thomasmore.be":
                                        if active_device.ip:
                                            path = find_path_to_type(devices, connections, active_device, 'Router')
                                            if path and path[-1].ip:
                                                mission_sys.surf_success, mission_sys.popup_text = True, ""
                                                m = mission_sys.get_current()
                                                if m and m.type == "SURF": mission_sys.advance()
                                            else: mission_sys.popup_text = get_text('error_route') if not path else get_text('error_ip')
                                        else: mission_sys.popup_text = get_text('error_no_ip')
                                    else: mission_sys.popup_text = get_text('error_404')
                        continue # Block all background interaction when OS is open
                        
                    # Terug naar Wereldknop (Alleen in Huis 2!)
                    if sm.current == 'House2' and mission_sys.level == 3:
                        btn_to_world = pygame.Rect(20, HEIGHT//2 - 20, 220, 40)
                        if btn_to_world.collidepoint(event.pos):
                            sm.start_transition("World", "Terug naar het overzicht...")
            
                    # INTRO popup click handler (General)
                    if mission and mission.type in ("INTRO", "INTRO_L2", "L1_EXP_PC", "L1_EXP_LAP", "L1_EXP_SW", "L1_EXP_HUB", "L1_EXP_RT", "L1_EXP_MOUSE"):
                        box = pygame.Rect(WIDTH//2 - 400, HEIGHT//2 - 200, 800, 400)
                        if mission.type == "INTRO_L2":
                             box = pygame.Rect(500 - 350, 350 - 150, 700, 300)

                        if box.collidepoint(event.pos):
                            if mission.type == "EXPLANATION_2":
                                mission_sys.level = 3
                                mission_sys.overlay_alpha = 0
                                mission_sys.setup_level()
                                # sm.current is now 'World' (set by setup_level)
                            else:
                                mission_sys.advance()
                            continue

                    if mission and mission.type == "EXPLANATION_CAT5":
                        box = pygame.Rect(WIDTH//2 - 350, HEIGHT//2 - 180, 700, 360)
                        if box.collidepoint(event.pos):
                            mission_sys.advance()
                            continue
                    if mission and mission.type == "EXPLANATION_CROSS":
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
                    if btn_straight.collidepoint(event.pos):
                        current_cable = 'Cat 5' if mission_sys.level == 1 else 'Straight'
                        continue
                    if btn_cross.collidepoint(event.pos):
                        current_cable = 'Cat 5e' if mission_sys.level == 1 else 'Crossover'
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
                            routers = [d for d in devices if d.type == 'Router']
                            
                            if mission_sys.level >= 2 and routers:
                                internet_source = routers[0]
                                for ep in endpoints:
                                    path = find_path(devices, connections, internet_source, ep)
                                    if path and len(path) > 1:
                                        packets.append(PacketPath(path))
                                        mission_sys.packets_sent += 1
                                if m and m.type == "PACKET": pass
                            elif len(endpoints) >= 2:
                                start_pc = endpoints[0]
                                target_pc = endpoints[-1]
                                for d in endpoints:
                                    if d.x > target_pc.x: target_pc = d
                                if target_pc != start_pc:
                                    path = find_path(devices, connections, start_pc, target_pc)
                                    if path and len(path) > 1:
                                        packets.append(PacketPath(path))
                                        mission_sys.packets_sent += 1
                                        if m and m.type == "PACKET": pass
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
                        if btn_straight.collidepoint(event.pos):
                            current_cable = 'Straight'
                            continue
                        if btn_cross.collidepoint(event.pos):
                            current_cable = 'Crossover'
                            continue
                    else:
                        # WAN Fiber al hierboven afgehandeld
                        pass
                        
                    # Track when mouse was pressed (for hold safety)
                    mouse_press_tick = pygame.time.get_ticks()
                    
                    # Devices — larger hit radius for easier selection
                    clicked_dev = None
                    for d in reversed(devices):
                        if math.hypot(d.x - event.pos[0], d.y - event.pos[1]) < d.radius + 15:
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
                            # HOLD SAFETY: Only place device on short click (< HOLD_THRESHOLD_MS)
                            # Long holding = intending to drag a cable, not place a device.
                            # We set mouse_press_tick here but defer placement to MOUSEBUTTONUP.
                            pass  # device placement deferred to MOUSEBUTTONUP
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    held_ms = pygame.time.get_ticks() - mouse_press_tick
                    
                    # House selection on World Map (larger hit radius)
                    if sm.current == 'World' and not dragging and current_cable is None:
                        for d in devices:
                            if d.type in ('House1', 'House2'):
                                if math.hypot(d.x - event.pos[0], d.y - event.pos[1]) < d.radius + 20:
                                    selected_house = d
                                    break
                    
                    if btn_enter_house.collidepoint(event.pos) and selected_house and sm.current == 'World' and not dragging and current_cable is None:
                        sm.start_transition(selected_house.type, get_text('trans_zoom_in'))
                        current_cable = 'Cat 5'
                        continue

                    if dragging and drag_start_dev:
                        target_dev = None
                        for d in devices:
                            if math.hypot(d.x - event.pos[0], d.y - event.pos[1]) < d.radius + 20: # +20px extra margen
                                target_dev = d
                                break
                                
                        if target_dev == drag_start_dev:
                            # Opende het OS (NIET in Level 1!)
                            if sm.current != 'World' and mission_sys.level > 1:
                                active_device = drag_start_dev
                                active_window = "MENU"
                                ui_alpha = 0
                        elif target_dev:
                            # Verbinding
                            dist = math.hypot(drag_start_dev.cable_c[0] - target_dev.cable_c[0], drag_start_dev.cable_c[1] - target_dev.cable_c[1])
                            mission = mission_sys.get_current()
                            if mission and mission.type == "TRY_CONNECT":
                                if dist > CABLES['Straight']['max_dist'] and current_cable == 'Straight':
                                    mission_sys.advance() 
                                    
                            exists = False
                            for c in connections:
                                if (c.d1 == drag_start_dev and c.d2 == target_dev) or (c.d2 == drag_start_dev and c.d1 == target_dev):
                                    exists = True
                                    c.cable_type = current_cable
                                    c.update_validity()
                                    break

                            if not exists and current_cable in CABLES:
                                # Forgiving connection distance check
                                max_d = CABLES[current_cable]['max_dist']
                                if dist <= max_d + 10: # Extra bit of leeway
                                    valid_cable = True
                                    dev1 = drag_start_dev.type
                                    dev2 = target_dev.type
                                    
                                    # Alleen vanaf Level 3 controleren we op Straight vs Crossover
                                    if mission_sys.level >= 3 and current_cable in ('Straight', 'Crossover'):
                                        type1 = 'EndDevice' if dev1 in ('PC', 'Laptop', 'Server') else dev1
                                        type2 = 'EndDevice' if dev2 in ('PC', 'Laptop', 'Server') else dev2
                                        
                                        if type1 == type2:
                                            # Zelfde types -> Moet Crossover zijn
                                            if current_cable != 'Crossover':
                                                valid_cable = False
                                                error_msg = "Foute kabel! Gebruik CROSSOVER voor gelijke apparaten."
                                                error_timer = 240
                                                m = mission_sys.get_current()
                                                if m and m.type == "L3_TRY_STRAIGHT": mission_sys.advance()
                                        else:
                                            # Verschillende types -> Moet Straight zijn
                                            if current_cable != 'Straight':
                                                valid_cable = False
                                                error_msg = "Foute kabel! Gebruik STRAIGHT voor verschillende apparaten."
                                                error_timer = 240
                                    
                                    if valid_cable:
                                        connections.append(Connection(drag_start_dev, target_dev, current_cable))
                                        mission_sys.fail_timer = 0 
                                    
                                    if not valid_cable:
                                        # Show cable error via mission system
                                        mission_sys.fail_msg = error_msg
                                        mission_sys.fail_timer = 180
                                else:
                                    miss = mission_sys.get_current()
                                    if miss and miss.type == "TRY_CONNECT":
                                        mission_sys.advance()
                                    else:
                                        msg = get_text('error_len')
                                        mission_sys.fail_msg = f"{msg} {CABLES[current_cable]['max_m']}m"
                                        mission_sys.fail_timer = 180
                                
                    dragging = False
                    drag_start_dev = None
                    
                    # ====================================================
                    # DEFERRED DEVICE PLACEMENT (held < HOLD_THRESHOLD_MS)
                    # ====================================================
                    if not dragging and held_ms < HOLD_THRESHOLD_MS and sm.current not in ('World', 'Start', 'Uitleg_Menu') and current_mode and current_mode != 'DELETE':
                        # Check nothing was clicked and it wasn't a toolbar hit
                        clicked_anything = False
                        if active_device: clicked_anything = True
                        for r in btn_modi.values():
                            if r.collidepoint(event.pos): clicked_anything = True
                        if btn_data.collidepoint(event.pos): clicked_anything = True
                        if btn_straight.collidepoint(event.pos): clicked_anything = True
                        if btn_cross.collidepoint(event.pos): clicked_anything = True
                        if btn_wan.collidepoint(event.pos): clicked_anything = True
                        for d in devices:
                            if math.hypot(d.x - event.pos[0], d.y - event.pos[1]) < d.radius + 15:
                                clicked_anything = True
                                break
                        
                        if not clicked_anything and event.pos[1] > 100:
                            mission = mission_sys.get_current()
                            # Placement safety check
                            if mission and ("PLACE" in mission.type):
                                # If the mission type contains 'PLACE' (e.g., PLACE, L3_PLACE_2RT, L3_PLACE_PC)
                                if (hasattr(mission, 'dev_type') and mission.dev_type) and current_mode != mission.dev_type:
                                    mission_sys.fail_msg = f"FOUT: Plaats een {mission.dev_type}, geen {current_mode}."
                                    mission_sys.fail_timer = 180
                                else:
                                    # If it has a target radius, check it
                                    if hasattr(mission, 'target_pos') and mission.target_pos and hasattr(mission, 'radius'):
                                        dist_to_target = math.hypot(event.pos[0] - mission.target_pos[0], event.pos[1] - mission.target_pos[1])
                                        if dist_to_target > mission.radius:
                                            mission_sys.fail_msg = "Oeps verkeerd geklikt! Plaats het object IN de cirkel."
                                            mission_sys.fail_timer = 180
                                            new_dev = None
                                        else:
                                            new_dev = Device(event.pos[0], event.pos[1], current_mode)
                                            devices.append(new_dev)
                                    else:
                                        # Free placement (no specific circle) but restricted to correct type
                                        new_dev = Device(event.pos[0], event.pos[1], current_mode)
                                        devices.append(new_dev)
                            elif mission and mission.type not in ("DONE", "FREE"):
                                # If there is an active mission but it's NOT a placement mission
                                mission_sys.fail_msg = "Hellaaa dat was de opdracht niet! Eerst de huidige taak afmaken."
                                mission_sys.fail_timer = 180
                            else:
                                # Free mode or non-restrictive mission phases
                                new_dev = Device(event.pos[0], event.pos[1], current_mode)
                                devices.append(new_dev)
                                if current_mode == 'Laptop':
                                    for d in devices:
                                        if d.type == 'Router':
                                            dist = math.hypot(d.x - new_dev.x, d.y - new_dev.y)
                                            if dist < CABLES['Wi-Fi']['max_dist']:
                                                connections.append(Connection(new_dev, d, 'Wi-Fi'))
                                                mission_sys.wifi_timer = 90
                                                break
                    
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                
            
        # --- RENDERING ---
        
        # 1. Connections & Dragging Line
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
                start_x, start_y = c1x + math.cos(angle) * d1_dist, c1y + math.sin(angle) * d1_dist
                pygame.draw.line(screen, color, (start_x, start_y), mouse_pos, 4)
                msg_too_long = "Too long!" if current_lang == 'en' else "Trop long!" if current_lang == 'fr' else "Te lang!"
                msg_max = "Max" if current_lang != 'nl' else "Max"
                
                # Als de kabel een enorme limiet heeft (1000m+), toon geen Max label
                if max_m >= 1000:
                    text_str = f"{dist_m}m"
                else:
                    text_str = f"{msg_too_long} {dist_m}m / {max_m}m" if drag_dist > max_dist else f"{dist_m}m ({msg_max} {max_m}m)"
                
                text = small_font.render(text_str, True, RED if drag_dist > max_dist else WHITE)
                screen.blit(text, (mouse_pos[0] + 10, mouse_pos[1] + 10))

        # 2. Packets
        new_packets = []
        pending_broadcasts = []
        for p in packets:
            p.update()
            
            # --- IP Security Check (Level 2+) ---
            # Packet dropt als het DOEL-apparaat geen IP heeft
            if mission_sys.level >= 2:
                dest = p.path[-1]
                if not dest.ip and dest.type in ('PC', 'Laptop'):
                    p.reached = True  # silently drop packet
                    continue
            
            p.draw(screen)
            
            if p.just_reached_node:
                p.just_reached_node = False
                reached_dev = p.path[p.curr_idx]
                if reached_dev.type == 'Hub':
                    # Hub Broadcast Logic
                    prev_dev = p.path[p.curr_idx - 1]
                    next_dev = p.path[p.curr_idx + 1] if p.curr_idx < len(p.path)-1 else None
                    
                    # Find all connected neighbors
                    for c in connections:
                        if c.is_valid:
                            other = None
                            if c.d1 == reached_dev: other = c.d2
                            elif c.d2 == reached_dev: other = c.d1
                            
                            if other and other != prev_dev and other != next_dev:
                                # Send a ghost/side packet to this neighbor
                                # If it's a 1-hop path, it just reaches it and dies
                                side_p = PacketPath([reached_dev, other])
                                pending_broadcasts.append(side_p)

            if not p.reached:
                new_packets.append(p)
            else:
                mission_sys.packets_delivered += 1
        
        packets = new_packets + pending_broadcasts
        curr['packets'] = packets

        for d in devices: d.draw(screen, sm.current)
        
        # World Map extra visuals (Road & Street)
        if sm.current == 'World':
            # Draw the road itself
            pygame.draw.rect(screen, (50, 50, 55), (0, 320, WIDTH, 60)) # Asphalt
            pygame.draw.rect(screen, (70, 70, 75), (0, 315, WIDTH, 5))  # Top shoulder
            pygame.draw.rect(screen, (70, 70, 75), (0, 380, WIDTH, 5))  # Bottom shoulder
            # Lane marking (dashed)
            for x in range(0, WIDTH, 60):
                pygame.draw.line(screen, WHITE, (x, 350), (x + 30, 350), 2)
            
            # Label
            st_font = pygame.font.SysFont(None, 45, bold=True)
            st_shad = st_font.render("Stationsstraat", True, BLACK)
            screen.blit(st_shad, (32, 282))
            st_txt = st_font.render("Stationsstraat", True, YELLOW)
            screen.blit(st_txt, (30, 280))
            
            # Highlight selected house
            if selected_house:
                pygame.draw.circle(screen, YELLOW, (selected_house.x, selected_house.y), selected_house.radius + 15, 3)
                # Pulse highlight shadow
                s = abs(math.sin(pygame.time.get_ticks() * 0.005))
                pygame.draw.circle(screen, YELLOW, (selected_house.x, selected_house.y), selected_house.radius + 15 + s*5, 1)

        # Laptop Wi-Fi Placement Guide
        if current_mode == 'Laptop' and sm.current != 'World' and sm.current != 'Start':
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
        show_main_ui = sm.current != 'Start'
        curr_m = mission_sys.get_current()
        # Only hide UI during full-screen overlays/intros
        if curr_m and (curr_m.type == 'INTRO' or curr_m.type.startswith('EXPLANATION') or curr_m.type in ('L3_TO_WORLD_1', 'L3_WORLD_1', 'L3_TO_WORLD_2')):
            show_main_ui = False
            
        if show_main_ui:
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
                    num_map = {'PC': '1', 'Laptop': '2', 'Switch': '3', 'Hub': '4', 'Router': '5'}
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
            
            # Level 1 & 2: Show Cat 5 + Cat 5e; Level 3+: Show Straight + Crossover
            level_low = (mission_sys.level <= 2 and sm.current != 'World')
            if level_low:
                cable_btns = [(btn_straight, 'Cat 5'), (btn_cross, 'Cat 5e')]
            else:
                cable_btns = [(btn_straight, 'Straight'), (btn_cross, 'Crossover'), (btn_wan, 'WAN Fiber')]
            
            for btn, name in cable_btns:
                # Restriction: Only WAN Fiber on World map, No WAN Fiber in House
                if sm.current == 'World' and name != 'WAN Fiber': continue
                if sm.current != 'World' and name == 'WAN Fiber': continue
                
                btn_color = (60, 60, 60) if current_cable != name else (100, 200, 100)
                pygame.draw.rect(screen, btn_color, btn)
                pygame.draw.rect(screen, WHITE, btn, 2)
                lbl_key = 'cat_straight' if name in ('Straight', 'Cat 5') else 'cat_cross' if name in ('Crossover', 'Cat 5e') else 'wan_label'
                label = 'Cat 5' if name == 'Cat 5' else 'Cat 5e' if name == 'Cat 5e' else get_text(lbl_key)
                t = font.render(label, True, WHITE)
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
                # Blinking logic for the button if a house is selected
                if selected_house:
                    s_blink = abs(math.sin(pygame.time.get_ticks() * 0.01))
                    btn_alpha = int(100 + s_blink * 155)
                    color = (100, 255, 100, btn_alpha)
                    # Support for transparent rectangle drawing
                    btn_s = pygame.Surface((btn_enter_house.width, btn_enter_house.height), pygame.SRCALPHA)
                    pygame.draw.rect(btn_s, color, (0, 0, btn_enter_house.width, btn_enter_house.height), 0, 5)
                    screen.blit(btn_s, (btn_enter_house.x, btn_enter_house.y))
                else:
                    pygame.draw.rect(screen, (60, 60, 80), btn_enter_house, 0, 5)
                
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
                    options = [('ip_settings', "ip_instellingen.png"), ('web_browsing', "web_browsing.png"), ('terminal', "terminal.png")]
                else:
                    options = [('ip_settings', "ip_instellingen.png"), ('restart', "restart.png"), ('reset', "factory_reset.png")]
                
                for key, icon_file in options:
                    r = pygame.Rect(bx, by, 130, 130)
                    pygame.draw.rect(os_surf, (220, 220, 220), r)
                    pygame.draw.rect(os_surf, GRAY, r, 2)
                    
                    icon = get_ext_icon(icon_file)
                    if icon:
                        os_surf.blit(icon, (bx + 35, by + 15))
                    
                    # Label (Localized)
                    lbl = font.render(get_text(key), True, BLACK)
                    os_surf.blit(lbl, (bx + 65 - lbl.get_width()//2, by + 90))
                    
                    bx += 145
                    
            elif active_window == "IP":
                cy = HEIGHT//2  # center Y of the box

                # --- PC/Laptop: DHCP toggle ABOVE IP inputs ---
                if mission_sys.level >= 3 and active_device.type in ('PC', 'Laptop'):
                    is_dhcp = getattr(active_device, 'dhcp', False)
                    dhcp_lbl = font.render("DHCP:", True, BLACK)
                    os_surf.blit(dhcp_lbl, (WIDTH//2 - 200, cy - 105))
                    btn_dhcp = pygame.Rect(WIDTH//2 + 20, cy - 110, 140, 32)
                    pygame.draw.rect(os_surf, (0, 180, 0) if is_dhcp else (160, 50, 50), btn_dhcp, 0, 6)
                    pygame.draw.rect(os_surf, BLACK, btn_dhcp, 2, 6)
                    dhcp_st = font.render("Actief" if is_dhcp else "Niet Actief", True, WHITE)
                    os_surf.blit(dhcp_st, (btn_dhcp.x + btn_dhcp.width//2 - dhcp_st.get_width()//2, btn_dhcp.y + 6))

                # --- Router ISP buttons ---
                if active_device.type == 'Router':
                    ti = font.render(f"{get_text('isp_provider')}:", True, BLACK)
                    os_surf.blit(ti, (WIDTH//2 - 220, cy - 110))
                    isp_btns = [("Proximus", WIDTH//2 - 30), ("Telenet", WIDTH//2 + 100)]
                    for name, ix in isp_btns:
                        ibtn = pygame.Rect(ix - 55, cy - 115, 110, 30)
                        is_sel = getattr(active_device, 'isp', None) == name
                        pygame.draw.rect(os_surf, GREEN if is_sel else (180, 180, 180), ibtn)
                        pygame.draw.rect(os_surf, BLACK, ibtn, 1)
                        tn = small_font.render(name, True, BLACK)
                        os_surf.blit(tn, (ibtn.x + ibtn.width//2 - tn.get_width()//2, ibtn.y + 5))

                # --- IP Address input ---
                t1 = font.render("IP Adres:", True, BLACK)
                os_surf.blit(t1, (WIDTH//2 - 200, cy - 35))

                # Gray out inputs if PC DHCP is active
                is_dhcp_on = active_device.type in ('PC', 'Laptop') and getattr(active_device, 'dhcp', False)
                if is_dhcp_on:
                    pygame.draw.rect(os_surf, (210, 210, 210), (WIDTH//2 - 100, cy - 40, 200, 30))
                    auto_txt = small_font.render("Automatisch via DHCP", True, (100, 100, 100))
                    os_surf.blit(auto_txt, (WIDTH//2 - 100, cy - 32))
                    pygame.draw.rect(os_surf, (210, 210, 210), (WIDTH//2 - 100, cy + 30, 200, 30))
                    os_surf.blit(auto_txt.copy(), (WIDTH//2 - 100, cy + 38))
                else:
                    ip_input.draw(os_surf)

                # --- Subnet mask input ---
                t2 = font.render("Subnet Mask:", True, BLACK)
                os_surf.blit(t2, (WIDTH//2 - 200, cy + 35))
                if not is_dhcp_on:
                    subnet_input.draw(os_surf)

                # --- Router: DHCP Server toggle BELOW subnet (Level 3+) ---
                if mission_sys.level >= 3 and active_device.type == 'Router':
                    is_srv = getattr(active_device, 'dhcp_srv', False)
                    srv_lbl = font.render("DHCP Server:", True, BLACK)
                    os_surf.blit(srv_lbl, (WIDTH//2 - 200, cy + 85))
                    btn_srv = pygame.Rect(WIDTH//2 + 20, cy + 80, 140, 32)
                    pygame.draw.rect(os_surf, (0, 120, 200) if is_srv else (160, 50, 50), btn_srv, 0, 6)
                    pygame.draw.rect(os_surf, BLACK, btn_srv, 2, 6)
                    srv_st = font.render("Actief" if is_srv else "Niet Actief", True, WHITE)
                    os_surf.blit(srv_st, (btn_srv.x + btn_srv.width//2 - srv_st.get_width()//2, btn_srv.y + 6))

                # --- Save button ---
                btn_save = pygame.Rect(WIDTH//2 - 50, cy + 130, 100, 30)
                if not is_dhcp_on:
                    pygame.draw.rect(os_surf, (100, 200, 100), btn_save)
                    pygame.draw.rect(os_surf, BLACK, btn_save, 2)
                    st = font.render(get_text('save'), True, BLACK)
                    os_surf.blit(st, (btn_save.x + btn_save.width//2 - st.get_width()//2, btn_save.y + 5))

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
            # --- DHCP Background Logic (Level 3+) ---
            if mission_sys.level >= 3:
                for d in devices:
                    if d.type in ('PC', 'Laptop') and d.dhcp:
                        # Zoek verbinding met een Router
                        path = find_path_to_type(devices, connections, d, 'Router')
                        if path and path[-1].ip:
                             # Gevonden! Geef automatisch een IP (gebaseerd op index voor uniekheid)
                             d.ip = f"192.168.1.{10 + d.name_idx}"
                             d.subnet = "255.255.255.0"
                        else:
                             # Geen DHCP server (Router) gevonden
                             d.ip = "Searching..."
                             d.subnet = "---"
            
            mission_sys.check_conditions(devices, connections, packets)
            mission_sys.draw_mission_text(screen, devices)
            mission_sys.draw_overlays(screen, devices)
        sm.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
