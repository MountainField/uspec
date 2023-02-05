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

__version__ = "1.0.24"
__description__ = "RSpec like behavior driven development (BDD) tool based on unittest"
__author__ = "Takahide Nogayama"
__author_email__ = "NOGAYAMA@gmail.com"
__url__ = "https://github.com/MountainField/uspec"
__download_url__ = "https://github.com/MountainField/uspec/releases"
__license__ = "MIT"

from abc import ABCMeta, abstractmethod
import contextlib as _contextlib
import logging as _logging
import inspect as _inspect
import os as _os
import sys as _sys
import unittest as _unittest
import functools

_LOGGER = _logging.getLogger("uspec")
_handler = _logging.StreamHandler()
_handler.setFormatter(_logging.Formatter('\n%(asctime)s p%(process)d %(threadName)s %(name)s %(levelname)s %(message)s (%(filename)s L%(lineno)s)'))
_LOGGER.addHandler(_handler)
_LOGGER.setLevel(_logging.WARN)

###################################################################################################
# Constants

# This is same as unittest.TestLoader.testMethodPrefix
TEST_METHOD_PREFIX = "test"
TEST_CLASS_PREFIX = "T"

_EXAMPLE_COUNTER = 0
_EXAMPLE_GROUP_COUNTER = 0

_NAME2SHARED_EXAMPLE = {}

###################################################################################################
# Core


def _concat_names(names, kwargs):
    name = ""
    for s in names:
        if _inspect.isclass(s) or callable(s):
            name += s.__name__
        elif s is None:
            pass
        else:
            name += str(s)
    for idx, (k, v) in enumerate(kwargs.items()):
        if idx != 0:
            name += ", "
        name += str(k) + "==" + str(v)
    return name


_TYPE_DESCRIBE = "describe"
_TYPE_CONTEXT = "context"

_HOOKTYPE_BEFORE_EXAMPLE = "before_example"
_HOOKTYPE_BEFORE_CONTEXT = "before_context"
_HOOKTYPE_AFTER_EXAMPLE = "before_example"
_HOOKTYPE_AFTER_CONTEXT = "before_context"


