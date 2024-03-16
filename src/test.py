import random
import pygame
import csv

from config import Config

data_dict = {}

def csv_to_dict(csv_file_path, key_column, value_column):
   result_dict = {}

   with open(csv_file_path, 'r', newline='') as file:
      csv_reader = csv.DictReader(file)

      for row in csv_reader:
         key = row[key_column]
         value = row[value_column]
         
         result_dict[key] = value

   return result_dict

def check_choice(random_country_data1, random_country_data2, i):
   if choice == 1 and random_country_data1 > random_country_data2:
       print("Youre right!")
   elif choice == 2 and random_country_data1 < random_country_data2:
       print("Youre right!")
   elif random_country_data2 == random_country_data1:
       print("Both are equals!")
   else:
       print("Rip bozo youre wrong!, Youre streak is:", i)
       exit()

def check_invert_choice(random_country_data1, random_country_data2, i):
   if choice == 1 and random_country_data1 < random_country_data2:
       print("Youre right!")
   elif choice == 2 and random_country_data1 > random_country_data2:
       print("Youre right!")
   elif random_country_data2 == random_country_data1:
       print("Both are equals!")
   else:
       print("Rip bozo youre wrong!, Youre streak is:", i)
       exit()

for data in Config.DATAS:
   data_dict[data] = csv_to_dict("Datasets/" + data + ".csv", "country", "score")

found = False
random_field = random.choice(Config.DATAS)

random_country_name1, random_country_data1 = random.choice(list(data_dict[random_field].items()))
random_country_name2, random_country_data2 = random.choice(list(data_dict[random_field].items()))

i = 0
while not found:
   print("1 -", random_country_name1, "has more", random_field, "than", random_country_name2)
   print("2 -", random_country_name1, "has less", random_field, "than", random_country_name2)

   choice = 0
   try:
      choice = int(input())
   except ValueError:
      continue

   if choice != 1 and choice != 2:
      continue

   if Config.INVERT[random_field] == True:
      check_invert_choice(random_country_data1, random_country_data2, i)
   else:
      check_choice(random_country_data1, random_country_data2, i)

   random_field = random.choice(Config.DATAS)

   random_country_name1 = random_country_name2
   random_country_data1 = data_dict[random_field][random_country_name1]

   random_country_name2, random_country_data2 = random.choice(list(data_dict[random_field].items()))
   i += 1
