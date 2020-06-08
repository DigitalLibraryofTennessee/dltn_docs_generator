===========================
Generating Provider Reports
===========================

This section describes how to generate provider reports and things to know regarding this process.

Individual provider reports are generated based on data from:

* Repox with `pyrepox <https://github.com/markpbaggett/pyrepox>`_
* `The DLTN MODS OAI Feed <https://dpla.lib.utk.edu/repox/OAIHandler?verb=ListRecords&metadataPrefix=MODS>`_

**Before you generate:** If you just want to update an `email address`, `description`, or `oai_endpoint` for a provider,
don't need to generate a whole new report.  Instead:

1. update the information against the **Repox API** (you can do this with pyrepox)
2. edit the corresponding rst directly.

Doing this is much faster!  Just make sure you update the value in Repox and not just in the rst file.

------------------
Generating Reports
------------------

1. Fill out your `config file`.
2. If you want MODS count to be correct, make sure that value is set to True (even though it takes a lot longer.)
3. To generate for all providers, just run `python generate.py`
4. To generate a report for a specific provider, use the p flag with the Repox provider_id:  `python generate.py -p memphispublicr0`
