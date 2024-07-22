from faker import Faker
import random
# from datetime import datetime, date, timedelta
Faker.seed()
from pprint import pprint

fake = Faker()

business_address_type = ['Billing','Shipping','Headquarters','Branch','Warehouse',
                         'Drop Shipping','Returns','Office','Factory','Supplier',
                         'Showroom','Distribution Center']
def create_companies(entities=1, id_start=1):
    data = []
    for i in range(entities):
        temp = {}
        id_ = id_start
        cuit = fake.ean13()
        name = fake.company()
        temp = {
            "id":id_,
            "cuit":cuit,
            "name":name
        }
        data.append(temp)
    return data


def create_company_address(id_start, company_id, address_type="Headquarters"):
    data = {"id": id_start,
            "company_id": company_id,
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip_code": fake.zipcode(),
            "country": fake.country(),
            "address_type": address_type}
    return data

def get_suppliers_id(max_val=10):
    ids = [1, 2]
    id_ = ids[-1]
    while True:
        id_ = sum(ids[-2:])
        if id_ > max_val:
            break
        ids.append(id_)
    return ids

def generate_company_related(entities=10):
    companies = create_companies(entities )
    suppliers = []
    company_addresses = []
    company_address_id = 1
    supplier_ids = get_suppliers_id(max_val = entities )
    for d in companies:
        company_id = d["id"]
        if company_id in supplier_ids:
            supplier = {"id":company_id,"company_id":company_id}
            suppliers.append(supplier)
        for address_type in random.choices(business_address_type, k=random.randint(1,3)):
            company_address = create_company_address(company_address_id, company_id, address_type=address_type)
            company_addresses.append(company_address)
            company_address_id+=1
    return companies, company_addresses, suppliers


def create_product_categories(entities=1, id_start=1):
    data = []
    for i in range(1, entities+1):
        temp = {"id":id_start+i,
                "category_name":fake.word().capitalize(),
                "description":fake.sentence()
                }
        data.append(temp)
    return data


def create_products(entities=1, id_start=1, product_category_id=1, supplier_id = 1):
    data = []
    for i in range(entities):
        temp = {"id":id_start + i,
                "name":fake.word(),
                "product_category_id":product_category_id,
                "supplier_id":supplier_id,
                "default_price":round(random.uniform(10.0, 100.0), 2),
                "is_active":1
                }
        data.append(temp)
    return data

def generate_products_related(supplier_ids, entities=10):
    product_categories = create_product_categories(entities)
    product_id = 1
    product_list = []
    for supplier_id in supplier_ids:
        number_of_products = random.randint(0,20)
        product_category_id = random.choice(product_categories)["id"]
        products = create_products(entities=number_of_products,
                                   id_start=product_id,
                                   product_category_id=product_category_id,
                                   supplier_id = supplier_id)
        product_id += number_of_products
        product_list.extend(products)

    return product_categories, product_list
pprint(generate_products_related(supplier_ids=[1,2,3,5], entities=2))
