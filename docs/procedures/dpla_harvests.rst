==========================
Quarterly Harvests to DPLA
==========================

Four times a year, metadata from our Repox instance is harvested by DPLA. The status of these ingests are tracked in
the `DPLA wiki <https://digitalpubliclibraryofamerica.atlassian.net/wiki/spaces/CT/pages/85920546/Digital+Library+of+Tennessee+Dashboard>`_.

================================
Check and Harvest Before Ingests
================================

Before each ingest, we minimally should test every set and transform that was touched prior to the last harvest. The
easiest way to do this is to use DLTN `check and harvest <https://github.com/digitallibraryoftennessee/check_and_harvest>`_
against the MODS metadata prefix in Repox.  With check and harvest, you can test an entire provider or go set by set.
Check and harvest will only test whether every record has a title, a data provider, a rights statement, a thubnail, and
a link to the object. Therefore, there can still be other problems.

=====================================================
Additional Checking with DLTN Metadata QA and variety
=====================================================

An easy way to look for other problems is to harvest a set into DLTN metadata QA and look at the output in variety.  If
odd namespaces or weird output exists, it's possible to catch some things here.

=======================
Unit Tests in DLTN XSLT
=======================

We try to add unit tests for every provider and transform in DLTN XSLT.  These unit tests should test whether the first
OAI PMH response of a given transform results in a valid well formed document.  They don't test for bad data in random
nodes.

