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

    $ module load parsl/2024.12.2


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


   ======
    import parsl
    from parsl.app.app import python_app, bash_app
    from parsl.data_provider.files import File
    import os
    from parsl.config import Config
    from parsl.channels import LocalChannel
    from parsl.providers import SlurmProvider
    from parsl.executors import HighThroughputExecutor
    from parsl.launchers import SrunLauncher
    from parsl.addresses import address_by_interface

    """ This config assumes that it is used to launch parsl tasks from the login nodes
    of Frontier at OLCF. Each job submitted to the scheduler will request 2 nodes for 10 minutes.
    """
    config = Config(
        executors=[
            HighThroughputExecutor(
                label="frontier_htex",
                address=address_by_interface('hsn0'),
                provider=SlurmProvider(
                    cmd_timeout=60,
                    channel=LocalChannel(),
                    nodes_per_block=1,
                    partition='extended',
                    scheduler_options='#SBATCH -A ABC123',   # Replace by your own allocation
                    worker_init='module load parsl/2024.12.2',
                    walltime='00:10:00',
                    launcher=SrunLauncher(),
                ),
            )
        ],
    )

    parsl.load(config)

    @python_app
    def hello ():
        import platform
        return 'Hello from {}'.format(platform.uname())

    print(hello().result())
    parsl.clear()

Now, run the program from a shell or script:

.. code-block:: console

    $ python3 hello-parsl.py


In the case of a successful execution, the output to ``stdout`` will look as follows:

.. code-block::

    Hello from uname_result(system='Linux', node='frontier10305', release='5.14.21-150500.55.49_13.0.57-cray_shasta_c', version='#1 SMP Sun May 12 13:35:37 UTC 2024 (33add2b)', machine='x86_64')

Congratulations! You have now run a Parsl job on Frontier.


