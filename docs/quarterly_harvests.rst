=================================
Procedures for Quarterly Harvests
=================================

----------------------------------
Adding and Reviewing GitHub Issues
----------------------------------

Procedures for DPLA Quarterly Harvests are based around the `DLTN XSLT Issue Tracker <https://github.com/digitallibraryoftennessee/dltn_Xslt/issues>`_.
Individual tasks should be added to the issue tracker by either the aggregation staff or a representative of the partner
library.

When reviewing tasks, the aggregation staff should assign a milestone and a label.

When a task is being work on, an aggregation staff member should self assign it.

The issue should remain open until all related parts are completed.

----------------
Adding a New Set
----------------

Step One: Running Check and Harvest
===================================

When a new harvest is requested, you should always start by running `check and harvest <https://github.com/DigitalLibraryofTennessee/check_and_harvest>`_
versus the incoming metadata format.  This will ensure that we don't accidentally add any records that are missing any
required fields.

If there are no bad records, the set can be added as is to Repox via OAI-PMH.  If there are any bad records, they must
be fixed by the partner or we must harvest the good records with `check and harvest <https://github.com/DigitalLibraryofTennessee/check_and_harvest>`_.

Step Two: DLTN Metadata QA and Variety
======================================

Before a metadata mapping can be written, we need to know what all the metadata practices across a set are. In order to
get a clear view of practices across an entire set, you can add the set with `DLTN Metadata QA <https://github.com/markpbaggett/dltn_metadata_QA>`_
and then run `variety.js <https://github.com/variety/variety>`_ against that set.

Step Three: Write Metadata Mapping
==================================

Based on the results of Step Two, write a metadata mapping that explains which fields should be mapped and to which field
in our outgoing MODS.  The final metadata mapping should be added to the `metadata mappings <https://dltn-technical-docs.readthedocs.io/en/latest/#metadata-mappings>`_
section of DLTN technical documentation.

Step Four: Determine Transform
==============================

If possible, reuse an existing transform in `DLTN XSLT <https://github.com/DigitalLibraryofTennessee/DLTN_XSLT/tree/master/XSLT>`_.
If small changes need to be made, make them and open a pull request.

If its easier to write a new transform, do it and open a pull request.

Step Five: Add Automated Test
=============================

Step Six: Generate IIIF Catalogs
================================

Step Seven: Add Set to Repox
============================

Step Eight: Update Catalogs and Transform in Repox
==================================================

Step Nine: Run Check and Harvest versus Final MODS
==================================================

Step Ten: Add Set to Ingestion3 Configuration
=============================================


----------------------------
Reharvesting an Existing Set
----------------------------



