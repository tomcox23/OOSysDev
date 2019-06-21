import random

BLACKJACK = 21
DEALERS_RULE = 17
AGGRESSIVE = 17
PASSIVE = 16
ROUND_NUM = 10

num_round = 0
wins = 0
lose = 0
draw = 0


class Deck(object):
    def __init__(self):
        self.cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace'] * 4

    def shuffle(self):
        random.shuffle(self.cards)
        print("Shuffled Cards")

    def deal_card(self):
        return self.cards.pop()

    def show(self):
        for c in self.cards:
            print(c)


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.total = 0

    def hit(self, deck):
        deal_card = deck.deal_card()
        self.hand.append(deal_card)
        if deal_card == 'King' or deal_card == 'Queen' or deal_card == 'Jack':
            self.total += 10
        elif deal_card == 'Ace':
            self.total += 11
        else:
            self.total += int(deal_card)

    def show_hand(self):
        print(self.name + " cards: " + str(self.hand) + " (total: " + str(self.total) + ")")

    def play_aggressive(self):
        self.play_aggressive()
        if player.total <= AGGRESSIVE:
            player.hit(card_deck)

    def play_passive(self):
        self.play_passive()
        if player.total <= PASSIVE:
            player.hit(card_deck)


if __name__ == "__main__":

    while num_round != ROUND_NUM:
        num_round += 1

        card_deck = Deck()
        card_deck.shuffle()
        player = Player("Your")
        house = Player("House")

        player.hit(card_deck)
        house.hit(card_deck)

        player.show_hand()
        house.show_hand()

        while player.total <= BLACKJACK:
            # player_input = input("Would you like to (H)it or (S)tand? > ").upper()
            # if player_input == 'H' and player.total < BLACKJACK:
            if player.total < BLACKJACK:
                player.hit(card_deck)
                player.show_hand()
                if player.total > BLACKJACK:
                    print("Busted, You lose!")
                    lose += 1
                    break
                elif player.total == BLACKJACK:
                    print("BlackJack, You got 21")

                continue
            # elif player_input == 'S':
            # print("Stand")

            while house.total < DEALERS_RULE:
                print("House hits")
                house.hit(card_deck)
                house.show_hand()
                if house.total > BLACKJACK:
                    print("House Busted")

                    break
                elif house.total >= DEALERS_RULE:
                    print("House stands")
                    break

            player.show_hand()
            house.show_hand()

            if (player.total > house.total) and (player.total <= BLACKJACK):
                print("You win!")
                wins += 1
                # without this line below player will lose if house total is more then 21 (bust) and players total is
                # less then house. this now results in a player win
                # Your cards: ['3', 'Jack', '4'](total: 17)
                # House cards: ['3', 'Jack', '9'](total: 22)
                # House wins

            elif(player.total < house.total) and (house.total > BLACKJACK):
                print("You win!")
                wins += 1
                # now returns the correct player win
                # Your cards: ['3', 'Jack', '4'](total: 17)
                # House cards: ['3', 'Jack', '9'](total: 22)
                # You win

            elif (player.total < house.total) and (house.total <= BLACKJACK):
                print("House wins!")
                lose += 1
            else:
                print("Push!")
                draw += 1
            break
        print("W:", wins, "L:", lose, "D:", draw, "R", num_round)
