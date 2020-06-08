===========================
Generating Provider Reports
===========================

This section describes how to generate provider reports and things to know regarding this process.

Individual provider reports are generated based on data from:

* Repox with `pyrepox <https://github.com/markpbaggett/pyrepox>`_
* `The DLTN MODS OAI Feed <https://dpla.lib.utk.edu/repox/OAIHandler?verb=ListRecords&metadataPrefix=MODS>`_

**Before you generate:** If you just want to update an `email address`, `description`, or `oai_endpoint` for a provider,
don't need to generate a whole new report.  Instead:

1. update the information against the **Repox API** (you can do this with pyrepox by following the instructions below)
2. edit the corresponding rst directly.

Doing this is much faster!  Just make sure you update the value in Repox and not just in the rst file.

------------------
Generating Reports
------------------

1. Fill out your `config file`.
2. If you want MODS count to be correct, make sure that value is set to True (even though it takes a lot longer.)
3. To generate for all providers, just run `python generate.py`
4. To generate a report for a specific provider, use the p flag with the Repox provider_id:  `python generate.py -p memphispublicr0`

-----------------------------------
Interacting with Repox with Pyrepox
-----------------------------------

If you want to update an email_address for a provider or get the identifier for a provider, you can do this with
`pyrepox <https://pypi.org/project/repox/>`_. While pyrepox does `many other things <https://pyrepox.readthedocs.io/en/latest/source/repox.html>`_
these examples are intended to help you with common tasks related to generating DLTN docs.

1. Using your preferred method, install pyrepox and enter a python interactive shell:

.. code-block:: shell
    :linenos:

    pipenv install repox
    python

2. Once you are in your interactive shell, import pyrepox and make a connection to our instance of repox.

.. code-block:: python
    :linenos:

    from repox.repox import Repox
    dltn = Repox("https://link-to-our-instance-of-repox.edu", "username", "password")

3. We're going to need our aggregator code (`TNDPLAr0`), or you can find it with:

.. code-block:: python
    :linenos:

    >>> dltn.list_all_aggregators()[0]
    'TNDPLAr0'

4. To find your provider id, use get_list_of_providers() with our aggregator id:

.. code-block:: python
    :linenos:

    >>> dltn.get_list_of_providers('TNDPLAr0')
    ['CountryMusicHallofFamer0', 'CrossroadstoFreedomr0', 'KnoxPLr0', 'memphispublicr0', 'MTSUr0', 'nashvillepublicr0', 'tslar0', 'UTKr0', 'utcr0']

5. Let's inspect a provider to see its current metadata:

.. code-block:: python
    :linenos:

    >>> dltn.get_provider('memphispublicr0')
    {'id': 'memphispublicr0', 'name': 'Memphis Public Library', 'country': 'ALBANIA', 'countryCode': 'al', 'description': 'contact: Gina Cordell platform: ContentDM', 'nameCode': 'memphispublic', 'homepage': '', 'providerType': 'LIBRARY', 'email': 'Gina.Cordell@memphistn.gov'}

6. Now, let's update the email address to be `mbagget1@utk.edu`:

.. code-block:: python
    :linenos:

    >>> dltn.update_provider('memphispublicr0', email='mbagget1@utk.edu')
    200

7. You can check your work by re-requesting the provider:

.. code-block:: python
    :linenos:

    >>> dltn.get_provider('memphispublicr0')
    {'id': 'memphispublicr0', 'name': 'Memphis Public Library', 'country': 'ALBANIA', 'countryCode': 'al', 'description': 'contact: Gina Cordell platform: ContentDM', 'nameCode': 'memphispublic', 'homepage': '', 'providerType': 'LIBRARY', 'email': 'mbagget1@utk.edu'}
