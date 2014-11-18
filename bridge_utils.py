#!/usr/bin/env python3

import cmd
import time
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
    time_stats = {}

    def pointcount(self):
        deal = self.deal()
        points = self.count(deal)
        cards = self.by_suit(deal)
        return cards, points

    def record_time(self, id, time):
        avg, num = self.time_stats.setdefault(id, (0, 0))
        curr_avg = (time + num * avg) / (num + 1)
        curr_num = num + 1
        self.time_stats[id] = (curr_avg, curr_num)


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

    @staticmethod
    def displ_stats(stats):
        for stat in stats:
            print('{}: {:.2f}s'.format(stat, stats[stat][0]))


class BridgeUtilsCmd(cmd.Cmd):
    intro = 'Welcome to Bridge Utils!'
    prompt = '> '
    train = Training()

    def do_pointcount(self, arg):
        """Point count (PC) training"""
        timing = arg and arg == 'time'
        cards, points = self.train.pointcount()
        CmdUtils.displ_hand(cards)
        if timing:
            start = time.time()
            input('Show answer...')
            stop = time.time()
            elap_time = stop - start
            self.train.record_time('point-count', elap_time)
            print('{}PC ({:.2f}s)'.format(points, elap_time))
        else:
            input('Show answer...')
            print('{}PC'.format(points))

    def do_pc(self, arg):
        """Point count (PC) training"""
        return self.do_pointcount(arg)

    def do_stats(self, arg):
        """Display training statistics"""
        print('''Average response time:\n======================''')
        CmdUtils.displ_stats(self.train.time_stats)

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
