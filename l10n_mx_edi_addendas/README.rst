.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
    :alt: License: LGPL-3

================
Mexican Addendas
================

Usage:
======

This module provides the structure for when signing an invoice, the xml corresponding appears with the addenda information.

As a first step, each addenda must be added in its corresponding partner.

     .. figure:: ../l10n_mx_edi_addendas/static/src/img/partner_addenda.png
        :width: 600pt

The addenda information is taken from the fields that are explicitly included in the invoice, and for the case that the
information is not in a specific field, it is necessary fill the fields in the wizard that appears in the view invoice.

Each addenda adds a button in invoice view wich open a wizard where the extra information
for the addenda can be set it. The fields in each wizard depend on the information required
by the addenda corresponding to the partner in active invoice.

     .. figure:: ../l10n_mx_edi_addendas/static/src/img/wizard_button.png
        :width: 600pt

Actually, the addendas available are:

Chrysler
--------

A button with name ``ADDENDA CHRYSLER`` is added in invoice view. This button opens the
following wizard:

     .. figure:: ../l10n_mx_edi_addendas/static/src/img/wizard_addenda_chrysler.png
        :width: 600pt

In the wizard is provided the information corresponding to each field.

Ford
----

A button with name ``ADDENDA FORD`` is added in invoice view. This button opens the
following wizard:

     .. figure:: ../l10n_mx_edi_addendas/static/src/img/wizard_addenda_ford.png
        :width: 600pt

In the wizard is provided the information corresponding to each field.

Porcelanite
-----------

A button with name ``ADDENDA PORCELANITE`` is added in invoice view. This button opens the
following wizard:


In the wizard is provided the information corresponding to each field.

Bosh
----

A button with name ``ADDENDA BOSH`` is added in invoice view. This button opens the
following wizard:


In the wizard is provided the information corresponding to each field.

Technical:
==========

To install this module go to ``Apps`` search ``l10n_mx_edi_addendas`` and click
in button ``Install``.

When the module is installed it is necessary activate the required addendas. To do
that go to Invoicing configuration settings and search by ``MX EDI addendas``. There
you can find the available addendas in the sistem.

     .. figure:: ../l10n_mx_edi_addendas/static/src/img/l10n_mx_edi_addendas_conf.png
        :width: 600pt


Contributors
------------

* Yennifer Santiago <yennifer@vauxoo.com>
* Nhomar Hernández <nhomar@vauxoo.com>
* Julio Serna Hernández <julio@vauxoo.com>

Maintainer
----------

.. figure:: https://www.vauxoo.com/logo.png
   :alt: Vauxoo
   :target: https://vauxoo.com

This module is maintained by Vauxoo.

a latinamerican company that provides training, coaching,
development and implementation of enterprise management
sytems and bases its entire operation strategy in the use
of Open Source Software and its main product is odoo.

To contribute to this module, please visit http://www.vauxoo.com.

