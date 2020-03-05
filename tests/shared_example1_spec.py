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


class ConcreteGame(Game):
    pass


from uspec import describe, context, it, set_property, expect_that


def shared_example_of_game(game_class):
    
    with describe(game_class):
        
        with describe("#score"):
                    
            @it("returns 0 for an all gutter game")
            def _(self):
                game = Game()
                for i in range(20): game.roll(0)
                self.assertEqual(game.score(), 0)
            
            def check(self):
                game = Game()
                for i in range(20): game.roll(0)
                self.assertEqual(game.score(), 0)
            
            set_property(verification_func=check)
            
            it("returns 0 for an all gutter game")


# direct
shared_example_of_game(Game)
shared_example_of_game(ConcreteGame)

# it behaves like Game
behaves_like_Game = shared_example_of_game
expect_that(Game, behaves_like_Game)
expect_that(ConcreteGame, behaves_like_Game)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
