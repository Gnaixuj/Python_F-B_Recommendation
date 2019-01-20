import pygame, sys
from pygame.locals import *
import math
from operator import itemgetter
import webbrowser
import time
import pickle

black = (0, 0, 0)
white = (255, 255, 255)
grey = (211, 211, 211)

pygame.init()

tiny_font = pygame.font.SysFont("arialblack", 13)
small_font = pygame.font.SysFont("arialblack", 25)
medium_font = pygame.font.SysFont("arialblack", 50)
large_font = pygame.font.SysFont("arialblack", 60)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DATA

# canteen_info = {Canteen Name: {Address, Tel, Opening Hrs, Seat Cap, Location (Coordinates), Rank, Patron Num}}
read_file = open("data.py", "rb") # Canteen Information Stored in data.py in Binary Encoding
canteen_info = pickle.load(read_file)

canteen_food = {"Food Court 1": {"FISH AND CHIPS" : 3.6,\
                                 "MALA" : 4.2,\
                                 "MIXED VEGETABLE RICE" : 3,\
                                 "CHICKEN RICE" : 3.5,\
                                 "JAPANESE CURRY RICE" : 3.5},\
                "Food Court 2": {"MIXED VEGETABLE RICE" : 2.5,\
                                 "CHINESE NOODLES" : 3,\
                                 "CHICKEN BULGOGI" : 4.6,\
                                 "STEAMED BUN" : 4.2,\
                                 "CHICKEN RICE" : 3,\
                                 "AYAM PENYET" : 4.5,\
                                 "PIZZA" : 5,\
                                 "TAKOYAKI" : 3},\
                "Food Court 9": {"NAAN" : 4.75,\
                                 "CHICKEN CHOP" : 4,\
                                 "GONG BO CHICKEN" : 2.5,\
                                 "BAN MIAN" : 4.2},\
                "Food Court 11": {"RAMEN" : 5.25,\
                                  "FRIED RICE" : 5,\
                                  "MIXED VEGETABLE RICE" : 4.5,\
                                  "BAN MIAN" : 4,\
                                  "FRUIT JUICE" : 2.7},\
                "Food Court 13": {"FISH SOUP" : 4,\
                                  "FRIED RICE" : 2.8 ,\
                                  "RAMYEON" : 4.5,\
                                  "MIXED VEGETABLE RICE" : 2.25},\
                "Food Court 14": {"NASI LEMAK" : 2,\
                                  "MEE SOTO" : 2.5,\
                                  "MEE REBUS" : 2.30,\
                                  "RAMEN" : 5,\
                                  "MEE HOON KWAY" : 4.5},\
                "Food Court 16": {"DUMPLING SOUP" : 3,\
                                  "FIRED CARROT CAKE" : 3.75,\
                                  "FISH BALL NOODLES" : 2.2,\
                                  "MEE GORENG" : 3,\
                                  "MALA" : 6},
                "North Spine Food Court": {"PASTA" : 4.65,\
                                           "DUCK RICE" : 2.5,\
                                           "BAN MIAN" : 3.8,\
                                           "CHICKEN BIRYANI" : 4.5,\
                                           "CHICKEN CURRY" : 6.5,\
                                           "MEE SUA" : 3.75 ,\
                                           "MINCED MEAT NOODLES" : 3,\
                                           "CHICKEN RICE" : 2.6,\
                                           "CHAR SIEW RICE" : 3.8,\
                                           "MIXED VEGETABLE RICE" : 2.5,\
                                           "PHO" : 3.5},
                "North Hill Food Court": {"MEE REBUS" : 3.9,\
                                          "FRIED RICE" : 3.5,\
                                          "FISH SOUP": 2,\
                                          "CHICKEN RICE" : 3,\
                                          "LONTONG" : 4.3,\
                                          "MIXED VEGETABLE RICE" : 2.5},\
                "Koufu @ the South Spine": {"CHICKEN RICE" : 2.5,\
                                            "ROASTED PORK RICE" : 3,\
                                            "FRIED DUMPLINGS" : 3.5,\
                                            "PASTA": 4.5,\
                                            "CHAPATI SET" : 3.8,\
                                            "FISH SOUP" : 4.3,\
                                            "BAN MIAN" : 3.5,\
                                            "YONG TAU FOO" : 3,\
                                            "BEE HOON" : 2.9,\
                                            "CHILI CRAB" : 29.9}}

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# USER INTERFACE FUNCTIONS

# Set Text Colour and Font Size
def text_objects(text, color, size):
    textSurface = size.render(text, True, color)
    return textSurface, textSurface.get_rect()

# Print Text On Button
def text_to_button(text, color, x, y, width, height, size):
    textSurf, textRect = text_objects(text, color, size)
    textRect.center = ((x + (width / 2)), (y + (height / 2)))
    screen_display.blit(textSurf, textRect)

# Print Text On Screen
def text_to_screen(msg, color, x, y, width, height, font_size):
    screen_text = font_size.render(msg, True, color)
    screen_display.blit(screen_text, [x, y, width, height])

