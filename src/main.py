import requests
import random
import pygame
import pygame.gfxdraw
import csv
import time

from config import Config

data_dict = {}
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

def csv_to_dict(csv_file_path, key_column, value_column):
   result_dict = {}
   print(csv_file_path)

   with open(csv_file_path, 'r', newline='') as file:
      csv_reader = csv.DictReader(file)

      for row in csv_reader:
         key = row[key_column]
         value = float(row[value_column])

         result_dict[key] = value

   return result_dict

def csv_to_dict_spe(csv_file_path, key_column, value_column):
   result_dict = {}
   print(csv_file_path)

   with open(csv_file_path, 'r', newline='') as file:
      csv_reader = csv.DictReader(file)

      for row in csv_reader:
         key = row[key_column]
         value = row[value_column]

         result_dict[key] = value

   return result_dict
def draw_rounded_rect(surface, rect, color, corner_radius):
    pygame.draw.rect(surface, color, rect.inflate(-2*corner_radius, 0))
    pygame.draw.rect(surface, color, rect.inflate(0, -2*corner_radius))
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

def guess(text, screen, color, random_country_data1, random_country_data2, choice, correct):
    answer = my_font.render(text, False, color)
    answer_rect = answer.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 3/4 + 100))
    rect_1 = pygame.Rect(0, 0, 0, 0)
    rect_2 = pygame.Rect(0, 0, 0, 0)
    temp_rect_1_size = 0
    temp_rect_2_size = 0
    rect_1_size = (float(random_country_data1) / ((float(random_country_data1) + 0.001) + float(random_country_data2))) * SCREEN_HEIGHT / 2
    rect_2_size = (float(random_country_data2) / ((float(random_country_data1) + 0.001) + float(random_country_data2))) * SCREEN_HEIGHT / 2
    trans_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT * 2/4))
    trans_surface.fill((128, 128, 128))
    trans_surface.set_alpha(128)
    screen.blit(trans_surface, (0, 170))
    while (temp_rect_1_size < rect_1_size or temp_rect_2_size < rect_2_size):
        if (temp_rect_1_size < rect_1_size):
            temp_rect_1_size += 1
        if (temp_rect_2_size < rect_2_size):
            temp_rect_2_size += 1

        rect_1 = pygame.Rect(0,                - 100 + (SCREEN_HEIGHT * 3/4 - temp_rect_1_size + 1), SCREEN_WIDTH / 2, temp_rect_1_size)
        rect_2 = pygame.Rect(SCREEN_WIDTH/2, - 100 + (SCREEN_HEIGHT * 3/4 - temp_rect_2_size + 1), SCREEN_WIDTH / 2, temp_rect_2_size)

        pygame.draw.rect(screen, (0, 0, 0), rect_2)
        pygame.draw.rect(screen, (0, 0, 0), rect_1)
        pygame.display.flip()
    answer_1 = my_font.render(str(random_country_data1), False, (255, 255, 255))
    answer_2 = my_font.render(str(random_country_data2), False, (255, 255, 255))
    answer_1_rect = answer_1.get_rect(center=(SCREEN_WIDTH/4, SCREEN_HEIGHT/2 - 100))
    answer_2_rect = answer_2.get_rect(center=(SCREEN_WIDTH/4 * 3, SCREEN_HEIGHT/2 - 100))

    if (choice == 2 and correct == True) or (choice == 1 and correct == False):
        pygame.draw.rect(screen, (255, 0, 0), rect_1)
        pygame.draw.rect(screen, (0, 255, 0), rect_2)
    elif (choice == 2 and correct == False) or (choice == 1 and correct == True):
        pygame.draw.rect(screen, (0, 255, 0), rect_1)
        pygame.draw.rect(screen, (255, 0, 0), rect_2)
    else:
        pygame.draw.rect(screen, (0, 0, 255), rect_1)
        pygame.draw.rect(screen, (0, 0, 255), rect_2)
    draw_rounded_rect(screen, answer_1_rect, (20, 20, 20), 10)
    draw_rounded_rect(screen, answer_2_rect, (20, 20, 20), 10)
    screen.blit(answer_1, answer_1_rect)
    screen.blit(answer_2, answer_2_rect)
    screen.blit(answer, answer_rect)
    pygame.display.flip()
    time.sleep(1)

