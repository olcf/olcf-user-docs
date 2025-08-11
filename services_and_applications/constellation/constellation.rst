.. _constellation_overview:

**************************
Overview
**************************

OLCF Constellation
------------------

OLCF provides Constellation, a data repository and DOI service for open scientific research data. Constellation enables users to share, browse, search, and download datasets associated with research projects conducted within or in collaboration with OLCF and Oak Ridge National Laboratory (ORNL). Constellation helps researchers comply with DOE public sharing requirements including the DOE Public Access Plan and DOE O 241.1C. Data submissions may be from any scientific domain and are carefully reviewed before being made available to the general public.

Constellation is suitable for datasets of all sizes, ranging from a couple of megabytes up to petabyte-scale publications. Archival storage and access are provided for a period of up to ten years before a review is conducted for continued retention and preservation.

Each dataset published via Constellation is assigned a Digital Object Identifier (DOI). A DOI is a unique and persistent alphanumeric identifier used to identify and resolve digital "objects" such as articles, reports, and datasets. Constellation obtains and activates DataCite DOIs through membership in the DOE Office of Scientific and Technical Information’s (OSTI) Data ID Service.

For scientific researchers, obtaining DOIs for their datasets is crucial as this facilitates proper citation and enhances the discoverability of their work in the scientific community. By providing a stable link to the data, a DOI allows other researchers to easily find, cite, and build upon the published datasets, promoting transparency, reproducibility, and collaboration. DOIs can also help researchers track the impact and usage of their data over time, increasing the visibility and credibility of their research contributions.

Constellation Infrastructure
----------------------------

Constellation leverages OLCF infrastructure for secure management of large datasets. Globus is used for data access and transfer. Draft datasets are uploaded to the Orion parallel filesystem in the Moderate security enclave via the OLCF DOI-UPLOADS Globus collection. After review and approval for publication, data are migrated to Themis, an IBM Spectrum Archive storage system in the Open security enclave. Data on Themis is open to the public, but users must register for a Globus account to download files.

To the extent reasonable, Constellation will endeavor to provide access to deposited data for a minimum period of 10 years. Constellation will attempt to maintain data and supporting files in the forms they were originally submitted. In some cases, Constellation may maintain the content, structure and/or functionality of the files through format migration or other appropriate strategies. Constellation will also strive to provide basic services which may include backup, obsolescence management, and periodic refreshment by copying the data to new storage media.

Authentication and Account Setup
---------------------------------

OLCF Moderate and Open users, as well as ORNL staff and students, can create a Constellation account to reserve DOIs and publish data. Visit `doi.ccs.ornl.gov` and authenticate using an OLCF username and passcode (PIN + RSA SecurID TOKENCODE) or ORNL UCAMS/XCAMS three-character username and passphrase. The first time a user logs in they will be asked to enter a Globus user identity, and to accept a User Agreement describing Constellation’s terms of use.

To use an existing Globus identity, go to `https://www.globus.org/get-started` and click 'Log In.' Most non-profit organizations including DOE national labs offer log in using institutional credentials. After logging in, your Globus identity can be found under Settings > Account > Identity. Your primary identity may be in the form of an email address or a 36-character UUID. Either value may be used with Constellation.

If institutional log in is not available for Globus, obtain a personal Globus ID. Navigate to `https://globusid.org/create` and complete the registration form. You will be asked to verify your email address. Once you confirm your email address, you can find your Globus ID by going to Settings > Account > Identity. Your primary identity is the first field displayed next to a crown icon and may be in the form of an email address or [globus_username]@globusid.org.

.. image:: example_screenshot.png
   :alt: Screenshot of Globus identities

After logging in to Constellation, you will be taken to your account dashboard.

Preparing & Submitting Data
----------------------------

Preparing Your Dataset
~~~~~~~~~~~~~~~~~~~~~~~

All data shared in Constellation should be identified by the depositor as appropriate for open public sharing. Preparing data for publication is a critical step in ensuring your research is FAIR – findable, accessible, interoperable, and reusable by the wider scientific community. Data for publication should be organized systematically.

- Create clear and descriptive directory structures and file names and maintain consistent formatting.
- Include supplementary information such as data dictionaries that define variables and provide necessary context for interpretation and reuse.
- Consider the ethical implications of data sharing, ensuring that sensitive information is anonymized when necessary.
- Blank or missing data values should be handled consistently across data files.
- If applicable, adhere to relevant data standards or formats specific to your field/domain, which will facilitate easier comparison and integration with other datasets.
- Copyrighted material may not be reshared through Constellation.

Users should acknowledge the OLCF in all publications and presentations that speak to work performed on OLCF resources. The appropriate acknowledgement statement can be found at: `https://www.olcf.ornl.gov/about-olcf/media-assets/`.

Data Review and Release
~~~~~~~~~~~~~~~~~~~~~~~

Constellation is a separate service from institutional publication management systems such as RESolution. Data depositors are responsible for following all appropriate data review and release policies of DOE and other funding institutions. Staff members of Oak Ridge National Laboratory should follow relevant SBMS procedures to Review and Release Scientific and Technical Information. Constellation staff may request confirmation that a dataset has been submitted to RESolution and approved by lab Releasing Officials prior to publication. Draft DOIs reserved in Constellation can be used in the dataset submission workflow in RESolution.

