import pygame
import sys
from pattern_oblique import Pattern

def oblique_stripe():
	pygame.init()

	pattern = Pattern()
	screen = pygame.display.set_mode(pattern.screen_size)
	pygame.display.set_caption("Draw A Oblique Stripe")

	while True:
#		pattern.manual_set()					
		pattern.auto_move(screen) 
#		pattern.auto_move_right(screen)
		pattern.update_screen(screen)

oblique_stripe()		
