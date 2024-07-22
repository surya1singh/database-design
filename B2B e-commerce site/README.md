# B2B platform

It would be best to design a database for a B2B e-commerce site. 

B2B platform

Companies may have many end Customers. The B2B platform allows them to buy Products from qualified Suppliers and sell them to end Customers.

End Customers are identified by their document number, full name, and date of birth.

Companies are identified by CUIT number (a unique identifier), and name.

Suppliers are just a different type of company, and they expose a list of Products and default prices.

Each Company can define its own price list (catalogue) using Products from many Suppliers. They can also place Orders on the platform indicating which end customer has to receive the goods.



Requirements

1.) Database implementation.

2.) Generated data for the B2B database source.

3.) Dimensional model for data warehouse.




#Solution for Database implementation.

First, we need the tables for companies
* companies
* company_addresses
* suppliers

Second for products and catalog items
* product_categories
* products
* catalogs
* catalog_items
* discounts

  Assumption: one product belongs to one category. for many-to-many relationships, another table will be required.


Then there will be users
* users
* user_addresses

Lastly related to orders
* orders
* order_items
* reviews
* payments
* shipment_tracking


This is the basic conceptual data design