*************************************************************************************
Apache Spark
*************************************************************************************

Overview
========

`Apache Spark <https://spark.apache.org/>`_ is a multi-language engine for executing data engineering, data science, and machine learning on single-node machines or clusters.
In this document we provide instructions to run multi-node Spark cluster on ``Andes`` system and show an example of pyspark job.


Getting Started
===============

Download Spark from the `Apache Spark download page <https://spark.apache.org/downloads.html>`_.
I used `Spark-3.1 <https://www.apache.org/dyn/closer.lua/spark/spark-3.1.3/spark-3.1.3-bin-hadoop3.2.tgz>`_, but it should work for newer versions as well.
``untar`` the downloaded file and rename the directory as ``spark``.


To setup a Spark cluster, we use the following Slurm script to request compute nodes.
The slurm script requests four nodes and spawns a Spark cluster having a master node and three worker nodes.
Number of worker nodes can be increased or decreased by changing the value of ``-N`` option in the Slurm script.  

.. code-block:: bash

    #!/bin/bash
    #SBATCH --mem=0
    #SBATCH -A <ABC1234>
    #SBATCH -t 1:00:00
    #SBATCH -N 4
    #SBATCH -J spark_test
    #SBATCH -o o.spark_test
    #SBATCH -e e.spark_test

    module load spark
    module load python

    nodes=($(scontrol show hostnames ${SLURM_JOB_NODELIST} | sort | uniq ))
    numnodes=${#nodes[@]}
    last=$(( $numnodes - 1 ))
    export SCRATCH=<SCRATCH_DIRECTORY>
    export SPARK_HOME=<PATH/WHERE/SPARK/DIRECTORY/IS>/spark
    master=${nodes[0]}
    masterurl="spark://${master}.olcf.ornl.gov:7077"
    ssh ${nodes[0]} "cd ${SPARK_HOME}; source /etc/profile ; module load spark; ./sbin/start-master.sh"
    for i in $( seq 1 $last )
    do
        ssh ${nodes[$i]} "cd ${SPARK_HOME}; source /etc/profile ; module load spark; ./sbin/start-worker.sh ${masterurl}"
    done

    ssh ${nodes[0]} "cd ${SPARK_HOME}; source /etc/profile ; module load spark; /usr/bin/time -v ./bin/spark-submit --deploy-mode client --executor-cores 32 --executor-memory 250G --conf spark.standalone.submit.waitAppCompletion=true --master $masterurl spark_test.py"
    wait
    echo 'end'
    exit


The Slurm script submits a test python script (``spark_test.py``) described below. This script runs a pyspark code to test the Spark cluster.
Copy the content below and save it as a ``spark_test.py`` file in the ``SPARK_HOME`` directory.
You can also change the ``spark_test.py`` file's path, but you will have to update the Slurm script appropriately.


.. code-block:: bash

    #spark_test.py
    import random
    from pyspark.sql import SparkSession
    import pyspark.sql.functions as F


    spark = SparkSession.builder.appName('Test-app').getOrCreate()

    #Generate sample dataset
    cola_list = ['2022-01-01', '2022-01-02', '2022-01-03' ]
    colb_list = ['CSC', 'PHY', 'MAT', 'ENG', 'CHE', 'ENV', 'BIO', 'PHRM']
    colc_list = [100, 200, 300, 400, 500, 600, 700, 800, 900]


    # declaring a random.seed value to generate same data in every run
    random.seed(1)
    sample_data = []
    for idx in range(1000):
        sample_data.append([random.choice(cola_list), random.choice(colb_list), random.choice(colc_list)])

    columns= ["date", "org", "value"]
    #creating a Spark dataframe
    df = spark.createDataFrame(data = sample_data, schema = columns)

    res = (df.groupBy('date','org')
           .agg(F.count('value').alias('count_value')))
    res.show()


If the spark cluster is setup and the ``spark-test.py`` executes successfully, the output in the log file ``o.spark_test``
should look similar to the table below.



.. code-block:: bash

  +----------+----+-----------+
  |      date| org|count_value|
  +----------+----+-----------+
  |2022-01-03| BIO|         37|
  |2022-01-02| ENV|         53|
  |2022-01-03| CHE|         39|
  |2022-01-03| PHY|         46|
  |2022-01-01| CSC|         45|
  |2022-01-03| CSC|         48|
  |2022-01-01| BIO|         39|
  |2022-01-01| MAT|         42|
  |2022-01-02| CHE|         44|
  |2022-01-03| ENV|         33|
  |2022-01-01| ENG|         33|
  |2022-01-02| ENG|         28|
  |2022-01-01| ENV|         33|
  |2022-01-02| CSC|         45|
  |2022-01-02| MAT|         51|
  |2022-01-01| PHY|         38|
  |2022-01-01|PHRM|         40|
  |2022-01-03|PHRM|         42|
  |2022-01-02|PHRM|         43|
  |2022-01-03| ENG|         56|
  +----------+----+-----------+
  only showing top 20 rows


Spark also provides a web UI to monitor cluster, and you can access it on your local machine by port forwarding the master node to local machine.


- For example, if master node is running on ``andes338``, you can run the following code on your local machine terminal.

  ``ssh -N <USERNAME>@andes-login1.olcf.ornl.gov -L 8080:andes338.olcf.ornl.gov:8080``

- Then access the Spark dashboard using address ``http://localhost:8080/`` on a web browser on your local machine.




.. note::
    The `spark documentation <https://spark.apache.org/docs/latest/>`_ is very useful tool, go through it to find the Spark capabilities.
