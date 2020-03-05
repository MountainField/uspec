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

with describe("Game"):
    
    for idx in range(10):
        
        with context(idx=idx):

            @it("returns 0", idx)
            def _(testcase, idx):
                print(idx)
                testcase.assertTrue(True)
            
if __name__ == '__main__':
    unittest.main(verbosity=2)