def check_choice(random_country_data1, random_country_data2, i, choice, screen):

    if choice == 1 and random_country_data1 > random_country_data2:
        guess("Youre right!", screen, (0, 255, 0), random_country_data1, random_country_data2, choice, 1)
    elif choice == 2 and random_country_data1 < random_country_data2:
        guess("Youre right!", screen, (0, 255, 0), random_country_data1, random_country_data2, choice, 1)
    elif random_country_data2 == random_country_data1:
        guess("Both are equals!", screen, (0, 0, 255), random_country_data1, random_country_data2, choice, 2)
    else:
        guess(f"Rip bozo youre wrong!, Youre streak is: {i - 1}", screen, (255, 0, 0), random_country_data1, random_country_data2, choice, 0)
        return 0
    return i

def check_invert_choice(random_country_data1, random_country_data2, i, choice, screen):

    if choice == 1 and random_country_data1 < random_country_data2:
        guess("You're right!", screen, (0, 255, 0), random_country_data1, random_country_data2, choice, 1)
    elif choice == 2 and random_country_data1 > random_country_data2:
        guess("You're right!", screen, (0, 255, 0), random_country_data1, random_country_data2, choice, 1)
    elif random_country_data2 == random_country_data1:
        guess("Both are equals!", screen, (0, 0, 255), random_country_data1, random_country_data2, choice, 2)
    else:
        guess(f"Rip bozo youre wrong!, Youre streak is: {i - 1}", screen, (255, 0, 0), random_country_data1, random_country_data2, choice, 0)
        return 0
    return i

def main_menu(screen, streak):
   start_rect = pygame.Rect(250, 700, 500, 150)
   quit_rect = pygame.Rect(1200, 700, 500, 150)
      
   while (True):
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            return False
         if event.type == pygame.MOUSEBUTTONDOWN:
            if (start_rect.collidepoint(event.pos)):
               return True
            if (quit_rect.collidepoint(event.pos)):
               return False
      
      screen.fill((20, 20, 20))
      pygame.draw.rect(screen, (255, 255, 255), start_rect)
      start_text = my_font = pygame.font.SysFont('Assets/Dosis-Bold.ttf', 100).render("START", False, (0,0,0))
      start_text_rect = start_text.get_rect(center=(500, 780))
      screen.blit(start_text, start_text_rect)
      pygame.draw.rect(screen, (255, 255, 255), quit_rect)
      quit_text = my_font = pygame.font.SysFont('Assets/Dosis-Bold.ttf', 100).render("QUIT", False, (0,0,0))
      quit_text_rect = quit_text.get_rect(center=(1450, 780))
      screen.blit(quit_text, quit_text_rect)
      
      home_text = my_font = pygame.font.SysFont('Assets/Dosis-Bold.ttf', 100).render("Welcome to Randle", False, (255,255,255))
      home_text_rect = home_text.get_rect(center=(SCREEN_WIDTH / 2, 200))
      screen.blit(home_text, home_text_rect)
      Title_text = my_font = pygame.font.SysFont('Assets/Dosis-Bold.ttf', 100).render("Make your choice beetween countries info", False, (255,255,255))
      Title_text_rect = Title_text.get_rect(center=(SCREEN_WIDTH / 2, 350))
      screen.blit(Title_text, Title_text_rect)
      Streak_text = my_font = pygame.font.SysFont('Assets/Dosis-Bold.ttf', 100).render("Your best streak is " + str(streak), False, (255,255,255))
      Streak_text_rect = Streak_text.get_rect(center=(SCREEN_WIDTH / 2, 500))
      screen.blit(Streak_text, Streak_text_rect)

      pygame.display.flip()
   

