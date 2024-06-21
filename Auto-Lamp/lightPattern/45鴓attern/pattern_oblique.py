import pygame
import sys
import math

class Pattern():

	def __init__(self):
		self.bg_color = (255, 255, 255)
		self.stripe_color = (0, 0, 0)
		self.screen_size = 740, 740

		self.delay = delay =20
		self.y = y = 740 #改变左侧矩形条纹的y值，使整个图案上下移动
		self.move_step = move_step = 2  #改变条纹移动速度
		self.pt_size = pt_size = 40
		self.pt_size_step = pt_size_step = 4  #改变条纹的宽度，使整个图案变大或变小
		self.rect1_width = rect1_width = 270  #改变左侧矩形条纹的长度，使斜条纹左右移动
		self.ob_width = 200  #斜条纹的投影宽度不改动
		self.ob_height = ob_height = int(self.ob_width * math.tan(15/180 * math.pi))
		self.rect2_width = self.screen_size[0] - self.rect1_width - self.ob_width

		#绘制斜条纹的四个点坐标
		self.points = [(self.rect1_width, self.y), 
			(self.rect1_width, self.y + self.pt_size - 1), 
			(self.rect1_width + self.ob_width, self.y + self.pt_size - self.ob_height - 1),
			(self.rect1_width + self.ob_width, self.y - self.ob_height)]
		#两头两个矩形的绘制范围
		self.rect1_range = (0, self.y, self.rect1_width, self.pt_size)
		self.rect2_range = (self.rect1_width + self.ob_width, self.y - self.ob_height, 
							self.rect2_width, self.pt_size)
	
	def update_range(self):
		self.rect2_width = self.screen_size[0] - self.rect1_width - self.ob_width
		self.points = [(self.rect1_width, self.y), 
			(self.rect1_width, self.y + self.pt_size - 1), 
			(self.rect1_width + self.ob_width, self.y + self.pt_size - self.ob_height - 1),
			(self.rect1_width + self.ob_width, self.y - self.ob_height)]
		#两头两个矩形的绘制范围
		self.rect1_range = (0, self.y, self.rect1_width, self.pt_size)
		self.rect2_range = (self.rect1_width + self.ob_width, self.y - self.ob_height, 
							self.rect2_width, self.pt_size)
	#绘制整个条纹图案
	def draw_stripe(self, screen):
		pygame.draw.rect(screen, self.stripe_color, self.rect1_range, 0)
		pygame.draw.polygon(screen, self.stripe_color, self.points, 0)
		pygame.draw.rect(screen, self.stripe_color, self.rect2_range, 0)	

	def update_screen(self, screen):
		screen.fill(self.bg_color)
		self.draw_stripe(screen)
		pygame.display.flip()

	def move_up(self):
		self.y = self.y - self.move_step
		self.rect1_width = self.rect1_width - self.move_step
		self.update_range()

	def move_down(self):
		self.y = self.y + self.move_step
		self.rect1_width = self.rect1_width + self.move_step
		self.update_range()

	def move_left(self):
		self.rect1_width = self.rect1_width - self.move_step 
		self.update_range()

	def move_right(self):
		self.rect1_width = self.rect1_width + self.move_step
		self.update_range()

	def size_up(self):
		self.pt_size += self.pt_size_step
		self.update_range()

	def size_down(self):
		self.pt_size -= self.pt_size_step
		self.update_range()

	def speed_up(self):
		if self.delay > 50:
			self.delay -= 50 
		self.update_range()

	def speed_down(self):
		if self.delay < 300:
			self.delay += 50
		self.update_range()

	#关于条纹宽窄和移动速度和移动方向的手动键盘操作
	def manual_set(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_w:     #按'w'加宽条纹
					self.size_up()				
				elif event.key == pygame.K_s:	#按's'缩窄条纹
					self.size_down()
				elif event.key == pygame.K_a:	#按'a'加速移动条纹
					self.speed_up()
				elif event.key == pygame.K_d:	#按'd'减速移动条纹
					self.speed_down()
				elif event.key == pygame.K_UP:     #按'w'加宽条纹
					self.move_up()				
				elif event.key == pygame.K_DOWN:	#按's'缩窄条纹
					self.move_down()
				elif event.key == pygame.K_LEFT:	#按'a'加速移动条纹
					self.move_left()
				elif event.key == pygame.K_RIGHT:	#按'd'减速移动条纹
					self.move_right()			

	#条纹从下向上自动移动
	def auto_move(self, screen):
		mark = True
		while True:
			while mark and self.y - 3 * self.pt_size > 0:
				pygame.time.delay(self.delay)
				self.move_up()
				self.manual_set()
				#按'i'暂停自动移动模式，恢复手动
				keys = pygame.key.get_pressed()
				if keys[pygame.K_i]:
					mark = False
				self.update_screen(screen)

			#按'o'切换回自动移动模式
			keys = pygame.key.get_pressed()
			if keys[pygame.K_o]:
				mark = True

			self.manual_set()
			self.update_screen(screen)

	def auto_move_right(self, screen):
		mark = True
		while True:
			while mark and self.y - 3 * self.pt_size > 0:
				pygame.time.delay(self.delay)
				self.move_right()
				self.manual_set()
				#按'i'暂停自动移动模式，恢复手动
				keys = pygame.key.get_pressed()
				if keys[pygame.K_i]:
					mark = False
				self.update_screen(screen)

			#按'o'切换回自动移动模式
			keys = pygame.key.get_pressed()
			if keys[pygame.K_o]:
				mark = True

			self.manual_set()
			self.update_screen(screen)
