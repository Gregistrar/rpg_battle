from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import time
import random
import os

# This magically allows color to work in the Terminal
os.system('color')

print("\n\n")

# Create Black Magic
fire = Spell("Fire", 20, 250, "black")
thunder = Spell("Thunder", 20, 250, "black")
blizzard = Spell("Blizzard", 20, 250, "black")
meteor = Spell("Meteor", 35, 375, "black")
quake = Spell("Quake", 30, 315, "black")

# Create White Magic
cure = Spell("Cure", 22, 220, "white")
cura = Spell("Cura", 32, 400, "white")
curaga = Spell("Curaga", 50, 6000, "white")

# Create some Items
potion = Item("Potion", "potion", "Heals 50 HP", 250)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 500)
superpotion = Item("Super Potion", "potion", "Heals 500 HP", 1000)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
hielixir = Item("Mega Elixir", "elixir", "Fully restores party's HP/MP", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


# Lists of actions, magic, items
player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spells = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 5}, {"item": hipotion, "quantity": 3},
                {"item": superpotion, "quantity": 2}, {"item": elixir, "quantity": 5},
                {"item": hielixir, "quantity": 5}, {"item": grenade, "quantity": 5}]

# Instantiate People
player1 = Person("Valos:", 3960, 95, 132, 34, player_spells, player_items)
player2 = Person("Talos:", 3160, 115, 145, 34, player_spells, player_items)
player3 = Person("Plato:", 3560, 105, 138, 34, player_spells, player_items)

enemy1 = Person("Imp    ", 1350, 150, 192, 25, enemy_spells, [])
enemy2 = Person("Balrog ", 11200, 250, 342, 25, enemy_spells, [])
enemy3 = Person("Goblin ", 1450, 165, 222, 25, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("=================================")
    print("\n")
    print("NAME                 HP                                     MP")
    for player in players:
        player.get_stats()
    # print("\n")
    time.sleep(1)

    for enemy in enemies:
        enemy.get_enemy_stats()
    time.sleep(1)

    for player in players:
        player.choose_action()
        while True:
            choice = input("    Choose Action: ")
            if choice in ("1", "2", "3"):
                break
            print("You have made an invalid choice, try again!")
        index = int(choice) - 1
        print("\n    You chose to use {}.".format(player.actions[index]))

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print(bcolors.OKBLUE + "\nYou attacked the {} for {} points of damage."
                  .format(enemies[enemy].name.replace(" ", ""), dmg) + bcolors.ENDC)
            if enemies[enemy].get_hp() == 0:
                print("{} has died.".format(enemies[enemy].name.replace(" ", "")))
                del enemies[enemy]
            time.sleep(1)
        elif index == 1:
            player.choose_magic()
            while True:
                index = input("    Choose magic: ")
                if index in ("1", "2", "3", "4", "5", "6", "7"):
                    break
                print("You have made an invalid choice, try again!")

            magic_choice = int(index) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP...\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.spell_type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n{} heals for {} HP.".format(spell.name, magic_dmg) + bcolors.ENDC)
            elif spell.spell_type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n{} deals {} points of damage to the {}."
                      .format(spell.name, magic_dmg, enemies[enemy].name.replace(" ", "")) + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print("{} has died.".format(enemies[enemy].name.replace(" ", "")))
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            while True:
                index = input("    Choose item: ")
                if index in ("1", "2", "3", "4", "5", "6"):
                    break
                print("You have made an invalid choice, try again!")

            item_choice = int(index) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\nNone left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.item_type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n{} heals for {} HP".format(item.name, item.prop) + bcolors.ENDC)
            elif item.item_type == "elixir":
                if item.name == "Mega Elixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n{} fully restores HP/MP".format(item.name) + bcolors.ENDC)
            elif item.item_type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.OKBLUE + "\n{} deals {} points of damage to the {}."
                      .format(item.name, item.prop, enemies[enemy].name.replace(" ", "")) + bcolors.ENDC)
                if enemies[enemy].get_hp() == 0:
                    print("{} has died.".format(enemies[enemy].name.replace(" ", "")))
                    del enemies[enemy]

    # Check if the battle is over
    defeated_enemies = 0
    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    if defeated_enemies == 3:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    elif defeated_players == 3:
        print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
        running = False

    # Enemy attacks!
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        if enemy_choice == 0:
            # Chose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemies[0].generate_damage()

            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + "\n{} attacks {} for {} HP."
                  .format(enemy.name.replace(" ", ""), players[target].name.replace(" ", "").replace(":", "")
                          , enemy_dmg) + bcolors.ENDC)
            time.sleep(1)
        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.spell_type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n{} heals {} for {} HP.".format(spell.name, enemy.name.replace(" ", "")
                                                                         , magic_dmg) + bcolors.ENDC)
            elif spell.spell_type == "black":
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n{} {} deals {} points of damage to {}."
                      .format(enemy.name.replace(" ", ""), spell.name, magic_dmg,
                              players[target].name.replace(" ", "").replace(":", "")) + bcolors.ENDC)
                if players[target].get_hp() == 0:
                    print("{} has died.".format(players[target].name.replace(" ", "").replace(":", "")))
                    del players[player]
    print("\n")
    time.sleep(2)






