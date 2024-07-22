from faker import Faker
import random
# from datetime import datetime, date, timedelta
Faker.seed()
from pprint import pprint

fake = Faker()

business_address_type = ['Billing','Shipping','Headquarters','Branch','Warehouse',
                         'Drop Shipping','Returns','Office','Factory','Supplier',
                         'Showroom','Distribution Center']
def create_companies(enteries = 1, id_start = 1):
    data = []
    for i in range(enteries):
        temp = {}
        id_ = id_start + i
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
    data = {"id": id_start + 1,
            "company_id": company_id,
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "zip_code": fake.zipcode(),
            "country": fake.country(),
            "address_type": address_type}
    return data

def get_suppliers_id(max_val = 10):
    ids = [1, 2]
    id_ = ids[-1]
    while True:
        id_ = sum(ids[-2:])
        if id_ > max_val:
            break
        ids.append(id_)
    return ids

def generate_company_related(entries = 10):
    companies = create_companies(entries)
    suppliers = []
    company_addresses = []
    supplier_ids = get_suppliers_id(max_val = entries)
    for d in companies:
        company_id = d["id"]
        if company_id in supplier_ids:
            supplier = {"id":company_id,"company_id":company_id}
            suppliers.append(supplier)
        for address_type in random.choices(business_address_type, k=random.randint(1,3)):
            company_address = create_company_address(company_id, company_id, address_type=address_type)
            company_addresses.append(company_address)
    return companies, company_addresses, suppliers
pprint(generate_company_related(10))
