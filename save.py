# Author: Noah Wilson, wilsonn2018@my.fit.edu
# Course: CSE 2050, Fall 2019
# Project: Save
"""Docstring for Save the Manatee Game"""

import argparse
from urllib.request import urlopen
import pygame
from pygame.locals import *


COQUINAS = list()
HYACINTH = list()
CLOSED_GATE = list()
OPEN_GATE = list()
BOATS = list()
WATER = list()


def check_in(a_list, coordinates):
    """This function takes a tuple of coordinates and checks if
        they are in the list passed through."""
    if coordinates in a_list:
        return True
    return False


def move_boats():
    """This function moves all the boats after Hugh Manatee moves"""
    for boat in BOATS:
        right = ((boat[0] + 48), (boat[1] + 48))
        left = ((boat[0] - 48), (boat[1] + 48))
        down = (boat[0], (boat[1] + 48))
        if check_in(WATER, down) and down != (HUGH_X, HUGH_Y):
            DISPLAY.blit(BOAT_PIC, down)
            BOATS.remove(boat)
            BOATS.append(down)
            DISPLAY.blit(WATER_PIC, boat)
            WATER.remove(down)
            WATER.append(boat)
        elif check_in(WATER, left) and left != (HUGH_X, HUGH_Y):
            DISPLAY.blit(BOAT_PIC, left)
            BOATS.remove(boat)
            BOATS.append(left)
            DISPLAY.blit(WATER_PIC, boat)
            WATER.remove(left)
            WATER.append(boat)
        elif check_in(WATER, right) and right != (HUGH_X, HUGH_Y):
            DISPLAY.blit(BOAT_PIC, right)
            BOATS.remove(boat)
            BOATS.append(right)
            DISPLAY.blit(WATER_PIC, boat)
            WATER.remove(right)
            WATER.append(boat)


# Get arguments from command prompt
PARSER = argparse.ArgumentParser()
PARSER.add_argument("-s", "--map", type=str)
CMD_ARGS = PARSER.parse_args()

# Open URL that contains the map
URL = CMD_ARGS.map
with urlopen(URL) as handle:
    BOARD = handle.read().decode('utf-8')

# Create the game display
BOAT_PIC = pygame.image.load("boat.png")
COQUINA_PIC = pygame.image.load("coquina.png")
GRATE_PIC = pygame.image.load("grate.png")
HUGH_PIC = pygame.image.load("hugh.png")
HYACINTH_PIC = pygame.image.load("hyacinth.png")
INJURED_PIC = pygame.image.load("injured.png")
OPENGATE_PIC = pygame.image.load("open.png")
SEAGRASS_PIC = pygame.image.load("seagrass.png")
WATER_PIC = pygame.image.load("water.png")

# Initialize the display
pygame.init()
WIDTH = 0
LENGTH = 0
for i in BOARD:
    if i == "\n":
        WIDTH += 1

for y in BOARD:
    LENGTH += 1
    if y == "\n":
        break

DISPLAY = pygame.display.set_mode((LENGTH*48, WIDTH*48))
pygame.display.set_caption("Save the Manatees!")
X_COR = 48
Y_COR = 0

# Create game music and points system
FONT = pygame.font.SysFont("Serif", 25)
pygame.mixer.music.load("mptheme.mp3")
pygame.mixer.music.play(-1)

# Create board
for i in BOARD:
    if i == "\n":
        X_COR = 0
        Y_COR += 48
    elif i == "M":
        DISPLAY.blit(HUGH_PIC, (X_COR, Y_COR))
        HUGH_X = X_COR
        HUGH_Y = Y_COR
    elif i == "W":
        DISPLAY.blit(INJURED_PIC, (X_COR, Y_COR))
    elif i == "#":
        DISPLAY.blit(COQUINA_PIC, (X_COR, Y_COR))
        t = (X_COR, Y_COR)
        COQUINAS.append(t)
    elif i == "*":
        DISPLAY.blit(BOAT_PIC, (X_COR, Y_COR))
        t = (X_COR, Y_COR)
        BOATS.append(t)
    elif i == "\\":
        DISPLAY.blit(HYACINTH_PIC, (X_COR, Y_COR))
        t = (X_COR, Y_COR)
        HYACINTH.append(t)
    elif i == "G":
        DISPLAY.blit(GRATE_PIC, (X_COR, Y_COR))
        t = (X_COR, Y_COR)
        CLOSED_GATE.append(t)
    elif i == "O":
        DISPLAY.blit(OPENGATE_PIC, (X_COR, Y_COR))
        t = (X_COR, Y_COR)
        OPEN_GATE.append(t)
    elif i == ".":
        DISPLAY.blit(SEAGRASS_PIC, (X_COR, Y_COR))
    elif i == " ":
        DISPLAY.blit(WATER_PIC, (X_COR, Y_COR))
        t = (X_COR, Y_COR)
        WATER.append(t)
    X_COR += 48