class _Context(object):
    
    def __init__(self, context_type,
                       context_stack,
                       *args,
                       **kwargs):
        global _EXAMPLE_GROUP_COUNTER
        
        self.context_type = context_type
        
        self.subject = None
        
        if len(args) > 0:
            if  isinstance(args[0], str):
                template = args[0]
                args = args[1:]
                self.name = template.format(*args, **kwargs)

                if context_type == _TYPE_DESCRIBE:
                    self.subject = self.name
            else:
                self.name = _concat_names(args, kwargs)
                
                if context_type == _TYPE_DESCRIBE:
                    self.subject = args[0]
        else:
            self.name = ""
        
        if context_type == _TYPE_CONTEXT:
            self.name = "(" + self.name + ")"

        if not isinstance(context_stack, list): raise TypeError("context_stack must be instance of list")
        self.context_stack = context_stack
        
        self.context_depth = len(context_stack)
        
        test_class = kwargs.get("test_class", None)
        if test_class is None:
            # Create Class name
            test_class_name = TEST_CLASS_PREFIX + "{0:04}".format(_EXAMPLE_GROUP_COUNTER)
            _EXAMPLE_GROUP_COUNTER += 1
            # for context in context_stack:
            #     if context.context_type is _TYPE_DESCRIBE:
            #         test_class_name += context.name
            # if self.context_type is _TYPE_DESCRIBE:
            #     test_class_name += self.name
            # Create Test Class 
            test_class = type(test_class_name, (_unittest.TestCase,), {})
            kwargs["test_class"] = test_class
        self.test_class = test_class
        
        self.properties = {
            "set_property": self.set_property,
            "before_example": self.before_example,
            "before_context": self.before_context,
            "after_example": self.after_example,
            "after_context": self.after_context,
            }
        
        if self.subject:
            self.properties["_subject"] = self.subject
        
        for name, value in kwargs.items():
            self.properties[name] = value
        
        self._backup_properties = {}
    
    def set_property(self, **kwargs):
        for k, v in kwargs.items():
            self.properties[k] = v
    
    def _get_property(self, name):
        scan_depth = min(self.context_depth + 1, len(self.context_stack))
        
        for depth in reversed(range(scan_depth)):
            context = self.context_stack[depth]
            if name in context.properties:
                return context.properties[name]
        return None
    
    def _get_properies_from_top(self, name):
        scan_depth = min(self.context_depth + 1, len(self.context_stack))
        
        properties = []
        for context in self.context_stack:
            if name in context.properties:
                properties.append(context.properties[name])
        return properties

    def __str__(self):
        return self.name

    def it(self, desc, *args, **kwargs):
        global _EXAMPLE_COUNTER
        
        desc = desc.format(*args, **kwargs)
        # desc = cw.ensure_text(desc)
        desc = desc.replace("\n", "\\n")
        
        test_name = TEST_METHOD_PREFIX + "{0:05} ".format(_EXAMPLE_COUNTER) + " ".join([str(c) for c in self.context_stack]) + " " + desc
        
        verification_func = self._get_property("verification_func")
        if callable(verification_func):
            setattr(self.test_class, test_name, lambda test: verification_func(test, *args, **kwargs))
    
        def decorator(f2):
            setattr(self.test_class, test_name, lambda test: f2(test, *args, **kwargs))
            return f2
        
        _EXAMPLE_COUNTER += 1
        
        return decorator
    
    def _before(self, hook_type, *args, **kwargs):

        if hook_type == _HOOKTYPE_BEFORE_EXAMPLE:

            def decorator(f):
                self.properties["_before_example"] = lambda test: f(test, *args, **kwargs)
                before_functions = self._get_properies_from_top("_before_example")

                def setUp(test):
                    for before_function in before_functions:
                        before_function(test)

                setattr(self.test_class, "setUp", setUp)
                return f

        elif hook_type == _HOOKTYPE_BEFORE_CONTEXT:

            def decorator(f):
                self.properties["_before_context"] = lambda cls: f(cls, *args, **kwargs)
                before_functions = self._get_properies_from_top("_before_context")

                def setUpClass(cls):
                    for before_function in before_functions:
                        before_function(cls)
                
                setattr(self.test_class, "setUpClass", classmethod(setUpClass))
                return f
        
        if len(kwargs) == 0 and len(args) == 1 and callable(args[0]):
            # decorator is called without parenthesis.  
            f = args[0]
            args = tuple()
            decorator(f)
            return f
                    
        return decorator
    
    def before_example(self, *args, **kwargs):
        return self._before(_HOOKTYPE_BEFORE_EXAMPLE, *args, **kwargs)
    
    def before_context(self, *args, **kwargs):
        return self._before(_HOOKTYPE_BEFORE_CONTEXT, *args, **kwargs)
    
    def _after(self, hook_type, *args, **kwargs):

        if hook_type == _HOOKTYPE_AFTER_EXAMPLE:

            def decorator(f):
                self.properties["_after_example"] = lambda test: f(test, *args, **kwargs)
                after_functions = list(reversed(self._get_properies_from_top("_after_example")))

                def tearDown(test):
                    for after_function in after_functions:
                        after_function(test)

                setattr(self.test_class, "tearDown", tearDown)
                return f

        elif hook_type == _HOOKTYPE_AFTER_CONTEXT:

            def decorator(f):
                self.properties["_after_context"] = lambda cls: f(cls, *args, **kwargs)
                after_functions = list(reversed(self._get_properies_from_top("_after_context")))

                def tearDownClass(cls):
                    for after_function in after_functions:
                        after_function(cls)
                
                setattr(self.test_class, "tearDownClass", classmethod(tearDownClass))
                return f
        
        if len(kwargs) == 0 and len(args) == 1 and callable(args[0]):
            # decorator is called without parenthesis.  
            f = args[0]
            args = tuple()
            decorator(f)
            return f
                    
        return decorator
    
    def after_example(self, *args, **kwargs):
        return self._after(_HOOKTYPE_AFTER_EXAMPLE, *args, **kwargs)
    
    def after_context(self, *args, **kwargs):
        return self._after(_HOOKTYPE_AFTER_CONTEXT, *args, **kwargs)
    

