import pygame
import os,sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pygame.init()

running = True
screen = pygame.display.set_mode((300, 400))

mb = pygame.image.load(resource_path("movement button.png"))
mb = pygame.transform.scale(mb, (100, 100))

size = pygame.font.SysFont(None, 50)
lsize = pygame.font.SysFont(None, 25)
allowed = "0123456789+-*/()=.^"

num = ""
button_rect = []
lans = 0

# Button layout (row-wise)
buttons = [
    ["7", "8", "9", "DEL", "AC"],
    ["4", "5", "6", "x", "÷"],
    ["1", "2", "3", "+", "–"],
    ["0", ".", "^", "Ans", "="]
]
# Pre-render text surfaces (IMPORTANT optimization)
text_surfaces = {}
for row in buttons:
    for item in row:
        font = lsize if item in ["DEL", "AC", "EXP", "Ans"] else size
        text_surfaces[item] = font.render(item, True, (255, 255, 255))

while running:
    pygame.display.set_caption("Calculator")
    screen.fill((51, 55, 66))

    # Display box
    pygame.draw.rect(screen, (161,161,161), (10,15,280,75), border_radius=5)
    pygame.draw.rect(screen, (0,0,0), (10,15,280,75), width=5, border_radius=5)

    # Draw buttons using loops
    start_x = 5
    start_y = 190
    btn_w, btn_h = 54, 47
    gap_x, gap_y = 59, 52
    button_rect = []

    for i, row in enumerate(buttons):
        for j, label in enumerate(row):
            x = start_x + j * gap_x
            y = start_y + i * gap_y

            # Special color for DEL and AC
            color = (160, 0, 0) if label in ["DEL", "AC"] else (160, 160, 160)
            button_rect.append(pygame.Rect(x,y,btn_w,btn_h))
            pygame.draw.rect(screen, color, (x, y, btn_w, btn_h), border_radius=5)

            # Center text
            text = text_surfaces[label]
            text_rect = text.get_rect(center=(x + btn_w//2, y + btn_h//2))
            screen.blit(text, text_rect)

    # Display input
    display = size.render(num, True, (255,255,255))
    screen.blit(display, (25, 40))

    # Image
    screen.blit(mb, (100, 85))
    if num.endswith("="):
        num = num.replace("x","*")
        num = num.replace("Ans",str(lans))
        num = num.replace("^","**")
        if all(ch in allowed for ch in num):
            num = num.replace("=","")
            num = str(eval(num, {"__builtins__": None}, {}))
            lans =num
        else:
            num = "Error"


    pygame.display.update()


    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                num = num[:-1]
            else:
                if event.unicode in allowed:
                    num += event.unicode
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button_sym,button_rect_rect in enumerate(button_rect):
                if button_rect_rect.collidepoint(event.pos):
                    button_row = button_sym//5
                    button_col = button_sym%5
                    button_num = buttons[button_row][button_col]
                    if button_num == "AC":
                        num = ""
                    elif button_num == "DEL":
                        num = num[:-1]
                    else:
                        num += button_num
                    break
pygame.quit() 