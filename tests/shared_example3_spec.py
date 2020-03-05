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


from uspec import describe, context, it, set_property, shared_example_of, expect, behave_like

########################################################


@shared_example_of(Game)
def _(actual_game_class, context_stack=[]):
    
    with describe("#score"):
                
        @it("returns 0 for an all gutter game")
        def _(self):
            game = actual_game_class()
            for i in range(20): game.roll(0)
            self.assertEqual(game.score(), 0)
        
        def check(self):
            game = actual_game_class()
            for i in range(20): game.roll(0)
            self.assertEqual(game.score(), 0)
        
        set_property(verification_func=check)
        
        it("returns 0 for an all gutter game")


with describe(ConcreteGame):
    it.behaves_like(Game)

########################################################

  
@shared_example_of(Game.score)
def _(game_score_method_generator, context_stack=None):
              
    @it("returns 0 for an all gutter game")
    def _(self):
        game_score_method = game_score_method_generator()
        # for i in range(20): game.roll(0)
        self.assertEqual(game_score_method(), 0)
      
    def check(self):
        game_score_method = game_score_method_generator()
#         for i in range(20): game.roll(0)
        self.assertEqual(game_score_method(), 0)
      
    set_property(verification_func=check)
     
    it("returns 0 for an all gutter game")

  
with describe(ConcreteGame):
 
    with describe(lambda: ConcreteGame().score):
     
        it.behaves_like(Game.score)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