GATE_COORD = CLOSED_GATE[0]
# Main Game Loop
TOTAL_HYACINTHS = len(HYACINTH)
TOTAL_POINTS = 0
while True:
    for user_input in pygame.event.get():
        if user_input.type == QUIT:
            pygame.quit()
            quit()

        # If all the hyacinths are gone make the gate open and if Hugh Manatee
        # is at the gate, end the game.
        if len(HYACINTH) == 0:
            if len(CLOSED_GATE) != 0:
                DISPLAY.blit(OPENGATE_PIC, GATE_COORD)
                CLOSED_GATE.remove(GATE_COORD)
            elif len(CLOSED_GATE) == 0 and (HUGH_X, HUGH_Y) == GATE_COORD:
                TOTAL_POINTS += TOTAL_HYACINTHS*50
                pygame.mixer.music.load("mario.mp3")
                pygame.mixer.music.play(1)
                DISPLAY.blit(COQUINA_PIC, (96, 0))
                DISPLAY.blit(COQUINA_PIC, (144, 0))
                DISPLAY.blit(COQUINA_PIC, (192, 0))
                SCORE = FONT.render("Score: " + str(TOTAL_POINTS), False, (0, 0, 0))
                DISPLAY.blit(SCORE, (50, 0))
                break

        # Whichever key is pressed, perform that move and check for collision.
        if user_input.type == KEYDOWN:
            TOTAL_POINTS -= 1
            # If user presses right arrow key
            if user_input.key == K_RIGHT:
                # Check if Manatee is trying to move into Coquinas
                if check_in(COQUINAS, (HUGH_X + 48, HUGH_Y)) or \
                        check_in(CLOSED_GATE, (HUGH_X + 48, HUGH_Y)):
                    continue
                # Check if Manatee is moving into Hyacinth
                elif check_in(HYACINTH, (HUGH_X + 48, HUGH_Y)):
                    TOTAL_POINTS += 25
                    DISPLAY.blit(WATER_PIC, (HUGH_X, HUGH_Y))
                    HUGH_X += 48
                    DISPLAY.blit(HUGH_PIC, (HUGH_X, HUGH_Y))
                    HYACINTH.remove((HUGH_X, HUGH_Y))
                    if (HUGH_X, HUGH_Y) not in WATER:
                        WATER.append((HUGH_X, HUGH_Y))
                # Check if Manatee is moving a boat
                elif check_in(BOATS, (HUGH_X + 48, HUGH_Y)):
                    # Check if moving the boat runs into anything besides water
                    if check_in(WATER, (HUGH_X + 96, HUGH_Y)):
                        DISPLAY.blit(WATER_PIC, (HUGH_X, HUGH_Y))
                        HUGH_X += 48
                        DISPLAY.blit(HUGH_PIC, (HUGH_X, HUGH_Y))
                        BOATS.remove((HUGH_X, HUGH_Y))
                        BOATS.append((HUGH_X + 48, HUGH_Y))
                        DISPLAY.blit(BOAT_PIC, (HUGH_X + 48, HUGH_Y))
                    else:
                        continue
                # Otherwise he is moving into water of grass
                else:
                    DISPLAY.blit(WATER_PIC, (HUGH_X, HUGH_Y))
                    HUGH_X += 48
                    DISPLAY.blit(HUGH_PIC, (HUGH_X, HUGH_Y))
                    if (HUGH_X, HUGH_Y) not in WATER:
                        WATER.append((HUGH_X, HUGH_Y))
            # If user presses left
            elif user_input.key == K_LEFT:
                if check_in(COQUINAS, (HUGH_X - 48, HUGH_Y)) or \
                        check_in(CLOSED_GATE, (HUGH_X - 48, HUGH_Y)):
                    continue
                elif check_in(HYACINTH, (HUGH_X - 48, HUGH_Y)):
                    TOTAL_POINTS += 25
                    DISPLAY.blit(WATER_PIC, (HUGH_X, HUGH_Y))
                    HUGH_X -= 48
                    DISPLAY.blit(HUGH_PIC, (HUGH_X, HUGH_Y))
                    HYACINTH.remove((HUGH_X, HUGH_Y))
                    if (HUGH_X, HUGH_Y) not in WATER:
                        WATER.append((HUGH_X, HUGH_Y))
                # Check if Manatee is moving a boat
                elif check_in(BOATS, (HUGH_X - 48, HUGH_Y)):
                    # Check if moving the boat runs into anything besides water
                    if check_in(WATER, (HUGH_X - 96, HUGH_Y)):
                        DISPLAY.blit(WATER_PIC, (HUGH_X, HUGH_Y))
                        HUGH_X -= 48
                        DISPLAY.blit(HUGH_PIC, (HUGH_X, HUGH_Y))
                        BOATS.remove((HUGH_X, HUGH_Y))
                        BOATS.append((HUGH_X - 48, HUGH_Y))
                        DISPLAY.blit(BOAT_PIC, (HUGH_X - 48, HUGH_Y))
                    else:
                        continue
                else:
                    DISPLAY.blit(WATER_PIC, (HUGH_X, HUGH_Y))
                    HUGH_X -= 48
                    DISPLAY.blit(HUGH_PIC, (HUGH_X, HUGH_Y))
                    if (HUGH_X, HUGH_Y) not in WATER:
                        WATER.append((HUGH_X, HUGH_Y))
            # If user presses down
            elif user_input.key == K_DOWN:
                if check_in(COQUINAS, (HUGH_X, HUGH_Y + 48)) or \
                        check_in(CLOSED_GATE, (HUGH_X, HUGH_Y + 48)):
                    continue
                elif check_in(HYACINTH, (HUGH_X, HUGH_Y + 48)):
                    TOTAL_POINTS += 25
                    DISPLAY.blit(WATER_PIC, (HUGH_X, HUGH_Y))
                    HUGH_Y += 48
                    DISPLAY.blit(HUGH_PIC, (HUGH_X, HUGH_Y))
                    HYACINTH.remove((HUGH_X, HUGH_Y))
                    if (HUGH_X, HUGH_Y) not in WATER:
                        WATER.append((HUGH_X, HUGH_Y))
                # Check if Manatee is moving a boat
                elif check_in(BOATS, (HUGH_X, HUGH_Y + 48)):
                    # Check if moving the boat runs into anything besides water
                    if check_in(WATER, (HUGH_X, HUGH_Y + 96)):
                        DISPLAY.blit(WATER_PIC, (HUGH_X, HUGH_Y))
                        HUGH_Y += 48
                        DISPLAY.blit(HUGH_PIC, (HUGH_X, HUGH_Y))
                        BOATS.remove((HUGH_X, HUGH_Y))
                        BOATS.append((HUGH_X, HUGH_Y + 48))
                        DISPLAY.blit(BOAT_PIC, (HUGH_X, HUGH_Y + 48))
                    else:
                        continue
                else:
                    DISPLAY.blit(WATER_PIC, (HUGH_X, HUGH_Y))
                    HUGH_Y += 48
                    DISPLAY.blit(HUGH_PIC, (HUGH_X, HUGH_Y))
                    if (HUGH_X, HUGH_Y) not in WATER:
                        WATER.append((HUGH_X, HUGH_Y))
            # If user presses up
            elif user_input.key == K_UP:
                if check_in(COQUINAS, (HUGH_X, HUGH_Y - 48)) or \
                        check_in(CLOSED_GATE, (HUGH_X, HUGH_Y - 48)):
                    continue
                elif check_in(HYACINTH, (HUGH_X, HUGH_Y - 48)):
                    TOTAL_POINTS += 25
                    DISPLAY.blit(WATER_PIC, (HUGH_X, HUGH_Y))
                    HUGH_Y -= 48
                    DISPLAY.blit(HUGH_PIC, (HUGH_X, HUGH_Y))
                    HYACINTH.remove((HUGH_X, HUGH_Y))
                    if (HUGH_X, HUGH_Y) not in WATER:
                        WATER.append((HUGH_X, HUGH_Y))
                # Check if Manatee is moving a boat
                elif check_in(BOATS, (HUGH_X, HUGH_Y - 48)):
                    # Check if moving the boat runs into anything besides water
                    if check_in(WATER, (HUGH_X, HUGH_Y - 48)):
                        DISPLAY.blit(WATER_PIC, (HUGH_X, HUGH_Y))
                        HUGH_Y -= 48
                        DISPLAY.blit(HUGH_PIC, (HUGH_X, HUGH_Y))
                        BOATS.remove((HUGH_X, HUGH_Y))
                        BOATS.append((HUGH_X, HUGH_Y - 48))
                        DISPLAY.blit(BOAT_PIC, (HUGH_X, HUGH_Y - 48))
                    else:
                        continue
                else:
                    DISPLAY.blit(WATER_PIC, (HUGH_X, HUGH_Y))
                    HUGH_Y -= 48
                    DISPLAY.blit(HUGH_PIC, (HUGH_X, HUGH_Y))
                    if (HUGH_X, HUGH_Y) not in WATER:
                        WATER.append((HUGH_X, HUGH_Y))
            move_boats()
            DISPLAY.blit(COQUINA_PIC, (96, 0))
            DISPLAY.blit(COQUINA_PIC, (144, 0))
            DISPLAY.blit(COQUINA_PIC, (192, 0))
            SCORE = FONT.render("Score: " + str(TOTAL_POINTS), False, (0, 0, 0))
            DISPLAY.blit(SCORE, (50, 0))
    pygame.display.update()
