"This was an old hack I was using to fix some async issues in 
Ghost.py. Newer versions have fixed this problem."
-Richard

ghost.py is a webkit web client written in python::

    from ghost import Ghost
    ghost = Ghost()
    page, extra_resources = ghost.open("http://jeanphix.me")
    assert page.http_status==200 and 'jeanphix' in ghost.content

.. image:: https://secure.travis-ci.org/jeanphix/Ghost.py.png
   :target: https://travis-ci.org/jeanphix/Ghost.py

