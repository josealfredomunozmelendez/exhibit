==========================================
Odoo Mexico Localization for Stock/Landing
==========================================

This module extends the functionality of Mexican localization to support customs numbers related with landed costs when you generate the electronic invoice.

Usage
=====

To use this module, you need to:

* Generate a new purchase order of a product from abroad. Landed costs are only possible for products configured in real time valuation with real price costing method. The costing method is configured on the product category

.. image:: static/description/purchase_order_new.png

* Receive the product of the purchase order

.. image:: static/description/picking_done_purchase.png

* Go to Inventory -> Inventory control -> Landed Cost

* Create a new landed cost indicating the picking of the purchase order and the number of the customs information (pedimento). Landed costs are only possible for products configured in real time valuation with real price costing method. The costing method is configured on the product category

.. image:: static/description/landed_cost_picking.png

* Start by creating specific products to indicate your various Landed Costs, such as freight, insurance or custom duties.
  Go to Inventory -> Configuration -> Landed Cost types. Landed costs are only possible for products configured in real time valuation with real price costing method. The costing method is configured on the product category.

.. image:: static/description/product_landed_cost.png

* Click the Compute button to see how the landed costs will be split across the picking lines.

.. image:: static/description/compute_landed_cost.png

* To confirm the landed costs attribution, click on the Validate button.

.. image:: static/description/validate_landed_cost.png

* Create a sales order for the product purchased from abroad

.. image:: static/description/sale_order_new.png

* Delivery the product related to the sales order

.. image:: static/description/picking_done_sale.png

* Create and validate a new invoice associated with the sales order

.. image:: static/description/validate_invoice_customs.png

* The customs information is found in the lines of the invoice associated with each product.

.. image:: static/description/invoice_custom_pedimento.png

* Check the electronic invoice associated with the product where the node of the customs information is displayed

.. image:: static/description/invoice_custom_xml.png


Credits
=======

* Jarsa Sistemas, Vauxoo


Contributors
------------

* Alan Ramos <alan.ramos@jarsa.com.mx>
* Miguel Ruiz <miguel.ruiz@jarsa.com.mx>
* Julio Serna <julio@vauxoo.com>
* Luis Torres <luis_t@vauxoo.com>
* Deivis Laya <deivis@vauxoo.com>

Do not contact contributors directly about support or help with technical issues.