Reserving a Draft DOI
~~~~~~~~~~~~~~~~~~~~~

To get started with a new data publication, reserve a DOI for your dataset by clicking on the "Reserve new DOI" button in your user dashboard. Enter a draft title for your dataset. Select whether the data you are submitting was created using resources of the Oak Ridge Leadership Computing Facility (OLCF). OLCF resources include Frontier, Summit, Slate (Onyx, Marble). Click “Save”. Your dataset and reserved DOI will now be visible in your dashboard under "Draft Datasets."

In your user dashboard, find your dataset in the "Draft Datasets" table and click the "add" button under "Metadata." This will open a form that enables entry of metadata associated with the new DOI. When all required fields are complete, click the “Save” button to save the DOI request as a draft. If any required field is omitted, you will see a “Data Entry Error” alert indicating the error. To resolve the issue, enter the missing information in the form and click the "Save" button again.

Removal of Dataset Drafts
~~~~~~~~~~~~~~~~~~~~~~~~~~

To ensure sustainability of technological and storage resources, Constellation staff will contact a depositor if a dataset is in the draft state for more than six months to ascertain its status. A good faith effort to contact the depositor and/or the project PI via email will be made prior to deletion. If a depositor does not respond, Constellation staff retain the right to delete datasets that have remained in draft state in Constellation for more than 12 months.

Adding Data and Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the “Draft Datasets” table, click the “Upload” link in the “Add Files” column. This link will direct you to your assigned directory in the OLCF DOI-UPLOADS collection in the Globus web interface.

You have the option to transfer files from another Globus collection, such as an OLCF storage system, or to upload files directly from your local machine. If you need to add data files larger than 1 GB from your laptop or desktop, you will need to install Globus Connect Personal. This tool allows you to create your own Globus endpoint, facilitating uploads for large datasets. Globus Connect Personal installations for your operating system can be found at `https://www.globus.org/globus-connect-personal`.

Include essential documentation, such as a README file, data dictionary, or other relevant dataset information, in the same directory as your data files. At minimum, a README file is recommended for inclusion with all data deposits. README files provide additional context and citation information for your dataset and should help future researchers understand and reuse your data. Download Constellation’s standard README template at `https://doi.ccs.ornl.gov/data-depositor-guide`.

Once your metadata is complete and all data files are uploaded, send your dataset for curator review and publication. Return to your Constellation dashboard and open the metadata form. Change the dropdown status at the bottom of the page to "Needs Approval" and click "Save."

Review States
~~~~~~~~~~~~~

When your dataset has been successfully submitted for approval, it will appear in the dashboard table “My Datasets Under Review.” Datasets are typically reviewed within 2-4 business days of submission. Curation may take longer depending on the size and complexity of the dataset. A curator will contact you by email with any questions or to share findings and request additional data files and documentation. If you have not been contacted after 7 business days, reach out to doi_support@ornl.gov.

When your DOI moves to the “My Approved Datasets” table, it indicates that all reviews are complete and the data files are being moved to archive storage. When the transfer is complete, a curator will mark the dataset published and you will see the DOI in the “My Published Datasets” table. A request is sent to OSTI to activate the draft DOI and add the metadata record to the DOE Data Explorer. DOIs can take 6-24 hours to become active and point to the metadata landing page. Once all publication steps are complete and the data is publicly available, you will receive a confirmation email from Constellation staff.

Data Curation
-------------

Data curation ensures compliance with repository and funder requirements and helps researchers adhere to the FAIR data principles. Curation for Constellation datasets may involve reviewing data for PII or other protected information, confirming that all files are present and accessible, generating and cleaning metadata, implementing file and directory naming schemes, suggesting or creating supplementary documentation, and reviewing and testing included code. Implementing curator recommendations can make data more impactful, reusable, and valuable to science over the long term.

All data shared in Constellation should be identified by the depositor as appropriate for public sharing (see the Data Depositor Agreement). Curators may request additional reviews by the IRB, legal office, and privacy specialists. Datasets that are identified as containing PII, CUI, UCNI, or information in a controlled subject area may be rejected.

Constellation curators are not scientific domain specialists and will not provide peer review of data or otherwise confirm the accuracy of outputs and analysis.

Reusing Constellation Data
---------------------------

Datasets published in Constellation are free to use and reuse. Datasets authored by ORNL staff have arisen under UT-Battelle, LLC’s Prime Contract No. DE-AC05-00OR22725 with the U.S. Department of Energy (DOE) to manage and operate the Oak Ridge National Laboratory. UT-Battelle, LLC will not assert any rights under United States law or under the Prime Contract it has in the dataset against any user of the dataset, including any copyrights or patent rights. UT-Battelle, LLC requests that attribution to the dataset is provided as academically appropriate.

Datasets published by affiliates of non-ORNL institutions may provide alternative open use licenses for their data. Attribution should be included in any resulting publications as academically appropriate. For additional questions on data use and reuse, Constellation staff can refer you to the original dataset depositor.