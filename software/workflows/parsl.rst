.. _workflows-parsl:

*****
Parsl
*****


Overview
========

Parsl is a flexible and scalable parallel programming library for Python which
is being developed at the University of Chicago. It augments Python with simple
constructs for encoding parallelism. For more information about Parsl, please
refer to its `documentation <https://parsl-project.org/>`_.


Prerequisites
=============

Parsl can be installed with Conda for use on Summit by running the following
from a login node:

.. code-block:: console

    $ module load workflows
    $ module load parsl/1.1.0


Hello world!
============

The following instructions illustrate how to run a "Hello world" program with
Parsl on Summit.

Parsl needs to be able to write to the working directory from compute nodes,
so we will work from within the member work directory and assume a project ID
``ABC123``:

.. code-block:: console

    $ mkdir -p ${MEMBERWORK}/abc123/parsl-demo/
    $ cd ${MEMBERWORK}/abc123/parsl-demo/


To run an example "Hello world" program with Parsl on Summit, create a
file called ``hello-parsl.py`` with the following contents, but with your own
project ID in the line specified:

.. code-block:: python

    from parsl.addresses import address_by_interface
    from parsl.config import Config
    from parsl.executors import HighThroughputExecutor
    from parsl.launchers import JsrunLauncher
    from parsl.providers import LSFProvider

    from parsl import python_app

    import parsl

    parsl.set_stream_logger()

    config = Config(
        executors = [
            HighThroughputExecutor(
                label = 'Summit_HTEX',
                address = address_by_interface('ib0'),
                worker_port_range = (50000, 55000),
                provider = LSFProvider(
                    launcher = JsrunLauncher(),
                    walltime = '00:10:00',
                    nodes_per_block = 1,
                    init_blocks = 1,
                    max_blocks = 1,
                    worker_init = 'source activate parsl-py36',
                    project = 'abc123', # replace this line
                    cmd_timeout = 30
                )
            )
        ]
    )

    @python_app
    def hello ():
        import platform
        return 'Hello from {}'.format(platform.uname())

    parsl.load(config)
    print(hello().result())
    parsl.clear()


Now, run the program from a shell or script:

.. code-block:: console

    $ python3 hello-parsl.py


There will be a flood of output to ``stdout``, but the lines that indicate
successful execution will look something like the following:

.. code-block::

    2021-06-28 16:10:46 parsl.dataflow.dflow:431 [INFO]  Task 0 completed (launched -> exec_done)
    Hello from uname_result(system='Linux', node='a01n14', release='4.14.0-115.21.2.el7a.ppc64le', version='#1 SMP Thu May 7 22:22:31 UTC 2020', machine='ppc64le', processor='ppc64le')


Congratulations! You have now run a Parsl job on Summit.


