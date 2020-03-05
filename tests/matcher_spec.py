# -*- coding: utf-8 -*-

# =================================================================
# uspec
#
# Copyright (c) 2020 Takahide Nogayama
#
# This software is released under the MIT License.
# http://opensource.org/licenses/mit-license.php
# =================================================================

from __future__ import unicode_literals, print_function, division


class Game(object):

    def roll(self, pins):
        pass

    def score(self):
        return 0


import unittest
from uspec import describe, context, it, set_property, expect, eq

with describe(Game):
    
    with describe(Game.score):
                
        @it("returns 0 for an all gutter game")
        def _(self):
            game = Game()
            for i in range(20): game.roll(0)
            expect(game.score()).to(eq(0))
        
        def check(self):
            game = Game()
            for i in range(20): game.roll(0)
            expect(game.score()).to(eq(0))
        
        set_property(verification_func=check)
        
        it("returns 0 for an all gutter game")

if __name__ == '__main__':
    unittest.main(verbosity=2)
