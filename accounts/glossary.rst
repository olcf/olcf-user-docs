*****************************
Glossary
*****************************

.. _glossary-closed-source:
.. glossary::
  Closed Source Software / Not Open Source Software
    Software with source code which is not publicly available for general
    distribution. For this type of software, the :ref:`Export Control
    Classification Number<glossary-eccn-number>` (ECCN) is requested. If the
    code is subject to a different export control jurisdiction (e.g. Department
    of State, ITAR) please indicate an appropriate categorization.

.. _glossary-eccn-number:
.. glossary::
  Export Control Classification Number (ECCN)
    US Department of Commerce Export Control Classification Number. If an
    application software package is export controlled, list the applicable ECCN.
    This is requested for all software that is :ref:`Not Open
    Source<glossary-closed-source>`. If the code is subject to a different
    export control jurisdiction (e.g. Department of State ITAR, Nuclear
    Regulatory Commission Controls) please indicate an appropriate
    categorization.

.. _glossary-health-data:
.. glossary::
  Human Health Data
    Human Health Data is intentionally broadly defined to include any information 
    that relates to the past, present, or future physical or mental health, condition, 
    or well-being of an individual or human population—regardless of the presence of personal 
    identifiers.

    Examples include:
      - Genomic data
      - Clinical data (e.g., electronic health records)
      - Data protected by HIPAA (PHI or Limited Data Set)
      - Health surveillance data
      - Public health data
      - Information about an individual intended for use in biomedical, behavioral, clinical, or other human health-related research

.. _glossary-nsdd-189:
.. glossary::
  National Security Decision Directive (NSDD) 189
    `National Security Decision Directive (NSDD) Number 189
    <https://fas.org/irp/offdocs/nsdd/nsdd-189.htm>`_ is a federal directive
    that establishes national policy for controlling the flow of science,
    technology, and engineering information produced in federally-funded
    fundamental research at colleges, universities, and laboratories. NSDD 189
    defines "Fundamental Research" as:

        *Basic and applied research in science and engineering, the results of which
        ordinarily are published and shared broadly within the scientific community,
        as distinguished from proprietary research and from industrial development,
        design, production, and product utilization, the results of which ordinarily
        are restricted for proprietary or national security reasons.*

    "Publicly Available Information" is defined as information obtainable free
    of charge (other than minor shipping or copying fees) and without
    restriction; which is available via the internet, journal publications, text
    books, articles, newspapers, magazines, etc.

.. _glossary-open-source:
.. glossary::
  Open Source Software
    Open Source software is publicly available software (source code) which is
    available for general distribution either for free or at a price that does
    not exceed the cost of reproduction and distribution. Frequently, this Open
    Source software is distributed under a license that grants the user the
    rights to use, copy, modify, prepare derivative works, and distribute that
    software without having to make royalty payments. Such distribution may
    include original or modified source code, other formats, and any derivative
    works thereof.

.. _glossary-proprietary-data:
.. glossary::
  Proprietary Data
    Proprietary Data are data which embody trade secrets developed at private
    expense, where such data (a) are not generally known or available from other
    sources without obligation concerning their confidentiality; (b) have not
    been made available by the owner to others without obligation concerning
    their confidentiality; and (c) are not already available to the Government
    without obligation concerning their confidentiality.

.. _glossary-sensitive-information:
.. glossary::
  Sensitive or Restricted Information
    Principal Investigators are responsible for knowing whether their project
    uses or generates sensitive or restricted information. Department of Energy
    systems contain data only related to scientific research.

    Sensitive Information: This includes, but is not limited to, personally-identifiable
    information (PII). PII is information that can be used to distinguish or trace an
    individual's identity, either alone or when combined with other information
    that is linked or linkable to a specific individual.

    Restricted Information: This includes, but is not limited to, classified information,
    unclassified controlled nuclear information (UCNI), naval nuclear propulsion
    information (NNPI), the design or development of nuclear, biological, or
    chemical weapons or of any weapons of mass destruction. Use of OLCF resources to
    store, manipulate, or remotely access classified information is prohibited.

    For more information contact the DOE at:

    | Office of Domestic and International Energy Policy
    | US Department of Energy
    | Washington DC 20585

.. _glossary-classification-categories:
.. glossary::
  Project Classification Categories
    Open (Category 1)
      Definition: This category is for projects with data sets that are truly non-sensitive 
      and do not require access controls. It is suitable for data that is rightfully publicly 
      available or could be exposed to a wider audience without compromising participant’s or 
      provider’s privacy or security.
  
      Example Use: 
      Data sets that haves been completely anonymized, lacks any possible link 
      back to an individual, and are not otherwise considered sensitive or protected under HIPAA, 
      ITAR, or other law or contractual restrictions. 
     
    Moderate (Category 2)
      Definition: This category is for projects with data sets that are moderately sensitive 
      and requires moderate security measures.
  
      Example Use: 
      Data sets that require access controls due to the data owner’s “terms of use.” 
      (e.g., you or your institution was required to sign or acknowledge a Data Use Agreement that 
      requires the data set be access-restricted as a condition of using it for this project).  
     
    Enhanced (Category 3, utilizes the CITADEL security framework)
      Definition: This category is designated for the most sensitive projects, requiring enhanced 
      security and access controls. 
  
      Example Use: 
      Data that includes identifiable, sensitive, or access-controlled health information, 
      such as complete electronic health records, or data covered under strict confidentiality agreements 
      or laws that mandate high levels of protection (e.g, data protected by HIPAA).


.. _glossary-strong-scaling:
.. glossary::
  Strong Scaling
    How time-to-solution of a computation varies with the number of processors
    for a fixed *total* problem size. Use the examples below as a guide when
    providing this kind of parallel performance data.

    .. csv-table::
       :header: "nProc", "Time to Solution, Actual", "Time to Solution, Ideal"
       :widths: 10, 20, 20

       64, 9600.00, 9600.00
       128, 5333.33, 4800.00
       256, 3000.00, 2400.00
       512, 1714.29, 1200.00
       1024, 1000.00, 600.00

    .. image:: /images/accounts_glossary_strong_scaling_01.png
       :width: 470 px
       :alt: strong scaling example graph 1

    |

    .. csv-table::
       :header: "nProc", "Time to Solution, Actual", "Time to Solution, Ideal"
       :widths: 10, 20, 20

       64, 64.00, 64.00
       128, 115.20, 128.00
       256, 204.80, 256.00
       512, 358.40, 512.00
       1024, 614.40, 1024.00

    .. image:: /images/accounts_glossary_strong_scaling_02.png
       :width: 470 px
       :alt: strong scaling example graph 2

.. _glossary-weak-scaling:
.. glossary::
  Weak Scaling
    How time-to-solution of a computation varies with the number of processors
    for a fixed *per processor* problem size. Use the example below as a guide
    when providing this kind of parallel performance data.

    .. csv-table::
       :header: "nProc", "Time to Solution, Actual", "Time to Solution, Ideal"
       :widths: 10, 20, 20

       64, 10.50, 10.50
       128, 10.45, 10.50
       256, 10.42, 10.50
       512, 10.40, 10.50
       1024, 10.43, 10.50

    .. image:: /images/accounts_glossary_weak_scaling_01.png
       :width: 470 px
       :alt: weak scaling example graph


