"""Custom extensions for Jinja2.

To use a custom extension, first import the corresponding class.

.. sourcecode:: python

    from extensions import RaiseExtension, RequireExtension

Next, register the extension with the desired `jinja2.Environment`.  This may
be done either during or after construction of the environment.

.. sourcecode:: python

    env = Environment(..., extensions=[RaiseExtension])
    env.add_extension(RequireExtension)

Once registered, an extension may be accessed from any Jinja2 template associated
with the registering environment.  Statement-based extensions may be invoked
as a keyword statement where the keyword is the tag with which the extension
was defined.  For example, `RaiseExtension` may be invoked as:

.. sourcecode:: jinja

    {% raise "An error occurred." %}

The `RaiseExtension` and `RequireExtensions` herein are taken from

.. seealso::

    `Example Extension <http://jinja.pocoo.org/docs/extensions/#example-extension>`_

"""



from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.exceptions import TemplateRuntimeError


class RaiseExtension(Extension):
    """ Jinja extension which provides "raise" statement.

    The raise statement will raise a TemplateRuntimeError with the given error
    message.

    Example::

        {% if x >= 3 %}
            {% raise "x must be less than 3" %}
        {% endif %}

    Author:     Dean Serenevy
    Copyright:  Copyright (c) 2013 APCI, LLC
    """

    # This is our keyword(s):
    tags = set(['raise'])

    # See also: jinja2.parser.parse_include()
    def parse(self, parser):

        # the first token is the token that started the tag. In our case we
        # only listen to "raise" so this will be a name token with
        # "raise" as value. We get the line number so that we can give
        # that line number to the nodes we insert.
        lineno = next(parser.stream).lineno

        # Extract the message from the template
        message_node = parser.parse_expression()

        return nodes.CallBlock(
            self.call_method('_raise', [message_node], lineno=lineno),
            [], [], [], lineno=lineno
        )

    def _raise(self, msg, caller):
        raise TemplateRuntimeError(msg)


class RequireExtension(Extension):
    """ Jinja extension which provides "require" statement.

    The `require` statement will `include` a template only if it has not been
    previously required (aka, "include once"). Unlike the jinja `import`
    statement, `require` allows the included template to contain content, not
    just macros. We use this for code generation where we wish to require
    utility functions, but there are likely other use cases as well.

    Author:     Dean Serenevy
    Copyright:  Copyright (c) 2013 APCI, LLC
    """

    # This is our keyword(s):
    tags = set(['require'])

    def __init__(self, environment):
        super(RequireExtension, self).__init__(environment)
        # Define the attr we will use
        environment.extend(require_seen=set())


    # See also: jinja2.parser.parse_include()
    def parse(self, parser):

        # the first token is the token that started the tag. In our case we
        # only listen to "require" so this will be a name token with
        # "require" as value. We get the line number so that we can give
        # that line number to the nodes we insert.
        lineno = next(parser.stream).lineno

        # Create an Include node, giving it our lineno and the next
        # expression which will be the template name to include. "require"
        # will not tolerate missing inclusions ever.
        include = nodes.Include(lineno=lineno)
        include.template = parser.parse_expression()
        include.ignore_missing = False

        # No matter what, we should continue here (since there may be
        # additional tokens that need to be removed).
        node = parser.parse_import_context(include, True)

        # Ensure the current file is marked as "seen" to avoid loops (to
        # pick up the entry template or any templates included through
        # other means - a bad idea, but may happen).
        self.environment.require_seen.add(parser.name)

        # However, if we've already seen the template, just return an empty node.
        name = include.template.as_const()
        if name in self.environment.require_seen:
            return nodes.CallBlock(
                self.call_method('_blank', [], lineno=lineno),
                [], [], [], lineno=lineno
            )
        else:
            self.environment.require_seen.add(name)
            return node

    def _blank(self, caller):
        return ""



EXTENSIONS = {
    'raise':    RaiseExtension,
    'require':  RequireExtension,
}
