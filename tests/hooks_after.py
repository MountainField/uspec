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
    
    @after_context
    def _(test_class):
        print("after_context")
        assert test_class.a == 0, test_class.a

    @after_example
    def _(self):
        print("after_example")
        assert self.a == 10
        assert self.b == 1
        self.b = 0
        self.__class__.a = 0
        
    @it("mehod1")
    def _(self):
        print("  method1")
        self.b = 1
        self.__class__.a = 10
        
    def verify(self):
        print("  method2")
        self.b = 1
        self.__class__.a = 10

    set_property(verification_func=verify)
    it("method2")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
