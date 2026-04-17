.. _nvflare_connect:

***************
Running NVFlare
***************

Before you can connect to the NVFlare server, you will need to have a deployed campaign. For information on how to create and deploy a campaign, please see the NVFlare
:ref:`nvflare_overview` page. Each deployed campaign will create downloadable startup files for campaign admininistrators and participants with the naming convention `<Project_ID>.zip`.
To download the startup files, navigate to the :ref:`campaigns` page and press "Download" in the `Projects Participating` subsection of this page. The following sections
of this page will walk you through how to move these files to an accessible location of Frontier and how to use the files to connect to the NVFlare server.

NVFlare Setup
-------------

The startup files will be downloaded locally so you will need to transfer the files to either a location on Orion.
This can easily be done by using :ref:`Globus <globus_transfer>` or command line utilies like `rsync`. For example:

.. code::

    rsync -avz ~/Downloads/<Project_ID>.zip <username>@frontier.olcf.ornl.gov:/lustre/orion/proj-shared/<Project_ID>

Once the files are accessible to Frontier, you can follow the below steps to install the NVFlare environment and prepare the NVFlare files. We
will use the ``hello-numpy-sag`` example from the `NVFlare repository <https://github.com/nvidia/nvflare>`_ to demonstrate how to use NVFlare on Frontier.

.. code::

    # Create NVFlare environment

    module load miniforge3

    conda create -n nvflare_env python=3.11 # Python version must be 3.8-3.12
    source activate nvflare_env

    pip install nvflare==2.6.2

.. code::

    # Replace the project id and hash values with your NVFlare campaign details.

    PROJ=<project_id> # e.g., ABC123
    proj=${PROJ,,}    # force lowercase, don't touch.


    unzip ${PROJ}.zip
    CAMPAIGN_FILE=$(find . -maxdepth 1 -type d -name "$proj-nvflare-*")

    if [[ -z "$CAMPAIGN_FILE" ]]; then
        echo "$CAMAIGN_FILE could not be unzipped. Please check."
        exit 1
    fi

    # Unzip reqs
    mkdir ${CAMPAIGN_FILE}/${PROJ}_Admin/local
    mkdir ${CAMPAIGN_FILE}/${PROJ}_Admin/transfer

    # Grab example code
    if [[ ! -d "NVFlare" ]]; then
        git clone --branch=2.3 https://github.com/NVIDIA/NVFlare.git
    fi

    # The files in the 'transfer' folder will be upload to the NVFlare server
    cp -r NVFlare/examples/hello-world/hello-numpy-sag ${CAMPAIGN_FILE}/${PROJ}_Admin/transfer/

    # Set permissions
    chmod u+x ${CAMPAIGN_FILE}/${PROJ}_Admin/startup/fl_admin.sh
    chmod u+x ${CAMPAIGN_FILE}/${PROJ}/startup/start.sh
    chmod u+x ${CAMPAIGN_FILE}/${PROJ}/startup/sub_start.sh

Administrator Setup
-------------------

To initialize the NVFlare service, administrators should aquire compute resources either through an interactive job or a reservation. Next,
activate your NVFlare environment and navigate to the ``<Project_ID>-nvflare-<hash>/<Project_ID>_Admin/startup`` folder. Finally, run the
`fl_admin.sh` file and enter the username ``<Project_ID>_Admin`` where you replace `<Project_ID>` with the actual project's id (e.g., User name: ABC123_Admin).

.. code::

    # From a compute node
    
    module load miniforge3
    source activate nvflare_env

    cd ${CAMPAIGN_FILE}/${PROJ}_Admin/startup/
    ./fl_admin.sh

    # When prompted, enter <Project_ID>_Admin as the username.

Once the NVFlare campaign is initialized, you can check the administrative commands available to you with ``?``. To launch the example
``hello-numpy-sag`` job, and check the status of your job, the server, and clients you can run the following commands:

.. code::
    
    # Replace "server" with client to check client status 
    check_status server 
   
    # Run the job from the 'transfer' folder
    submit_job hello-numpy-sag/jobs/hello-numpy-sag

    # List the status of queued/running jobs
    list_jobs 

.. note::
    If you're testing the ``hello-numpy-sag`` example, you may need to change the "min_clients" parameter in the `meta.json` and `config_fed_server.json`
    files to 1 in order for the jobs to run using a single client.

Client Setup
------------

If you're a client you can start the client service by navigating to the ``startup`` directory and executing the ``start.sh`` script. Once
started, the admin should be available to the administrator to interact with.

.. code::

    # From a compute node

    module load miniforge3
    source activate nvflare_env

    cd cd ${CAMPAIGN_FILE}/${PROJ}/startup/
    ./start.sh 




