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
  Health Data
    The term Health Data is interpreted rather broadly; it includes any part of
    a patient's medical record or payment history. In particular, the US Health
    Insurance Portability and Accountability Act (HIPAA) defines Protected
    Health Information (PHI) that must be treated with great care.

    For more information on HIPAA and PHI see `Health Information Privacy
    <https://www.hhs.gov/hipaa/for-professionals/index.html>`_ from the U.S.
    Department of Health & Human Services.

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
    systems contain data only related to scientific research and do not contain
    personally identifiable information. Therefore, you should answer "Yes" if
    your project uses or generates data that falls under the Privacy Act of 1974
    U.S.C. 552a.

    Use of OLCF resources to store, manipulate, or remotely access any national
    security information is prohibited. This includes, but is not limited to,
    classified information, unclassified controlled nuclear information (UCNI),
    naval nuclear propulsion information (NNPI), the design or development of
    nuclear, biological, or chemical weapons or of any weapons of mass
    destruction. For more information contact the DOE at:

    | Office of Domestic and International Energy Policy
    | US Department of Energy
    | Washington DC 20585

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


