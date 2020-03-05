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

from uspec import describe, context, it

with describe("Game {0}", 1) as (_, game_id):
    
    assert game_id == 1, game_id
    
    with context("when day is {a}", a=2) as (_, day):
        
        assert day == 2, day
        
        @it("returns foo")
        def _(self):
            self.assertTrue(True)

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
