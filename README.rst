|Python version| |Build Status|

=======
 ultan
=======

*"You know old Ultan, I take it? No, course not. If you did, you'd know the way
 to the library."* *— The Shadow of the Torturer, Gene Wolfe*


``ultan`` is a Python identifier and documentation server. It provides two main
services:

1. It can list all identifiers available in your current Python environment.
2. It can provide docstrings for names.

This may not sound very spectactular, and it's not. The main trick ``ultan``
aims for is being able to provide a comprehensive list of identifiers, *even for
modules which are not imported*. It uses various strategies to scan your
installed packages for identifiers, doing things, for example, like parsing
source files into ASTs and looking for assignments.

Why?
====

``ultan`` is supposed to scratch a specific itch: being able to do completion on
identifiers which aren't actually available in the current namespace. For
example, if I'm coding along and want to add ``uuid.uuid1()``, standard
completers won't give me that completion unless I've already imported ``uuid``.
``ultan`` will know about ``uuid.uuid1()`` even if you haven't imported
``uuid``, so you can get the completion.

This may be a terrible idea! But I want to give it a try.

Tests
=====

``ultan`` uses ``tox`` to run its tests. Here's that works:

.. code-block::

   $ pip install -e .[test]
   $ tox

There are more details to it, of course, but you can learn about those by
reading the ``tox`` documentation.

.. |Python version| image:: https://img.shields.io/badge/Python_version-3.4+-blue.svg
   :target: https://www.python.org/
.. |Build Status| image:: https://travis-ci.org/abingham/ultan.png?branch=master
   :target: https://travis-ci.org/abingham/ultan
