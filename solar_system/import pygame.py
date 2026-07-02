import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# ─── Window Settings ───────────────────────────────────────
WIDTH, HEIGHT = 800, 800

# ─── Constants ─────────────────────────────────────────────
PI = math.pi

# ─── Time Control ──────────────────────────────────────────
time_speed = 1.0
# Camera controls
camera_x = 0.0
camera_y = 0.0
zoom = 1.0
# ─── Planet Data ───────────────────────────────────────────
# Each planet: [orbit_radius, size, speed, angle, R, G, B,
#               moon_orbit, moon_size, moon_speed, moon_angle, mR, mG, mB, name]
planets = [
    [0.18, 0.018, 4.7, 0.0,  0.6, 0.6, 0.6,  0.0,  0.0,   0.0, 0.0, 0.0, 0.0, 0.0, "Mercury"],
    [0.28, 0.030, 3.5, 0.0,  0.9, 0.7, 0.3,  0.0,  0.0,   0.0, 0.0, 0.0, 0.0, 0.0, "Venus"  ],
    [0.40, 0.035, 2.0, 0.0,  0.2, 0.5, 1.0,  0.06, 0.012, 5.0, 0.0, 0.8, 0.8, 0.8, "Earth"  ],
    [0.53, 0.025, 1.5, 0.0,  0.8, 0.3, 0.1,  0.0,  0.0,   0.0, 0.0, 0.0, 0.0, 0.0, "Mars"   ],
    [0.65, 0.075, 0.8, 0.0,  0.8, 0.6, 0.4,  0.10, 0.010, 4.0, 0.0, 0.7, 0.6, 0.5, "Jupiter"],
    [0.75, 0.060, 0.6, 0.0,  0.9, 0.8, 0.5,  0.09, 0.008, 3.5, 0.0, 0.9, 0.8, 0.6, "Saturn" ],
    [0.84, 0.040, 0.4, 0.0,  0.5, 0.8, 0.9,  0.0,  0.0,   0.0, 0.0, 0.0, 0.0, 0.0, "Uranus" ],
    [0.93, 0.038, 0.3, 0.0,  0.2, 0.3, 0.8,  0.0,  0.0,   0.0, 0.0, 0.0, 0.0, 0.0, "Neptune"],
]

# ─── Cached Font ───────────────────────────────────────────
system_font = None

# ─── Draw Filled Circle ────────────────────────────────────
def draw_circle(radius, r, g, b, segments=100):
    glColor3f(r, g, b)
    glBegin(GL_POLYGON)
    
    for i in range(segments + 1):
        angle = 2 * PI * i / segments
        glVertex2f(radius * math.cos(angle), radius * math.sin(angle))
    glEnd()

# ─── Draw Orbit Path ───────────────────────────────────────
def draw_orbit_path(radius, segments=100):
    glColor3f(0.25, 0.25, 0.25)
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        angle = 2 * PI * i / segments
        glVertex2f(radius * math.cos(angle), radius * math.sin(angle))
    glEnd()

# ─── Draw Saturn's Rings ───────────────────────────────────
def draw_rings(inner_r, outer_r, segments=100):
    glColor3f(0.8, 0.7, 0.4)
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(segments + 1):
        angle = 2 * PI * i / segments
        glVertex2f(outer_r * math.cos(angle), outer_r * math.sin(angle) * 0.3)
        glVertex2f(inner_r * math.cos(angle), inner_r * math.sin(angle) * 0.3)
    glEnd()

# ─── Draw Text Label ───────────────────────────────────────
def draw_text(surface, text, x, y):
    global system_font
    if system_font is None:
        system_font = pygame.font.SysFont("Arial", 12, bold=True)
        
    text_surface = system_font.render(text, True, (220, 220, 220))
    surface.blit(text_surface, (x, y))

# ─── World to Screen Coordinates ───────────────────────────
def world_to_screen(wx, wy):
    sx = int((wx + 1.0) / 2.0 * WIDTH)
    sy = int((1.0 - (wy + 1.0) / 2.0) * HEIGHT)
    return sx, sy

