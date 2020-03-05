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

import unittest
import uspec
from uspec import describe, context, it


###################################
class TestGame(unittest.TestCase): pass


with describe("Game", test_class=TestGame):
    
    assert test_class is TestGame
    
    @it("hoge")
    def _(self):
        self.assertTrue(True)

assert TestGame is not None

##################################
TEST_CLASS_NAME_GAME2 = None

with describe("Game2"):
    TEST_CLASS_NAME_GAME2 = test_class.__name__

    @it("hoge")
    def _(self):
        self.assertTrue(True)

assert TEST_CLASS_NAME_GAME2 in globals()


##################################
def wrap():
    global TEST_CLASS_NAME_GAME3
    
    with describe("Game3"):
        
        TEST_CLASS_NAME_GAME3 = locals()["test_class"].__name__
        
        @it("hoge")
        def _(self):
            self.assertTrue(True)

    
wrap()

assert TEST_CLASS_NAME_GAME3 in globals()

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
