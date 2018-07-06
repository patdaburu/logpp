#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. currentmodule:: test_example.py
.. moduleauthor:: Pat Daburu <pat@daburu.net>

This module contains tests of the :py:mod:`logpp.logging` module.
"""

import logging
import unittest
from logpp.logging import LogppMessage, LogppMixin, LogppHandler, msg


class TestLogppMessage(unittest.TestCase):
    """
    Tests of the :py:class:`LogppMessage` class and the :py:func:`msg` function.
    """
    def test_init_verify(self):
        """
        Arrange/Act: Initialize a :py:class:`LogppMessage` instance.
        Assert: The values passed in at construction are reflected in the
            instance and the string representation reflects the summary.
        """
        lpp_msg = LogppMessage(summary='test', detail={'a': 1, 'b': 2})
        self.assertEqual('test', lpp_msg.summary)
        self.assertEqual('test', str(lpp_msg))
        self.assertEqual(1, lpp_msg.detail['a'])
        self.assertEqual(2, lpp_msg.detail['b'])

    def test_msg_verify(self):
        """
        Arrange/Act: Initialize a :py:class:`LogppMessage` instance using the
            :py:func:`msg` function.
        Assert: The values passed to the function are reflected in the
            instance and the string representation reflects the summary.
        """
        lpp_msg = msg(summary='test', detail={'a': 1, 'b': 2})
        self.assertEqual('test', lpp_msg.summary)
        self.assertEqual('test', str(lpp_msg))
        self.assertEqual(1, lpp_msg.detail['a'])
        self.assertEqual(2, lpp_msg.detail['b'])


class TestLogppHandler(unittest.TestCase):
    """
    Tests of the :py:class:`LogppHandler` class.
    """
    def test_extend_log_emitted(self):
        """
        Arrange: Extend the :py:class:`LogppHandler` class and set up logging.
        Act: Log several messages.
        Assert: The number of messages handled is the number expected.
        """
        # Extend the base class.
        class TestLogppHandler(LogppHandler):

            def __init__(self):
                super().__init__()
                # Keep count of the number of messages logged.
                self.handled_count = 0

            def emit_logpp(self, msg_: LogppMessage):
                # Every time we handle a message, increment the count.
                self.handled_count += 1
        # Set up the logger.
        logger = logging.getLogger('TestLogppHandler')
        logger.setLevel(logging.INFO)
        logpp_handler = TestLogppHandler()
        logger.addHandler(logpp_handler)

        # We'll log a fixed number of messages.
        log_count = 10
        for i in range(0, log_count):
            # Log a logpp message.  It should be reflected in the count.
            logpp_msg = msg(summary='test', detail={'a': 1, 'b': 2})
            logger.info(logpp_msg)
            # Log a string message.  It should not be relected in the count.
            logger.info('not counted')

        # Verify the number of messages handled matches the number sent.
        self.assertEqual(log_count, logpp_handler.handled_count)


class TestLogppMixin(unittest.TestCase):
    """
    Tests of the :py:class:`LogppMixin` class.
    """
    def test_extend_getLogger_loggerNameIsClassName(self):
        """
        Arrange: Extend :py:class:`LogppMixin`.
        Act: Instantiate and get the logger.
        Assert: The logger's name reflects the class name.
        """
        class TestBase(object):
            pass

        class TestLogpp(TestBase, LogppMixin):
            pass

        test_logpp = TestLogpp()
        logger = test_logpp.logger()

        self.assertEqual(
            f'{test_logpp.__class__.__module__}.' 
            f'{test_logpp.__class__.__name__}',
            logger.name
        )

    def test_extendWithLoggerName_getLogger_loggerNameIsClassName(self):
        """
        Arrange: Extend :py:class:`LogppMixin` with the `__loggername__`
            class attribute.
        Act: Instantiate and get the logger.
        Assert: The logger's name reflects the `__loggername__` class attribute.
        """
        class TestBase(object):
            pass

        class TestLogpp(TestBase, LogppMixin):
            __loggername__ = 'test_logger'
            pass

        test_logpp = TestLogpp()
        logger = test_logpp.logger()

        self.assertEqual(
            'test_logger',
            logger.name
        )


