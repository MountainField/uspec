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
        print("before_context1")
        assert not hasattr(test_class, "a")
        test_class.a = 1

    @before_example
    def _(self):
        print("  before_example1")
        assert hasattr(self, "a")
        
        assert not hasattr(self, "b")
        self.b = 1
        
    @it("mehod1")
    def _(self):
        print("    method1")
        assert self.b == 1
        
    def verify(self):
        print("    method2")
        assert self.b == 1

    set_property(verification_func=verify)
    it("method2")

    with describe("#score"):
        
        @before_context
        def _(test_class):
            print("before_context2")
            assert hasattr(test_class, "a")
            assert not hasattr(test_class, "A")
            test_class.A = 10
    
        @before_example
        def _(self):
            print("  before_example2")
            assert hasattr(self, "a")
            assert hasattr(self, "A")
            
            assert hasattr(self, "b")
            assert not hasattr(self, "B")
            self.B = 10
            
        @it("mehod1")
        def _(self):
            print("    method12")
            assert self.b == 1
            assert self.B == 10
            
        def verify(self):
            print("    method22")
            assert self.b == 1
            assert self.B == 10

        set_property(verification_func=verify)
        it("method2")
        
        with context("when foo is {foo}", foo="FOO"):
            
            @before_context
            def _(test_class):
                print("before_context3")
                assert hasattr(test_class, "a")
                assert hasattr(test_class, "A")
                assert not hasattr(test_class, "aa")
                test_class.aa = 100
        
            @before_example
            def _(self):
                print("  before_example3")
                assert hasattr(self, "a")
                assert hasattr(self, "A")
                assert hasattr(self, "aa")
                
                assert hasattr(self, "b")
                assert hasattr(self, "B")
                assert not hasattr(self, "bb")
                self.bb = 100
                
            @it("mehod1")
            def _(self):
                print("    method123")
                assert self.b == 1
                assert self.B == 10
                assert self.bb == 100
                
            def verify(self):
                print("    method223")
                assert self.b == 1
                assert self.B == 10
                assert self.bb == 100

            set_property(verification_func=verify)
            it("method2")
        
if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
