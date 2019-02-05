---------------------------------------
Reading and Writing DLTN XSL Transforms
---------------------------------------

This section is designed to help make reading and modifying our transforms as easy as possible for new people.

Header and Globals
==================

Stylesheet Attributes
---------------------

Our stylesheet attributes should look similar across the entire repository. In addition to declaring any needed namespaces,
we define a default namespace that is equal to the format of the processed document (usually MODS). This makes it so
our final documents don't have the mods namespace repeated throughout.

.. code-block:: xslt
   :emphasize-lines: 7

    <?xml version="1.0" encoding="UTF-8"?>
    <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:lyncode="http://www.lyncode.com/xoai"
    xmlns:dltn = "https://github.com/digitallibraryoftennessee"
    xmlns="http://www.loc.gov/mods/v3"
    exclude-result-prefixes="#all"
    xpath-default-namespace="http://www.lyncode.com/xoai"
    version="2.0">

We also define a xpath-default-namespace so that our selectors are less verbose.  This is normally equal to namespace of
your primary template match.

.. code-block:: xslt
   :emphasize-lines: 9

    <?xml version="1.0" encoding="UTF-8"?>
    <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:lyncode="http://www.lyncode.com/xoai"
    xmlns:dltn = "https://github.com/digitallibraryoftennessee"
    xmlns="http://www.loc.gov/mods/v3"
    exclude-result-prefixes="#all"
    xpath-default-namespace="http://www.lyncode.com/xoai"
    version="2.0">

Finally, we need to exclude all outgoing prefixes so they aren't in our outputted document.

.. code-block:: xslt
   :emphasize-lines: 8

    <?xml version="1.0" encoding="UTF-8"?>
    <xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns:lyncode="http://www.lyncode.com/xoai"
    xmlns:dltn = "https://github.com/digitallibraryoftennessee"
    xmlns="http://www.loc.gov/mods/v3"
    exclude-result-prefixes="#all"
    xpath-default-namespace="http://www.lyncode.com/xoai"
    version="2.0">

Output settings
---------------

Although not necessarily used by the Repox XSL processor, we add output settings for people who may test XML generation
from the command line.

Copy and pasting this as is is fine.

.. code-block:: xslt

    <!-- output settings -->
    <xsl:output encoding="UTF-8" method="xml" omit-xml-declaration="yes" indent="yes"/>
    <xsl:strip-space elements="*"/>


Includes and imports
--------------------

In order to be DRY, often times you will want to include or import another stylesheet.  Do that at the top of your
document

.. code-block:: xslt

    <xsl:include href="tsladctomods.xsl"/>

Text normalization
------------------

In order to be DRY, add a normalize space template at the top of your document to accompany the main identity transform.

.. code-block:: xslt

    <xsl:template match="text()">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template>

Identity transform
==================

In order to keep our transforms as simple as possible, we require that all new transforms start with an identity
transform.  This is our primary template and tells the processor to copy all text and attributes.  This template is then
accompanied by other transforms that give more explicit instructions.

.. code-block:: xslt

    <xsl:template match="text()">
        <xsl:value-of select="normalize-space(.)"/>
    </xsl:template>

Primary template match
======================

After your identity transform, add a primary template that tells the processor where your metadata records are.

.. code-block:: xslt

    <!-- match metadata -->
    <xsl:template match="lyncode:metadata">

    </xsl:template>

Inside our main template match we will start serializing our final document.

.. code-block:: xslt

    <xsl:template match="lyncode:metadata">
        <!-- match the document root and return a MODS record -->
        <mods xmlns="http://www.loc.gov/mods/v3" version="3.5"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-5.xsd">

        </mods>
    </xsl:template>

Finally, we will call other templates throughout our main template.

.. code-block:: xslt
   :emphasize-lines: 8,13,32,33

    <xsl:template match="lyncode:metadata">
        <!-- match the document root and return a MODS record -->
        <mods xmlns="http://www.loc.gov/mods/v3" version="3.5"
            xmlns:xlink="http://www.w3.org/1999/xlink"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.loc.gov/mods/v3 http://www.loc.gov/standards/mods/v3/mods-3-5.xsd">
            <!-- title-->
            <xsl:apply-templates select="element[@name = 'dc']/element[@name = 'title']/element/field"/>

            <!-- rights-->
            <xsl:choose>
                <xsl:when test="element[@name = 'dc']/element[@name = 'rights']/element/field">
                    <xsl:apply-templates select="element[@name = 'dc']/element[@name = 'rights']/element/field"/>
                </xsl:when>
                <xsl:otherwise>
                    <accessCondition type="local rights statement">All rights reserved. The accompanying
                        digital object and its associated documentation are provided for online research and
                        access purposes. Permission to use, copy, modify, distribute and present this
                        digital object and the accompanying documentation, without fee, and without written
                        agreement, is hereby granted for educational, non-commercial purposes only. The
                        Rhodes College Archives reserves the right to decide what constitutes educational
                        and commercial use; commercial users may be charged a nominal fee to be determined
                        by current, commercial rates for use of special materials. In all instances of use,
                        acknowledgement must begiven to Rhodes College Archives and Special Collection,
                        Memphis, TN. For information regarding permission to use this image, please email
                        the Archives at archives@rhodes.edu or call 901-843-3334.</accessCondition>
                </xsl:otherwise>
            </xsl:choose>

            <!-- urls -->
            <location>
                <xsl:apply-templates select='element[@name = "dc"]/element[@name = "identifier"]/element[@name = "uri"]/element[@name = "none"]/field[@name = "value"]'/>
                <xsl:apply-templates select='element[@name="bundles"]/element[@name="bundle"][field[@name="name"][text()="THUMBNAIL"]]/element[@name="bitstreams"]/element[@name="bitstream"][1]/field[@name="url"]'/>
            </location>

        </mods>
    </xsl:template>

Sub templates
=============

From our main template, we will apply other templates throughout our stylesheet.  These templates should match on the
corresponding selector.

.. code-block:: xslt


    <!-- title -->
    <xsl:template match="element[@name = 'dc']/element[@name = 'title']/element/field">
        <titleInfo>
            <title>
                <xsl:apply-templates/>
            </title>
        </titleInfo>
    </xsl:template>