# ─── Display Function ──────────────────────────────────────
def display(surface):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Draw the Sun
    draw_circle(0.10, 1.0, 0.85, 0.0)

    # Label positions collected for pygame rendering
    labels = [("Sun", world_to_screen(0.10, 0.10))]

    for p in planets:
        orbit_r, size, speed, angle = p[0], p[1], p[2], p[3]
        r, g, b = p[4], p[5], p[6]
        moon_orbit, moon_size, moon_speed, moon_angle = p[7], p[8], p[9], p[10]
        mr, mg, mb = p[11], p[12], p[13]
        name = p[14]

        # Draw orbit path
        draw_orbit_path(orbit_r)

        # ── Push: move to planet position ─────────────────
        glPushMatrix()
        glRotatef(angle, 0, 0, 1)
        glTranslatef(orbit_r, 0.0, 0.0)

        # Saturn rings
        if name == "Saturn":
            draw_rings(size * 1.4, size * 2.2)

        draw_circle(size, r, g, b)

        # Collect label position in screen coords
        px = orbit_r * math.cos(math.radians(angle))
        py = orbit_r * math.sin(math.radians(angle))
        sx, sy = world_to_screen(px + size + 0.01, py + size + 0.01)
        labels.append((name, (sx + 5, sy - 5)))

        # ── Push: move to moon position ───────────────────
        if moon_orbit > 0.0:
            draw_orbit_path(moon_orbit)
            glPushMatrix()
            glRotatef(moon_angle, 0, 0, 1)
            glTranslatef(moon_orbit, 0.0, 0.0)
            draw_circle(moon_size, mr, mg, mb)
            glPopMatrix()
        # ── Pop: back to planet ───────────────────────────

        glPopMatrix()
        # ── Pop: back to sun ──────────────────────────────

    return labels

# ─── Update Angles ─────────────────────────────────────────
def update(dt):
    for p in planets:
        p[3] += p[2] * time_speed * dt * 30   
        p[10] += p[9] * time_speed * dt * 30  
        if p[3]  > 360: p[3]  -= 360
        if p[10] > 360: p[10] -= 360

# ─── Camera Update ─────────────────────────────────────────
def update_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    size = zoom
    # Calculate aspect ratio
    aspect = WIDTH / HEIGHT

    if aspect >= 1:
        glOrtho(
            -size * aspect + camera_x,
             size * aspect + camera_x,
            -size + camera_y,
             size + camera_y,
            -1,
             1
        )
    else:
        glOrtho(
            -size + camera_x,
             size + camera_x,
            -size / aspect + camera_y,
             size / aspect + camera_y,
            -1,
             1
        )
    glMatrixMode(GL_MODELVIEW)
# ─── Main Loop ─────────────────────────────────────────────
def main():
    global time_speed, system_font
    global camera_x, camera_y, zoom
    global WIDTH, HEIGHT
    pygame.init()
    pygame.font.init()

    # Create window with OpenGL support
    pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)
    screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    OPENGL | DOUBLEBUF | RESIZABLE
)
    pygame.display.set_caption("Solar System Simulator")

    # Overlay surface for text labels
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    # Set up OpenGL coordinate system
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0.0, 0.0, 0.05, 1.0)

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60) / 1000.0  

        # ── Handle Events ─────────────────────────────────
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h

                screen = pygame.display.set_mode(
                    (WIDTH, HEIGHT),
                    OPENGL | DOUBLEBUF | RESIZABLE
                )

                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

                glViewport(0, 0, WIDTH, HEIGHT)
            if event.type == KEYDOWN:
                if event.key == K_PLUS or event.key == K_EQUALS:
                    time_speed += 0.5
                if event.key == K_MINUS:
                    time_speed -= 0.5
                if event.key == K_r:
                    time_speed = 1.0
                        # Camera movement
                if event.key == K_LEFT:
                    camera_x -= 0.1

                if event.key == K_RIGHT:
                    camera_x += 0.1

                if event.key == K_UP:
                    camera_y += 0.1

                if event.key == K_DOWN:
                    camera_y -= 0.1

                # Zoom
                if event.key == K_z:
                    zoom -= 0.1
                    if zoom < 0.3:
                        zoom = 0.3

                if event.key == K_x:
                    zoom += 0.1
                if event.key == K_ESCAPE:
                    pygame.quit()
                    return
       # ── Update orbital angles ──────────────────────────
        update(dt)

       # ── Update camera ──────────────────────────────────
        update_camera()

       # ── Draw OpenGL scene ──────────────────────────────
        labels = display(screen)
        # ── Draw text labels using pygame overlay ──────────
        overlay.fill((0, 0, 0, 0))  
        for text, pos in labels:
            draw_text(overlay, text, pos[0], pos[1])

        # Controls hint
        if system_font is None:
            system_font = pygame.font.SysFont("Arial", 12, bold=True)
        hint = system_font.render(
    "+/- Speed   Arrows Move Camera   Z/X Zoom   R Reset   ESC Quit",
    True,
    (120, 120, 120)
)
        overlay.blit(hint, (10, HEIGHT - 25))
        

        # ── Blit overlay onto OpenGL window ────────────────
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        try:
            overlay_data = pygame.image.tobytes(overlay, "RGBA", True)
        except AttributeError:
            overlay_data = pygame.image.tostring(overlay, "RGBA", True)
            
        glRasterPos2f(-1.0, -1.0)
        glDrawPixels(WIDTH, HEIGHT, GL_RGBA, GL_UNSIGNED_BYTE, overlay_data)
        
        glDisable(GL_BLEND)
        # ───────────────────────────────────────────────────

        glFlush()
        pygame.display.flip()

if __name__ == "__main__":
    main()
