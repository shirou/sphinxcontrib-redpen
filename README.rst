Sphinx redpen
================================================

This extension provides `Redpen <http://redpen.cc/>`_ validator.

install
----------------

::

  pip install sphinxcontrib-redpen


and add `'sphinxcontrib.redpen'` in extensions in your conf.py.

::

   extensions = [
       'sphinxcontrib.redpen',
   ]

And redpen is also required.


How to use
-------------


Config
```````````

Set some variables in your `conf.py`.

redpen_configfile
  Redpen XML config file.
redpen_server
  Redpen server hostname
redpen_port = 8080
  Redpen server port.
redpen_loglevel
  log level

::

   redpen_configfile = 'test.conf.xml'
   redpen_server = "localhost"
   redpen_port = 8080
   redpen_loglevel = 'info'


Start Redpen Server
````````````````````````````````````

You need start redpen-server before use this extension.

::

  $ redpen-server

Then, `make html` or else.



Related
----------

Redpen
  http://redpen.cc/


License
--------

Apache License (same as Redpen)




