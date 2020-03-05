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
from uspec import describe, context, it


class TestGame(unittest.TestCase): pass


with describe("Game", test_class=TestGame, a=10):
    
    b = 20
    
    with describe(".score()", a=11):
        
        c = 30
        d = 40
        
        @it("returns 0", a, b, c)
        def _(testcase, a, b, c):
            assert a == 11
            assert b == 20
            assert c == 30
            try: 
                assert d == 40  # => Errror
            except Exception:
                pass
            assert d == 41

        c = 31
        d = 41
        
        @it("returns 0", a, b, c)
        def _(testcase, a, b, c):
            assert a == 11
            assert b == 20
            assert c == 31
            assert d == 41

    b = 21
    
    with describe(".score()", a=11):
        
        c = 30
        d = 40
        
        @it("returns 0", a, b, c)
        def _(testcase, a, b, c):
            assert a == 11
            assert b == 21
            assert c == 30
            try: 
                assert d == 40  # => Errror
            except Exception:
                pass
            assert d == 41

        c = 31
        d = 41
        
        @it("returns 0", a, b, c)
        def _(testcase, a, b, c):
            assert a == 11
            assert b == 21
            assert c == 31
            assert d == 41

if __name__ == '__main__':
    unittest.main(verbosity=2)
