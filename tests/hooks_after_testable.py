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
    
    @after_example
    def _(self):
        # second
        print("  after_example1")
        assert self.__class__.a == 10
        assert self.b == 1
        assert self.__class__.A == 10
        assert self.B == 0
        self.__class__.a = 0

    @after_context
    def _(test_class):
        # fourth
        print("after_context1")
        assert test_class.a == 0
        assert test_class.A == 0

    with context("#score"):
        
        @after_example
        def _(self):
            # first 
            print("  after_example2")
            assert self.__class__.a == 10
            assert self.b == 1
            assert self.__class__.A == 10
            assert self.B == 1
            self.B = 0
            
        @after_context
        def _(test_class):
            # third
            print("after_context2")
            assert test_class.A == 10
            assert test_class.a == 0
            test_class.A = 0
    
        @it("mehod1")
        def _(self):
            print("    method1")
            self.b = 1
            self.B = 1
            self.__class__.a = 10
            self.__class__.A = 10
            
        def verify(self):
            print("    method2")
            self.b = 1
            self.B = 1
            self.__class__.a = 10
            self.__class__.A = 10
    
        set_property(verification_func=verify)
        it("method2")

if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
