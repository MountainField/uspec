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

TEST_CLASS_NAME_GAME1 = None
TEST_CLASS_NAME_GAME2 = None
TEST_CLASS_NAME_GAME3 = None
TEST_CLASS_NAME_GAME4 = None

with describe("Game1"):
    
    TEST_CLASS_NAME_GAME1 = test_class.__name__
    
    @it("hoge")
    def _(self):
        self.assertEqual(self.__class__.__name__, "Test0Game1")

    with describe("Game2"):
        
        TEST_CLASS_NAME_GAME2 = test_class.__name__
        
        @it("hoge")
        def _(self):
            pass

        with context("Game3"):
            
            TEST_CLASS_NAME_GAME3 = test_class.__name__
            
            @it("hoge")
            def _(self):
                pass

    with describe("Game4"):
        
        TEST_CLASS_NAME_GAME4 = test_class.__name__

assert TEST_CLASS_NAME_GAME1 in globals()
assert TEST_CLASS_NAME_GAME2 in globals()
assert TEST_CLASS_NAME_GAME3 in globals()
assert TEST_CLASS_NAME_GAME4 not in globals()

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
