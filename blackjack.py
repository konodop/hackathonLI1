# Импортируем os для доступа к спрайтам
import os
# Импортируем random для самого блэкджека
import random
import sys
# Импортируем пайгейм для игры
import pygame
c = "111122223333444455556666777788889999JJJJQQQQKKKKAAAA"
cards = [i for i in c]
nexts = ["да", "д", "газ", "ок", "yep", "yes", "y", "+"]
skips = ["нет", "н", "стоп", "не", "no", "n", "nope", "-"]
money = 1000
while True:
    stavka = 0
    dealer_sum = 0
    player_sum = 0
    top_card = 51
    random.shuffle(cards)
    print("Ваши деньги:", money)
    while stavka == 0:
        try:
            stavka = int(input("Ваша ставка:\n"))
        except Exception:
            print("не цифра, попробуйте заново")
        if stavka > money:
            print("ставка больше ваших денег")
            stavka = 0
    player = cards[top_card] + cards[top_card - 1]
    top_card -= 2
    dealer = cards[top_card] + cards[top_card - 1]
    top_card -= 2
    for i in dealer:
        if i in "123456789":
            dealer_sum += int(i)
        elif i in "JQK":
            dealer_sum += 10
        else:
            if dealer_sum != 11:
                dealer_sum += 11
            else:
                dealer_sum += 1

    while top_card >= 0:
        print("карты дилера: *", dealer[-1])
        print("Ваши карты:", *player)
        take_card = input("Взять карту?\n")
        if take_card.lower() in nexts:
            player += cards[top_card]
            top_card -= 1
        elif take_card.lower() in skips:
            break
    for i in player:
        if i in "123456789":
            player_sum += int(i)
        elif i in "JQK":
            player_sum += 10
        else:
            while True:
                inp = input("Туз 11 или 1\n")
                if inp == "11":
                    player_sum += 11
                    break
                elif inp == 1:
                    player_sum += 1
    print()
    if player_sum > 21:
        print("Вы проиграли")
        money -= stavka
    else:
        while top_card >= 0:
            q = cards[top_card]
            top_card -= 1
            dealer += q
            if q in "123456789":
                dealer_sum += int(q)
            elif q in "JQK":
                dealer_sum += 10
            else:
                if dealer_sum < 11:
                    dealer_sum += 11
                else:
                    dealer_sum += 1
            if dealer_sum <= 16:
                continue
            else:
                break
        print("Ваши карты:", *player, "\t сумма:", player_sum)
        print("карты дилера:", *dealer, "\t сумма:", dealer_sum)

        # логика подсчёта выигрыша
        if dealer_sum > 21 or player_sum > dealer_sum:
            print("Вы выйграли")
            money += stavka
        elif dealer_sum > player_sum:
            print("Вы проиграли")
            money -= stavka
        else:
            print("Ничья")
    print()
    print("Ваши деньги:", money)
    if money > 0:
        next_game = input("Продолжить?\n")
        if next_game.lower() in nexts:
            continue
    print()
    break
print("Всё")
