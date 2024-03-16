import requests
import random
import pygame
import csv

from config import Config

data_dict = {}
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def csv_to_dict(csv_file_path, key_column, value_column):
   result_dict = {}
   print(csv_file_path)

   with open(csv_file_path, 'r', newline='') as file:
      csv_reader = csv.DictReader(file)

      for row in csv_reader:
         key = row[key_column]
         value = row[value_column]
         
         result_dict[key] = value

   return result_dict

def check_choice(random_country_data1, random_country_data2, i, choice):
   if choice == 1 and random_country_data1 > random_country_data2:
       print("Youre right!")
   elif choice == 2 and random_country_data1 < random_country_data2:
       print("Youre right!")
   elif random_country_data2 == random_country_data1:
       print("Both are equals!")
   else:
       print("Rip bozo youre wrong!, Youre streak is:", i)
       exit()

def check_invert_choice(random_country_data1, random_country_data2, i, choice):
   if choice == 1 and random_country_data1 < random_country_data2:
       print("Youre right!")
   elif choice == 2 and random_country_data1 > random_country_data2:
       print("Youre right!")
   elif random_country_data2 == random_country_data1:
       print("Both are equals!")
   else:
       print("Rip bozo youre wrong!, Youre streak is:", i)
       exit()

def loop(my_font, country_dict):
   pygame.init()
   screen = pygame.display.set_mode((1280, 720))
   clock = pygame.time.Clock()
   running = True
   new = True
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
                  check_invert_choice(random_country_data1, random_country_data2, i, 1)
               else:
                  check_choice(random_country_data1, random_country_data2, i, 1)
            if (answer2_pic_rect.collidepoint(event.pos)):
               new = True
               if Config.INVERT[random_field]:
                  check_invert_choice(random_country_data1, random_country_data2, i, 2)
               else:
                  check_choice(random_country_data1, random_country_data2, i, 2)

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

      screen.fill("purple")
      question = my_font.render("Wich has more " + random_field + " ?", False, (0, 0, 0))
      answer1 = my_font.render("1- " + random_country_name1, False, (0, 0, 0))
      answer2 = my_font.render("2- " + random_country_name2, False, (0, 0, 0))

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

      question_rect = question.get_rect(center=(SCREEN_WIDTH/2, 100))
      answer1_rect = answer1.get_rect(center=(100, SCREEN_HEIGHT * (3/4)))
      answer2_rect = answer1.get_rect(center=(SCREEN_WIDTH - 200, SCREEN_HEIGHT * (3/4)))
      answer1_pic_rect = answer1_pic.get_rect(center=(100, SCREEN_HEIGHT * (3/4) - 200))
      answer2_pic_rect = answer2_pic.get_rect(center=(SCREEN_WIDTH - 200, SCREEN_HEIGHT * (3/4) - 200))

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
my_font = pygame.font.SysFont('Comic Sans MS', 30)
country_dict = csv_to_dict("Datasets/Countries.csv", "c1", "c2")

loop(my_font, country_dict)
