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
from uspec import describe, it


class TestGame(unittest.TestCase): pass


with describe("Game", test_class=TestGame, a=10, b=20):

    assert a == 10
    assert b == 20
    
    with describe(".score()", a=99):
        
        assert a == 99
        assert b == 20
        
        @it("returns 0")
        def _(testcase):
            pass
    
    assert a == 10
    assert b == 20

assert "a" not in locals()
assert "a" not in globals()

if __name__ == '__main__':
    unittest.main(verbosity=2)
