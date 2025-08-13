.. _constellation_preparing_data:

*****************************
Preparing and Submitting Data
*****************************

Preparing Your Dataset
----------------------

All data shared in Constellation should be identified by the depositor as appropriate for open public sharing. Preparing data for publication is a critical step in ensuring your research is FAIR – findable, accessible, interoperable, and reusable by the wider scientific community. Data for publication should be organized systematically.

- Create clear and descriptive directory structures and file names and maintain consistent formatting.
- Include supplementary information such as data dictionaries that define variables and provide necessary context for interpretation and reuse.
- Consider the ethical implications of data sharing, ensuring that sensitive information is anonymized when necessary.
- Blank or missing data values should be handled consistently across data files.
- If applicable, adhere to relevant data standards or formats specific to your field/domain, which will facilitate easier comparison and integration with other datasets.
- Copyrighted material may not be reshared through Constellation.

Users should acknowledge the OLCF in all publications and presentations that speak to work performed on OLCF resources. The appropriate acknowledgement statement can be found at: `<https://www.olcf.ornl.gov/about-olcf/media-assets/>`_.

Data Review and Release
-----------------------

Constellation is a separate service from institutional publication management systems such as RESolution. Data depositors are responsible for following all appropriate data review and release policies of DOE and other funding institutions. Staff members of Oak Ridge National Laboratory should follow relevant SBMS procedures to Review and Release Scientific and Technical Information. Constellation staff may request confirmation that a dataset has been submitted to RESolution and approved by lab Releasing Officials prior to publication. Draft DOIs reserved in Constellation can be used in the dataset submission workflow in RESolution.

Reserving a Draft DOI
---------------------

To get started with a new data publication, reserve a DOI for your dataset by clicking on the "Reserve new DOI" button in your user dashboard. Enter a draft title for your dataset. Select whether the data you are submitting was created using resources of the Oak Ridge Leadership Computing Facility (OLCF). OLCF resources include Frontier, Summit, Slate (Onyx, Marble). Click “Save”. Your dataset and reserved DOI will now be visible in your dashboard under "Draft Datasets."

In your user dashboard, find your dataset in the "Draft Datasets" table and click the "add" button under "Metadata." This will open a form that enables entry of metadata associated with the new DOI. When all required fields are complete, click the “Save” button to save the DOI request as a draft. If any required field is omitted, you will see a “Data Entry Error” alert indicating the error. To resolve the issue, enter the missing information in the form and click the "Save" button again.

Removal of Dataset Drafts
-------------------------

To ensure sustainability of technological and storage resources, Constellation staff will contact a depositor if a dataset is in the draft state for more than six months to ascertain its status. A good faith effort to contact the depositor and/or the project PI via email will be made prior to deletion. If a depositor does not respond, Constellation staff retain the right to delete datasets that have remained in draft state in Constellation for more than 12 months.

Adding Data and Documentation
-----------------------------

In the “Draft Datasets” table, click the “Upload” link in the “Add Files” column. This link will direct you to your assigned directory in the OLCF DOI-UPLOADS collection in the Globus web interface.

You have the option to transfer files from another Globus collection, such as an OLCF storage system, or to upload files directly from your local machine. If you need to add data files larger than 1 GB from your laptop or desktop, you will need to install Globus Connect Personal. This tool allows you to create your own Globus endpoint, facilitating uploads for large datasets. Globus Connect Personal installations for your operating system can be found at `https://www.globus.org/globus-connect-personal <https://www.globus.org/globus-connect-personal>`_.

Include essential documentation, such as a README file, data dictionary, or other relevant dataset information, in the same directory as your data files. At minimum, a README file is recommended for inclusion with all data deposits. README files provide additional context and citation information for your dataset and should help future researchers understand and reuse your data. Download Constellation’s standard README template at `https://doi.ccs.ornl.gov/data-depositor-guide <https://doi.ccs.ornl.gov/data-depositor-guide>`_.

Once your metadata is complete and all data files are uploaded, send your dataset for curator review and publication. Return to your Constellation dashboard and open the metadata form. Change the dropdown status at the bottom of the page to "Needs Approval" and click "Save."

Review States
-------------

When your dataset has been successfully submitted for approval, it will appear in the dashboard table “My Datasets Under Review.” Datasets are typically reviewed within 2-4 business days of submission. Curation may take longer depending on the size and complexity of the dataset. A curator will contact you by email with any questions or to share findings and request additional data files and documentation. If you have not been contacted after 7 business days, reach out to doi_support@ornl.gov.

When your DOI moves to the “My Approved Datasets” table, it indicates that all reviews are complete and the data files are being moved to archive storage. When the transfer is complete, a curator will mark the dataset published and you will see the DOI in the “My Published Datasets” table. A request is sent to OSTI to activate the draft DOI and add the metadata record to the DOE Data Explorer. DOIs can take 6-24 hours to become active and point to the metadata landing page. Once all publication steps are complete and the data is publicly available, you will receive a confirmation email from Constellation staff.

Data Curation
-------------

Data curation ensures compliance with repository and funder requirements and helps researchers adhere to the FAIR data principles. Curation for Constellation datasets may involve reviewing data for PII or other protected information, confirming that all files are present and accessible, generating and cleaning metadata, implementing file and directory naming schemes, suggesting or creating supplementary documentation, and reviewing and testing included code. Implementing curator recommendations can make data more impactful, reusable, and valuable to science over the long term.

All data shared in Constellation should be identified by the depositor as appropriate for public sharing (see the Data Depositor Agreement). Curators may request additional reviews by the IRB, legal office, and privacy specialists. Datasets that are identified as containing PII, CUI, UCNI, or information in a controlled subject area may be rejected.

Constellation curators are not scientific domain specialists and will not provide peer review of data or otherwise confirm the accuracy of outputs and analysis.
