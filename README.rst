python-debug
============

Using python-gdb.py is hard enough.  Using GDB with a process launched in a docker container is also a pain.  Using
the python-gdb.py helpers with a Python process run from a GDB container is a painful affair.  It doesn't have to be
this way.

The Dockerfile provided here is modified from the official Docker ``python:3.6.3-slim`` Dockerfile in order to provide
support for GDB debugging of python programs using the gdb bindings provided by CPython.  Details about that can be
found at the following sites:

- https://docs.python.org/devguide/gdb.html
- https://wiki.python.org/moin/DebuggingWithGdb

The following images are available:

- ``vertexproject/pydebug:3.6.3-slim``
- ``vertexproject/pydebug:3.6-slim``

These can be used as a drop in replacement for the ``python:3.6-slim`` or ``python:3.6.3-slim`` docker images.

Using the image
---------------

The images can be run with docker-compose or docker run.  You must add the ``SYS_PTRACE`` capability to the container.
Using ``docker run`` this can be done by adding the ``--cap-add=SYS_PTRACE`` command line argument.  For docker-compose,
the following section must be added to a docker-compose.yml file:

::

    cap_add:
      - SYS_PTRACE

Once the image is running, the running container can be attached too with ``docker exec``. Once a his is attached, you
can use ``gdb -p 1`` to attach to the running process. An example of this is seen below:

::

    # Starting the example docker-compose file
    debug_python$ docker-compose up -d --force-recreate
    Recreating debugpython_pydebug_1

    # Attaching to the running container
    debug_python$ docker exec -it --privileged debugpython_pydebug_1 bash

    # Firing up gdb
    root@computer:/# gdb -p 1
    GNU gdb (Debian 7.7.1+dfsg-5) 7.7.1
    Copyright (C) 2014 Free Software Foundation, Inc.
    License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
    and "show warranty" for details.
    This GDB was configured as "x86_64-linux-gnu".
    Type "show configuration" for configuration details.
    For bug reporting instructions, please see:
    <http://www.gnu.org/software/gdb/bugs/>.
    Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.
    For help, type "help".
    Type "apropos word" to search for commands related to "word".
    Attaching to process 1
    Reading symbols from /usr/local/bin/python3.6...done.
    Reading symbols from /usr/local/lib/libpython3.6dm.so.1.0...done.
    Loaded symbols for /usr/local/lib/libpython3.6dm.so.1.0
    Reading symbols from /lib/x86_64-linux-gnu/libpthread.so.0...(no debugging symbols found)...done.
    [Thread debugging using libthread_db enabled]
    Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
    Loaded symbols for /lib/x86_64-linux-gnu/libpthread.so.0
    Reading symbols from /lib/x86_64-linux-gnu/libdl.so.2...(no debugging symbols found)...done.
    Loaded symbols for /lib/x86_64-linux-gnu/libdl.so.2
    Reading symbols from /lib/x86_64-linux-gnu/libutil.so.1...(no debugging symbols found)...done.
    Loaded symbols for /lib/x86_64-linux-gnu/libutil.so.1
    Reading symbols from /lib/x86_64-linux-gnu/libm.so.6...(no debugging symbols found)...done.
    Loaded symbols for /lib/x86_64-linux-gnu/libm.so.6
    Reading symbols from /lib/x86_64-linux-gnu/libc.so.6...(no debugging symbols found)...done.
    Loaded symbols for /lib/x86_64-linux-gnu/libc.so.6
    Reading symbols from /lib64/ld-linux-x86-64.so.2...(no debugging symbols found)...done.
    Loaded symbols for /lib64/ld-linux-x86-64.so.2
    Reading symbols from /usr/local/lib/python3.6/lib-dynload/_heapq.cpython-36dm-x86_64-linux-gnu.so...done.
    Loaded symbols for /usr/local/lib/python3.6/lib-dynload/_heapq.cpython-36dm-x86_64-linux-gnu.so
    0x00007fe81984c873 in select () from /lib/x86_64-linux-gnu/libc.so.6

    # Seeing the python stack trace
    (gdb) py-bt
    Traceback (most recent call first):
      <built-in method sleep of module object at remote 0x7fe8192283d8>
      File "/scripts/stall.py", line 23, in foo
        time.sleep(1)
      File "/scripts/stall.py", line 14, in haha
        foo(arg2)
      File "/scripts/stall.py", line 10, in hehe
        haha(arg1)
      File "/scripts/stall.py", line 27, in <module>
        hehe(v1)
      <built-in method exec of module object at remote 0x7fe819734cd8>
      File "/usr/local/lib/python3.6/runpy.py", line 85, in _run_code
        exec(code, run_globals)
      File "/usr/local/lib/python3.6/runpy.py", line 193, in _run_module_as_main
        "__main__", mod_spec)

    # Seeing the locals for the current stack
    (gdb) py-locals
    Unable to read information on python frame

    # Opps - we're in a C function so we have to go up to the python frame instead
    (gdb) py-up
    #6 Frame 0xffa738, for file /scripts/stall.py, line 23, in foo (arg3=100000, ifloat=<float at remote 0x7fe8193ceee0>, jstr='100000.0', c=298, i=297)
        time.sleep(1)

    # Now we can see the locals!
    (gdb) py-locals
    arg3 = 100000
    ifloat = <float at remote 0x7fe8193ceee0>
    jstr = '100000.0'
    c = 298
    i = 297

