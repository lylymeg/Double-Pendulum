import pygame
import math
import sys

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Double Pendulum Chaos Simulation")
clock = pygame.time.Clock()

# Couleurs (Fond sombre, néons vibrants)
DARK_BG = (10, 12, 18)
ROD_COLOR = (80, 95, 120)
BALL_COLOR = (0, 210, 255)
TIP_COLOR = (255, 140, 0)
WHITE = (255, 255, 255)
GRAY = (120, 130, 150)

# Paramètres du pendule double
cx, cy = WIDTH // 2, HEIGHT // 2 - 50
l1 = 160  # Longueur du bras 1
l2 = 140  # Longueur du bras 2
m1 = 20   # Masse 1
m2 = 20   # Masse 2

# Angles initiaux
theta1 = math.pi / 2
theta2 = math.pi / 2
omega1 = 0.0  # Vitesse angulaire 1
omega2 = 0.0  # Vitesse angulaire 2

g = 1.0       # Gravité

# Surface pour garder la mémoire des traînées lumineuses
trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Polices
font_medium = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 15)

prev_x2, prev_y2 = None, None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Réinitialiser la simulation avec de nouveaux angles aléatoires
                theta1 = math.pi / random.uniform(0.8, 1.5)
                theta2 = math.pi / random.uniform(0.8, 1.5)
                omega1, omega2 = 0.0, 0.0
                trail_surface.fill((0, 0, 0, 0))
                prev_x2, prev_y2 = None, None

    # --- PHYSIQUE DU PENDULE DOUBLE (Équations différentielles de Lagrange) ---
    # Calcul des accélérations angulaires (alpha1, alpha2)
    num1 = -g * (2 * m1 + m2) * math.sin(theta1) - m2 * g * math.sin(theta1 - 2 * theta2) - 2 * math.sin(theta1 - theta2) * m2 * (omega2**2 * l2 + omega1**2 * l1 * math.cos(theta1 - theta2))
    den1 = l1 * (2 * m1 + m2 - m2 * math.cos(2 * theta1 - 2 * theta2))
    alpha1 = num1 / den1

    num2 = 2 * math.sin(theta1 - theta2) * (omega1**2 * l1 * (m1 + m2) + g * (m1 + m2) * math.cos(theta1) + omega2**2 * l2 * m2 * math.cos(theta1 - theta2))
    den2 = l2 * (2 * m1 + m2 - m2 * math.cos(2 * theta1 - 2 * theta2))
    alpha2 = num2 / den2

    # Mise à jour des vitesses et des angles
    omega1 += alpha1
    omega2 += alpha2
    theta1 += omega1
    theta2 += omega2

    # Amortissement léger pour stabiliser l'énergie sur le long terme
    omega1 *= 0.9995
    omega2 *= 0.9995

    # Calcul des coordonnées cartésiennes des deux masses
    x1 = cx + l1 * math.sin(theta1)
    y1 = cy + l1 * math.cos(theta1)

    x2 = x1 + l2 * math.sin(theta2)
    y2 = y1 + l2 * math.cos(theta2)

    # --- RENDU GRAPHIQUE ---
    screen.fill(DARK_BG)

    # Dessiner la traînée de l'extrémité du pendule sur la surface persistante
    if prev_x2 is not None and prev_y2 is not None:
        pygame.draw.line(trail_surface, (255, 140, 0, 180), (prev_x2, prev_y2), (x2, y2), 2)
    prev_x2, prev_y2 = x2, y2

    # Effacer légèrement le vieux tracé pour garder un effet de fondu artistique
    trail_surface.fill((0, 0, 0, 2), special_flags=pygame.BLEND_RGBA_SUB)
    screen.blit(trail_surface, (0, 0))

    # Dessiner les bras du pendule
    pygame.draw.line(screen, ROD_COLOR, (cx, cy), (x1, y1), 4)
    pygame.draw.line(screen, ROD_COLOR, (x1, y1), (x2, y2), 4)

    # Dessiner les articulations et masses
    pygame.draw.circle(screen, WHITE, (cx, cy), 6)
    pygame.draw.circle(screen, BALL_COLOR, (int(x1), int(y1)), 10)
    pygame.draw.circle(screen, TIP_COLOR, (int(x2), int(y2)), 12)

    # --- HUD ET INSTRUCTIONS ---
    title_txt = font_medium.render("SIMULATION DE PENDULE DOUBLE — THÉORIE DU CHAOS", True, WHITE)
    screen.blit(title_txt, (WIDTH // 2 - title_txt.get_width() // 2, 15))

    inst_txt = font_small.render("Système dynamique non linéaire | R : Réinitialiser avec de nouveaux angles", True, GRAY)
    screen.blit(inst_txt, (WIDTH // 2 - inst_txt.get_width() // 2, 45))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()