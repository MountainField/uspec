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

with describe("Game"):
    
    @before_context
    def _(test_class):
        print("before_context")
        assert not hasattr(test_class, "a")
        test_class.a = 1

    @before_example
    def _(self):
        print("before_example")
        assert hasattr(self, "a")
        
        assert not hasattr(self, "b")
        self.b = 1
        
    @it("mehod1")
    def _(self):
        print("  method1")
        assert self.b == 1
        
    def verify(self):
        print("  method2")
        assert self.b == 1

    set_property(verification_func=verify)
    it("method2")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