def loop(my_font, country_dict):
   pygame.init()
   screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
   clock = pygame.time.Clock()
   running = True
   new = True
   best_streak = 0
   i = 0

   random_field = None
   random_country_name1 = None
   random_country_name2 = None
   random_country_data1 = None
   random_country_data2 = None
   answer1_pic_rect = None
   answer2_pic_rect = None

   while running:

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            running = False

         if event.type == pygame.MOUSEBUTTONDOWN:
            if (answer1_pic_rect.collidepoint(event.pos)):
               new = True
               if Config.INVERT[random_field]:
                  i = check_invert_choice(random_country_data1, random_country_data2, i, 1, screen)
               else:
                  i = check_choice(random_country_data1, random_country_data2, i, 1, screen)
            if (answer2_pic_rect.collidepoint(event.pos)):
               new = True
               if Config.INVERT[random_field]:
                  i = check_invert_choice(random_country_data1, random_country_data2, i, 2, screen)
               else:
                  i = check_choice(random_country_data1, random_country_data2, i, 2, screen)

      if (i - 1 > best_streak):
         best_streak = i - 1

      if (i == 0):
         running = main_menu(screen, best_streak)

      if (new == False):
         continue

      try:
         random_field = random.choice(Config.DATAS)
         random_country_name1, random_country_data1 = random.choice(list(data_dict[random_field].items()))
         random_country_name2, random_country_data2 = random.choice(list(data_dict[random_field].items()))
         country_dict[random_country_name1]
         country_dict[random_country_name2]
      except Exception:
         continue

      screen.fill((20, 20, 20))
      question = my_font.render("Which has more " + random_field + " ?", False, (255, 255, 255))
      answer1 = my_font.render("1- " + random_country_name1, False, (255, 255, 255))
      answer2 = my_font.render("2- " + random_country_name2, False, (255, 255, 255))

      answer1_pic = None
      answer2_pic = None

      try:
         answer1_pic = requests.get("http://www.geognos.com/api/en/countries/flag/" + country_dict[random_country_name1] + ".png")
         answer2_pic = requests.get("http://www.geognos.com/api/en/countries/flag/" + country_dict[random_country_name2] + ".png")
         if (answer1_pic.status_code != 200 or answer2_pic.status_code != 200):
            continue
         answer1_pic = answer1_pic.content
         answer2_pic = answer2_pic.content
      except Exception:
         continue

      with open("image1.png", "wb") as f:
         f.write(answer1_pic)
      with open("image2.png", "wb") as f:
         f.write(answer2_pic)

      answer1_pic = pygame.image.load("image1.png")
      answer2_pic = pygame.image.load("image2.png")
      answer1_pic = pygame.transform.scale(answer1_pic, (960, 540))
      answer2_pic = pygame.transform.scale(answer2_pic, (960, 540))

      question_rect = question.get_rect(center=(SCREEN_WIDTH/2, 100))
      answer1_rect = answer1.get_rect(center=(960 / 2, SCREEN_HEIGHT * (3/4)))
      answer2_rect = answer1.get_rect(center=(960 + 960 / 2, SCREEN_HEIGHT * (3/4)))
      answer1_pic_rect = answer1_pic.get_rect(center=(960 / 2, SCREEN_HEIGHT * (1/2) - 100))
      answer2_pic_rect = answer2_pic.get_rect(center=(960 + 960 / 2, SCREEN_HEIGHT * (1/2) - 100))

      screen.blit(question, question_rect)
      screen.blit(answer1, answer1_rect)
      screen.blit(answer2, answer2_rect)
      screen.blit(answer1_pic, answer1_pic_rect)
      screen.blit(answer2_pic, answer2_pic_rect)

      pygame.display.flip()

      i += 1
      new = False

      clock.tick(60)  # limits FPS to 60

   pygame.quit()

for data in Config.DATAS:
   data_dict[data] = csv_to_dict("Datasets/" + data + ".csv", "country", "score")

pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
my_font = pygame.font.SysFont('Assets/Dosis-Bold.ttf', 50)
country_dict = csv_to_dict_spe("Datasets/Countries.csv", "c1", "c2")

loop(my_font, country_dict)