@_contextlib.contextmanager
def _context(context_type, *args, **kwargs):
    
    frame = _inspect.currentframe()
    try:
        parent_frame = frame.f_back.f_back
        # get context_stack
        if "context_stack" in parent_frame.f_locals:
            context_stack = parent_frame.f_locals["context_stack"]
        else:
            context_stack = []
            parent_frame.f_locals['context_stack'] = context_stack
        
        context = _Context(context_type, context_stack, *args, **kwargs)
        context.frame = parent_frame
        context_stack.append(context)

        for name, value in context.properties.items():
            if not name.startswith("_"):
                if name in parent_frame.f_locals:
                    context._backup_properties[name] = parent_frame.f_locals[name]
                parent_frame.f_locals[name] = value
        
    finally:
        del frame

    # return the control of program to caller
    yargs = list(args)
    if kwargs:
        yargs.extend([v for k, v in kwargs.items()])
    yield context.subject, yargs
    
    frame = _inspect.currentframe()
    try:
        # Delete it variable from caller's variables
        if len(context_stack) == 0:
            del parent_frame.f_locals['context_stack']
        
        for name, value in context.properties.items():
            if not name.startswith("_"):
                if name in parent_frame.f_locals:
                    del parent_frame.f_locals[name]
                if name in context._backup_properties:
                    parent_frame.f_locals[name] = context._backup_properties[name]

        # Declare the test class to be found by unittest loader
#         if context.test_class.__name__ not in parent_frame.f_globals:
#             if len([method_name for method_name in dir(context.test_class) if method_name.startswith(TEST_METHOD_PREFIX)]) > 0:
#                 _LOGGER.debug("Declaring test_class %s", context.test_class.__name__)
#                 parent_frame.f_globals[context.test_class.__name__] = context.test_class
#             else:
#                 _LOGGER.debug("Skipping declaration of test_class %s because it does not have any test method.", context.test_class.__name__)
        root_context = context_stack[0]
        if context.test_class.__name__ not in root_context.frame.f_globals:
            test_method_names = [method_name for method_name in dir(context.test_class) if method_name.startswith(TEST_METHOD_PREFIX)]
            if len(test_method_names) > 0:
                _LOGGER.debug("Declaring test_class %s", context.test_class.__name__)
                root_context.frame.f_globals[context.test_class.__name__] = context.test_class
            else:
                _LOGGER.debug("Skipping declaration of test_class %s because it does not have any test method.", context.test_class.__name__)

    finally:
        del frame

    # Pop
    context_stack.pop()


def describe(*args, **kwargs):
    return _context(_TYPE_DESCRIBE, *args, **kwargs)


description = describe


def context(*args, **kwargs):
    return _context(_TYPE_CONTEXT, *args, **kwargs)


def set_property(**kwargs):
    
    frame = _inspect.currentframe()
    try:
        parent_frame = frame.f_back
        # get context_stack
        if "context_stack" in parent_frame.f_locals:
            context_stack = parent_frame.f_locals["context_stack"]
            if len(context_stack) == 0:
                raise ValueError("No context was found")
            leaf_context = context_stack[-1]
            
            for name, value in kwargs.items():
                leaf_context.properties[name] = value
                parent_frame.f_locals[name] = value
        else:
            raise ValueError("No context_stack was found")
        
    finally:
        del frame


class It(object):
    
    def __call__(self, message, *args, **kwargs):
        
        frame = _inspect.currentframe()
        try:
            parent_frame = frame.f_back
            # get context_stack
            if "context_stack" not in parent_frame.f_locals:
                raise ValueError("No context_stack was found")
            context_stack = parent_frame.f_locals["context_stack"]
            if len(context_stack) == 0:
                raise ValueError("No context was found")
            leaf_context = context_stack[-1]
        finally:
            del frame
        
        return leaf_context.it(message, *args, **kwargs)
    
    def behaves_like(self, shared_exmple_name, *args, **kwargs):
        
        if shared_exmple_name not in _NAME2SHARED_EXAMPLE:
            raise ValueError("shared_example '%s' is not registered" % shared_exmple_name)
        
        frame = _inspect.currentframe()
        try:
            parent_frame = frame.f_back
            # get context_stack
            if "context_stack" not in parent_frame.f_locals:
                raise ValueError("No context_stack was found")
            context_stack = parent_frame.f_locals["context_stack"]
            if len(context_stack) == 0:
                raise ValueError("No context was found")
        finally:
            del frame
        
        leaf_context = context_stack[-1]
        actual_subject = leaf_context._get_property("_subject")
        
        shared_example_func = _NAME2SHARED_EXAMPLE[shared_exmple_name]
        
        kwargs["context_stack"] = context_stack
        
        with context("behaves like " + shared_exmple_name):
            shared_example_func(actual_subject, *args, **kwargs)


