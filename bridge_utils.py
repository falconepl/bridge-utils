#!/usr/bin/env python3

import cmd
from itertools import product
from random import sample, shuffle


class Core:
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    pcards = ['J', 'Q', 'K', 'A']
    suits = ['S', 'H', 'D', 'C']
    deck = list(product(cards, suits))

    def count(self, cards):
        total = 0
        for crd, _ in cards:
            if crd in self.pcards:
                total += self.pcards.index(crd) + 1
        return total

    def deal(self):
        shuffle(self.deck)
        return sample(self.deck, 13)

    def by_suit(self, cards):
        d = {}
        for card, suit in cards:
            d.setdefault(suit, []).append(card)
        return d


class Training(Core):
    def pointcount(self):
        deal = self.deal()
        points = self.count(deal)
        cards = self.by_suit(deal)
        return cards, points


class CmdUtils():
    @staticmethod
    def symb(suit_id):
        red = '\033[91m'
        endc = '\033[0m'
        s = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣'}

        if suit_id in ['H', 'D']:
            return red + s[suit_id] + endc
        else:
            return s[suit_id]

    @staticmethod
    def displ_hand(cards):
        for suit in Core.suits:
            print(CmdUtils.symb(suit), end=' ')
            if suit in cards:
                for card in cards[suit]:
                    print(card, end='')
            print(' ', end='')
        print()


class BridgeUtilsCmd(cmd.Cmd):
    intro = 'Welcome to Bridge Utils!'
    prompt = '> '
    train = Training()

    def do_pointcount(self, arg):
        """Point count (PC) training"""
        cards, points = self.train.pointcount()
        CmdUtils.displ_hand(cards)
        input('Show answer...')
        print(str(points))

    def do_pc(self, arg):
        """Point count (PC) training"""
        return self.do_pointcount(arg)

    def do_quit(self, arg):
        """Exit BridgeUtils"""
        return self.do_exit(arg)

    def do_q(self, arg):
        """Exit BridgeUtils"""
        return self.do_exit(arg)

    def do_exit(self, arg):
        """Exit BridgeUtils"""
        print('See you!')
        return True


if __name__ == '__main__':
    BridgeUtilsCmd().cmdloop()
