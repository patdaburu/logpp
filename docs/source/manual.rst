.. _manual:

.. toctree::
    :glob:

Manual
======

Why `logpp`?
------------

`logpp` is a fairly simple module that contains some extensions for Python's
built in `logging <https://docs.python.org/3/library/logging.html>`_ module.
It provides a few facilities that allow you to pass extended information with
logging messages.

The three principle components are listed below.

* :py:func:`logpp.logging.msg`
* :py:class:`logpp.logging.LogppMessage`
* :py:class:`logpp.logging.LogppHandler`

The module also provides the :py:class:`logpp.logging.LogppMixin` which you can
use to provide standardized access to a logger via the
:py:class:`logpp.logging.LogppMixin.logger` method.

Logging a Message
-----------------

The example below has been expanded to make the components easier to see, but
it's actually a fairly simple one-liner.  The :py:func:`logpp.logging.msg`
function takes a summary `str` and a detail object (which in the example is
just a dictionary).

The function returns a :py:class:`logpp.logging.LogppMessage` which, when
represented in `str` form is simply the summary.

.. code-block:: python

    logging.info(
        msg(
            'The weather is currently sunny with a temperature of 25°C.',
            {
                'conditions': 'sunny',
                'temperature': 25
            }
        )
    )

Logging handlers that aren't aware of the detail information should simply see
the `logpp` message as the summary.

Handling Messages
-----------------

If you're using `logpp`, chances are you want to do something useful or clever
with the detail information.  To accomplish that you can create your own
`logging handler <https://docs.python.org/3/library/logging.html#handler-objects>`_.
If your custom handler is only interested in `logpp` messages, you can extend
the :py:class:`logpp.logging.LogppHandler` and override the
:py:func:`logpp.logging.LogppHandler.emit_logpp` method.  The base class will
perform checks to make sure that only logging messages that are instances of
the :py:class:`logpp.logging.LogppMessage` class are passed to this method.

Putting it All Together
-----------------------

The sample below briefly demonstrates the creation of a custom log handler and
should give you an idea of what to expect from such a facility.

.. code-block:: python

    import logging
    from logpp.logging import msg, LogppMessage, LogppHandler


    # Create a custom handler.
    class CustomLogppHandler(LogppHandler):

        def emit_logpp(self, msg_: LogppMessage):
            print(f'SUMMARY: {msg_.summary}')
            print(f'DETAILS: {msg_.detail}')


    logging.basicConfig(level=logging.INFO)
    # Add the custom handler to the logger (just as you would with any handler).
    logging.getLogger().addHandler(CustomLogppHandler())

    # Log a message to be handled by the custom handler.
    logging.info(
        msg(
            'The weather is currently sunny with a temperature of 25°C.',
            {
                'conditions': 'sunny',
                'temperature': 25
            }
        )
    )

    # Log a message that will be ignored by the custom handler.
    logging.info('This message will be ignored by the custom handler.')