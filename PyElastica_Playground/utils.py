
def draw_text(screen, text, color, x, y, font):
    img = font.render(text, True, color)
    screen.blit(img, (x,y))