# Create Button and Corresponding Functions
def button(text, x, y, width, height, inactive_color, active_color, text_size, function = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if (x + width) > cur[0] > x and (y + height) > cur[1] > y:
        pygame.draw.rect(screen_display, active_color, (x, y, width, height))
        if click[0] == 1 and function != None:
            
            if function == "distance":
                time.sleep(0.5)
                display("NTU Campus.jpg")
                print("Select Current Location")
                user_location = mouse_click()
                locationlist_canteens = sort_list(canteen_info, "Location")
                sort_by_distance(user_location, locationlist_canteens)
                time.sleep(0.5)
                navigation()
                
            elif function == "rank":
                ranklist_canteens = sort_list(canteen_info, "Rank")
                sort_by_rank(ranklist_canteens)
                time.sleep(0.5)
                navigation()
                
            elif function == "price":
                time.sleep(0.5)
                foodlist_canteens = canteen_food
                while True:
                    max_target_price = input("Input Maximum Price of Food: ")
                    try:
                        max_price = float(max_target_price)
                        break
                    except ValueError:
                        print("Price Input is Not a Numerical Value. Please Try Again")
                        continue
                search_by_price(max_price, foodlist_canteens)
                
            elif function == "food":
                time.sleep(0.5)
                foodlist_canteens = canteen_food
                target_food = input("Input Food Name for Search: ")
                search_by_food(target_food.upper(), foodlist_canteens)

            elif function == "navigate_menu":
                time.sleep(0.5)
                menu("navigate")

            elif function == "navigate":
                time.sleep(0.5)                
                for canteen in canteen_info.keys():
                    if text == canteen:
                        temp = text.split()
                        temp_edit = "%20".join(temp)
                webbrowser.open("http://maps.ntu.edu.sg/maps#q:" + temp_edit)

            elif function == "main":
                time.sleep(0.5)
                title_screen()

            elif function == "update_menu":
                time.sleep(0.5)
                menu("update_rank")

            elif function == "update_rank":
                time.sleep(0.5)
                canteen_name = text
                while True:
                    rank_str = input("Enter Your Rank for the Selected Food Court (0 to 10): ")
                    try:
                        rank_int = float(rank_str)
                        if 0 <= rank_int <= 10:
                            update_rank(rank_int, canteen_name)
                            break
                        else:
                            print("Rank Input is Out of Range. Please Try Again")
                            continue
                    except ValueError:
                        print("Rank Input is Not a Numerical Value. Please Try Again")
                        continue

            elif function == "info":
                for canteen_name, info in canteen_info.items():
                    print(canteen_name, info)
                    print()
    else:
        pygame.draw.rect(screen_display, inactive_color, (x, y, width, height))
    text_to_button(text, black, x, y, width, height, text_size)
   
# Main Title Screen
def title_screen():
    display("Title Screen.jpg")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        button("Sort by Distance", 300, 250, 395, 50, white, grey, small_font, function = "distance")
        button("Sort by Rank", 300, 325, 395, 50, white, grey, small_font, function = "rank")
        button("Search by Food", 300, 400, 395, 50, white, grey, small_font, function = "food")
        button("Search by Price", 300, 475, 395, 50, white, grey, small_font, function = "price")
        button("Update Ranking", 300, 550, 395, 50, white, grey, small_font, function = "update_menu")
        button("Food Court Navigation", 300, 625, 395, 50, white, grey, small_font, function = "navigate_menu")
        button("Info", 895, 650, 100, 50, white, grey, small_font, function = "info")
        pygame.display.update()

# List of Canteen for User to Select (for Navigation or Rank Update)
def menu(function_type):
    screen_display.fill(black)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        function = function_type
        if function == "navigate":
            text_to_screen("Select Food Court for Navigation", white, 55, 5, 60, 25, medium_font)
        elif function == "update_rank":
            text_to_screen("Select Food Court to Update Rank", white, 40, 5, 60, 25, medium_font)
            
        button("Food Court 1", 125, 100, 350, 50, white, grey, small_font, function)
        button("Food Court 2", 125, 175, 350, 50, white, grey, small_font, function)
        button("Food Court 9", 125, 250, 350, 50, white, grey, small_font, function)
        button("Food Court 11", 125, 325, 350, 50, white, grey, small_font, function)
        button("Food Court 13", 125, 400, 350, 50, white, grey, small_font, function)
        button("Food Court 14", 125, 475, 350, 50, white, grey, small_font, function)        
        button("Food Court 16", 545, 100, 350, 50, white, grey, small_font, function)
        button("Ananda Kitchen", 545, 175, 350, 50, white, grey, small_font, function)
        button("Foodgle Food Court", 545, 250, 350, 50, white, grey, small_font, function)
        button("North Hill Food Court", 545, 325, 350, 50, white, grey, small_font, function)
        button("Pioneer Food Court", 545, 400, 350, 50, white, grey, small_font, function)
        button("Quad Cafe", 545, 475, 350, 50, white, grey, small_font, function)
        button("North Spine Food Court", 125, 550, 350, 50, white, grey, small_font, function)
        button("Koufu @ the South Spine", 545, 550, 350, 50, white, grey, small_font, function)
        button("Return to Main", 750, 625, 145, 50, white, grey, tiny_font, function = "main")
        pygame.display.update()

# Allow User to Open Navigation Menu after Searching / Sorting
def navigation():
    screen_display.fill(black)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        text_to_screen("Open Navigation Menu?", white, 125, 50, 125, 50, large_font)
        button("Yes", 200, 475, 150, 100, white, grey, small_font, function = "navigate_menu")
        button("No", 645, 475, 150, 100, white, grey, small_font, function = "main")
        pygame.display.update()
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MAIN FUNCTIONS

# Display Image On Screen
def display(image):
    introScreenImage = pygame.image.load(image)
    screen = pygame.display.set_mode((995,700)) # Screen Size (Max x, y Coordinates)
    screen.blit(introScreenImage,(0,0))
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    pygame.display.flip()
    pygame.display.set_caption("NTU F&B Recommendation System")

# Get Coordinates of Mouse Click
def mouse_click():
    while True:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos() 
                return position

# Straight Line Distance btw 2 Points
def distance_a_b(current_location, travel_location):
        x_value = travel_location[0] - current_location[0]
        y_value = travel_location[1] - current_location[1]
        distance_float = math.sqrt((x_value ** 2) + (y_value **2))
        distance_int = int(distance_float)
        return distance_int

# Create Temp List for Sorting Based on Criteria (distance or rank)
def sort_list(target_list, criteria):
    result_list = []
    for canteen in target_list.keys():
        temp_list = [canteen]
        temp_value = target_list[canteen][criteria]
        temp_list.append(temp_value)
        result_list.append(temp_list)
    return result_list

# Sort Canteen By Distance From Selected Point (nearest to furthest)
def sort_by_distance(user_location, locationlist_canteens):
    for canteen in locationlist_canteens:
        travel_location = canteen[1]
        distance = distance_a_b(user_location, travel_location)    
        canteen.append(distance)
    for canteen in locationlist_canteens:
        sort_dist = sorted(locationlist_canteens, key = itemgetter(2))
    print("Canteen Nearest to Furthest From You: ")
    print()
    result_display(sort_dist)

# Sort Canteen By Rank (highest to lowest)
def sort_by_rank(ranklist_canteens):
    sort_rank = sorted(ranklist_canteens, key = itemgetter(1), reverse = True)
    print("Canteen Ranked from Highest to Lowest: ")
    print()
    result_display(sort_rank)

# Search Canteen & Food Based on User Price Range
def search_by_price(max_target_price, foodlist_canteens):
    search_price = []
    canteen_name = set()
    for canteen, info in foodlist_canteens.items():
        for food, price in info.items():
            temp_list = []
            if price <= max_target_price:
                temp_list = [canteen, food, price]
                canteen_name.add(canteen)
                search_price.append(temp_list)
            else:
                continue
    if len(search_price) == 0:
        print("No Food Can Be Bought At This Price. Sorry")
        print("Returning to Main Menu")
    else:
        result_display(search_price)
        display_info(canteen_name)

# Search Food Based on User Input 
def search_by_food(foodname, foodlist_canteens):
    search_food = []
    canteen_name = []
    for canteen, info in foodlist_canteens.items():
        for food in info.keys():
            if food == foodname:
                temp_list = [canteen, food]
                canteen_name.append(canteen)
                search_food.append(temp_list)
                break
    if len(search_food) == 0:
        print("Food Does not Exist in NTU")
        print("Returning to Main Menu")
    else:
        result_display(search_food)
        display_info(canteen_name)

# Display Results After Searching / Sorting
def result_display(result_list):
    for result in result_list:
        print(result)
        print()

# Display All Info about Canteen
def display_info(canteen_name):
    for canteen in canteen_name:
        for food_court, info in canteen_info.items():
            if canteen == food_court:
                print(food_court, info)
                print()
            continue

# Allow User to Update Rank and Save the Result
def update_rank(rank_int, canteen_name):
    for food_court in canteen_info.keys():
            if canteen_name == food_court:         
                canteen_info[canteen_name]["Rank"] = round((((canteen_info[canteen_name]["Rank"] * canteen_info[canteen_name]["Patron_Num"]) + rank_int)\
                                                            / (canteen_info[canteen_name]["Patron_Num"] + 1)), 2)
                canteen_info[canteen_name]["Patron_Num"] += 1
    write_file = open("data.py", "wb")
    pickle.dump(canteen_info, write_file)
    write_file.close()
    print("Rank Updated")
    print("Current Rank of ", canteen_name, " is", canteen_info[canteen_name]["Rank"])
        
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MAIN PROGRAM

screen_display = pygame.display.set_mode((995,700))
title_screen()