it = It()

###################################################################################################
# Shared example


def shared_example_of(name):

    def _decorator(func):
        _NAME2SHARED_EXAMPLE[name] = func
        return func

    return _decorator


###################################################################################################
# Expectation
class _ExpectationTarget(object):
    
    def __init__(self, actual):
        self.actual = actual
    
    def to(self, matcher, message=None):
        matcher.matches(self.actual)


class _Matcher(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def matches(self, actual):
        pass


class _BehaveLikeMatcher(_Matcher):

    def __init__(self, name, *args, **kwargs):
        self.shared_example_func = _NAME2SHARED_EXAMPLE[name]
        self.args = args
        self.kwargs = kwargs
        
    def matches(self, actual):
        self.shared_example_func(actual, *self.args, **self.kwargs)


class _EqualMatcher(_Matcher):

    def __init__(self, expected):
        self.expected = expected
        
        self.test_instance = None
        frame = _inspect.currentframe()
        try:
            parent_frame = frame.f_back
            for k, v in parent_frame.f_locals.items():
                if isinstance(v, _unittest.TestCase):
                    self.test_instance = v
                    break
        finally:
            del frame
        if self.test_instance is None:
            raise ValueError("An instance of unittest.TestCase is not found")
        
    def matches(self, actual):
        self.test_instance.assertEqual(actual, self.expected)


def expect(target):
    return _ExpectationTarget(target)


def behave_like(expected_shared_example_name, *args, **kwargs):
    return _BehaveLikeMatcher(expected_shared_example_name, *args, **kwargs)


eq = _EqualMatcher

###################################################################################################
# Utilities


def expect_that(name, shared_example_function, *args, **kwargs):
    shared_example_function(name, *args, **kwargs)

# def execute_command(cmd):
#     import subprocess
#     p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     stdout_str, stderr_str = p.communicate()
#     status = p.returncode
#     return (status, stdout_str, stderr_str)


def execute_command(cmd, **popen_kwargs):
    _LOGGER.info("Executing command: %s", cmd)
    
    import subprocess
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **popen_kwargs)
    stdout, stderr = p.communicate()
    status = p.returncode
    
    if _LOGGER.isEnabledFor(_logging.INFO):
        if not isinstance(stdout, str): 
            stdout_text = stdout.decode(encoding="UTF-8", errors="replace")  # 
            stderr_text = stderr.decode(encoding="UTF-8", errors="replace")
        else:
            stdout_text = stdout
            stderr_text = stderr
        _LOGGER.debug("Found exit status: %s, cmd:\n%s\nstdout:\n%s\nstderr:\n%s", status, cmd, stdout_text, stderr_text)
        
    return (status, stdout, stderr)


def execute_shellscript(script, **popen_kwargs):
    import io
    import tempfile

    _LOGGER.info("Executing shellscript: %s", script)

    encoding = popen_kwargs.get("encoding", "UTF-8")
    errors = popen_kwargs.get("errors", "replace")
    
    _, temp_file = tempfile.mkstemp(suffix='', prefix='')
    with io.open(temp_file, "wt", encoding=encoding, errors=errors) as f:
        f.write(script)
    
    return execute_command(["/bin/bash", temp_file], **popen_kwargs)


def check_command(test, cmd, expected_status=None, expected_stdout=None, expected_stderr=None, **popen_kwargs):
    
    (status, stdout, stderr) = execute_command(cmd, **popen_kwargs)

    if expected_status is not None and status != expected_status and status != 0:
        _sys.stderr.write("\n====stderr start====\n")
        if not isinstance(stderr, str): 
            stderr_text = stderr.decode(encoding="UTF-8", errors="replace")
        _sys.stderr.write(stderr_text)
        _sys.stderr.write("\n====stderr end  ====\n")
    if expected_status is not None:
        test.assertEqual(status, expected_status)
    if expected_stdout is not None:
        test.assertEqual(stdout, expected_stdout)
    if expected_stderr is not None:
        test.assertEqual(stderr, expected_stderr)

###################################################################################################
# Cli


def main(*args, **kwargs):
    return _unittest.main(*args, **kwargs)
