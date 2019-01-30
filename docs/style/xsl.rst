============
XML and XSLT
============

-----
About
-----

This style guide covers the use of both XML and XSLT.

XML
===

XML is the primary serialization format we use in DLTN for metadata exchange.  This is driven by the fact that our
workflows are primarily based around `OAI-PMH <https://www.openarchives.org/pmh/>`_.

XSLT
====

XSLT (Extensible Stylesheet Language Transformations) is the primary language we use for transforming XML documents to
`DLTN MODS <https://docs.google.com/spreadsheets/d/1BzZvDOf4fgas3TD21xF40lu2pk2XW0k2pTGJKIt6438/edit#gid=102934983>`_.
This is mainly driven by the fact that we use `Repox <https://github.com/europeana/REPOX>`_ as our aggregation platform.

**Note**:  Repox's XSL processor is built on Saxon 8.7.  Therefore, all XSLT needs to be tested verus 8.7 rather than a
the current version.

--------------------------------
Implicit vs. Explicit Processing
--------------------------------

Rule
====

For all new XSL transforms, we create XSL transforms that are implicit and based around an
`identity transform <http://www.usingxml.com/Transforms/XslIdentity>`_. A simple way to think about an identity
transform is as a generic XSL transform that copies the input XML document to the output.  Once we copy everything with
our identity transform, we create any needed templates to create the final XML that we want.

Justification
=============

When we first started our service hub, we wrote explicit transforms.  They were long, difficult to read, and
fragile.  Whenever we needed to modify a template, refactoring was expensive.

We find implicit transforms to be less verbose, easier to read, and much easier to modify and extend.

Example
=======

.. code-block:: xslt

    <?xml version="1.0" encoding="UTF-8"?>
    <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:lyncode="http://www.lyncode.com/xoai"
    xmlns="http://www.loc.gov/mods/v3" exclude-result-prefixes="#all"
    xpath-default-namespace="http://www.lyncode.com/xoai" version="2.0">

        <!-- copy all incoming metadata with an identity transform -->
        <xsl:template match="@* | node()">
            <xsl:copy>
                <xsl:apply-templates select="@* | node()"/>
            </xsl:copy>
        </xsl:template>

        <!-- Match where the incoming records start -->
        <xsl:template match="lyncode:metadata">
            <!-- Start building our MODS -->
            <mods xmlns="http://www.loc.gov/mods/v3" version="3.5" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-5.xsd">

                <!-- Serialize our title -->
                <xsl:apply-templates select="element[@name = 'dc']/element[@name = 'title']/element/field"/>

            </mods>
        </xsl:template>

        <!-- Our title template -->
        <xsl:template match="element[@name = 'dc']/element[@name = 'title']/element/field">
            <titleInfo>
                <title>
                    <xsl:apply-templates/>
                </title>
            </titleInfo>
        </xsl:template>

    </xsl:stylesheet>

-----------
Namespacing
-----------

Rule
====

Stylesheets can have default namespaces for both XML and XPATH.

xsl:param values should be namespaced to avoid collision with xpath-default-namespace.

Justification
=============

XSL is verbose.  Verbosity makes things hard to read.  Therefore, it's okay to use default namespaces for your xml and
xpaths.

This practice often causes collisions.  Therefore, namespace things like xsl:param values so that things just work
without a lot of deep thinking.

Example
=======


.. code-block:: xslt

    <?xml version="1.0" encoding="UTF-8"?>
        <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:xs="http://www.w3.org/2001/XMLSchema"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:lyncode="http://www.lyncode.com/xoai"
        xmlns:dltn = "https://github.com/digitallibraryoftennessee"
        xmlns="http://www.loc.gov/mods/v3"
        exclude-result-prefixes="#all"
        xpath-default-namespace="http://www.lyncode.com/xoai" version="2.0">

        <!-- output settings -->
        <xsl:output encoding="UTF-8" method="xml" omit-xml-declaration="yes" indent="yes"/>
        <xsl:strip-space elements="*"/>

        <!-- includes and imports -->

        <!--
        Collection/Set = Crossroads Friends and Family
        -->

        <!-- Types -->
        <xsl:param name="pType">
            <dltn:type string="moving image">Video</dltn:type>
            <dltn:type string="text">Text</dltn:type>
            <dltn:type string="sound recording">Sound</dltn:type>
        </xsl:param>

    </xsl:stylesheet>

