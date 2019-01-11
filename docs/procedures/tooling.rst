==============================
Tooling and Other Applications
==============================

Below is a master list of tools currently in use by DLTN's technical aggregation team for aggregation, remediation, and other
processes.

* `Repox <https://github.com/europeana/repox>`_: Primary Aggregation utility.
* `Pyrepox <https://github.com/markpbaggett/pyrepox>`_: Pyrepox is a python client written around the Repox API that we
  use for deployment, reporting, and other Repox specific tasks.
* `DLTN Docs Generator <https://github.com/DigitalLibraryofTennessee/dltn_docs_generator>`_: a utility that uses Pyrepox
  to generate this site.
* `ContentDM IIIF Manifest Catalog Generator <https://github.com/DigitalLibraryofTennessee/contentdm_catalog_manifest_generator>`_:
  Simple utility that we use to generate catalog.xml files of objects that have IIIF manifests that we parse with dtln_xslt.
* `DLTN XSLT <https://github.com/DigitalLibraryofTennessee/DLTN_XSLT>`_: Our master repository of metadata transforms,
  IIIF manifest catalogs, remediation templates, etc.
* `Variety.js <https://github.com/variety/variety>`_: A MongoDB schema analyzer that we use as part of metadata QA.
* `DLTN Metadata QA <https://github.com/markpbaggett/dltn_metadata_QA>`_: A terrible QA tool that was thrown together in a few days several years ago that we still use
  as part of QA work.
* `DLTN Check and Harvest <https://github.com/DigitalLibraryofTennessee/check_and_harvest>`_: A simple script we use to
  grab "good" files only from problematic sets.
