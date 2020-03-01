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

Step One: Run Check and Harvest
===============================

When a new harvest is requested, you should always start by running `check and harvest <https://github.com/DigitalLibraryofTennessee/check_and_harvest>`_
versus the incoming metadata format.  This will ensure that we don't accidentally add any records that are missing any
required fields.

If there are no bad records, the set can be added as is to Repox via OAI-PMH.  If there are any bad records, they must
be fixed by the partner or we must harvest the good records with `check and harvest <https://github.com/DigitalLibraryofTennessee/check_and_harvest>`_.

See the `Check and Harvest Instructions <https://dltn-technical-docs.readthedocs.io/en/latest/tools/check_and_harvest.html>`_
for more information.

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

All new sets should be accompanied by an automated test.  These tests help ensure that we don't accidentally break
an existing transform when applying it to a new set with modifications.

Automated tests are built around `shunit2 <https://github.com/kward/shunit2>`_, a xUnit based unit test framework for
Bourne based shell scripts. Automated tests are kept in the `tests directory in DLTN_XSLT <https://github.com/DigitalLibraryofTennessee/DLTN_XSLT/tree/master/tests>`_.
Each test should be defined in the validate_scenarios.sh script.  For transforms that apply to multiple sets, the set
can simply be added to the `corresponding text file <https://github.com/DigitalLibraryofTennessee/DLTN_XSLT/tree/master/tests/test_data>`_.

Step Six: Generate IIIF Catalogs for ContentDM Providers
========================================================

We generate IIIF manifest catalogs for all ContentDM providers.  This allows us to map the manifests to our outgoing
metadata so that DPLA can use the manifest to generate larger size thumbnails and have a higher quality image of the
object in the DPLA interface.  This makes the object rank higher in Google results because the size of the image helps
determine rank in the search engine.

To generate the catalog files, use `ContentDM Catalog Manifest Generator <https://github.com/DigitalLibraryofTennessee/contentdm_catalog_manifest_generator>`_.
Then add the catalog to `DLTN XSLT <https://github.com/DigitalLibraryofTennessee/DLTN_XSLT>`_ and open a pull request.

Step Seven: Add Set to Repox
============================

To add a set to Repox, you can:

1. Login to `Repox <https://dpla.lib.utk.edu/repox>`_ and define the new set under the provider.
2. Add the set to the command line with `pyrepox <https://github.com/markpbaggett/pyrepox>`_.

You'll need to associate the corresponding transform with the set.  This has to be done in the GUI initially if the set
is new.

Step Eight: Update Catalogs and Transform in Repox
==================================================

To update catalogs and transforms, clone the `DLTN XSLT <https://github.com/digitailibraryoftennessee/dltn_xslt`_
repository and copy the contents to dpla:/vhosts/repoxdata/configuration/xslt.

**Note**: you should always touch all files in that directory to ensure Repox sees the updated transform.

Step Nine: Run Check and Harvest versus Final MODS
==================================================

Before we are send things to DPLA, always run check and harvest versus the final MODS of any new or modified sets.

Step Ten: Add Set to Ingestion3 Configuration
=============================================

Once testing is done, add the set to sets.yml in the `config repo <https://github.com/DigitalLibraryofTennessee/dltn_ingestion3_config_generator>`_.

----------------------------
Reharvesting an Existing Set
----------------------------

Step One: Run Check and Harvest
===============================

------------------------------
Sharing New Metadata with DPLA
------------------------------

----------------------------
Generating Quarterly Reports
----------------------------

To generate reports, a few things need to happen. In the DLTN XSLT tracker, each issue completed during the quarter
should have:

1. an associated milestone
2. an associated assignee
3. be closed

Then, quarterly reports can be generated by running issue_reports.py in
`dltn technical docs <https://github.com/DigitalLibraryofTennessee/dltn_docs_generator>`_.


