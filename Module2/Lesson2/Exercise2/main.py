"""Transaction: Create a function that transfers a specified quantity of a 
product from one warehouse to another, ensuring that both stock updates occur 
within a single transaction."""
import os
import django
# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lesson2.settings')
django.setup()

# Agora você pode importar e usar os models
from store.models import Product, Warehouse
from django.db import transaction

@transaction.atomic
def transfer_products(origin: Warehouse, destination: Warehouse, products: list[Product]):
    origin.products.remove(*products)
    destination.products.add(*products)
    print(f"Transferred {len(products)} products from {origin.name} to {destination.name}.")
    
def main():
    w1 = Warehouse.objects.get(name="Warehouse 1")
    w2 = Warehouse.objects.get(name="Warehouse 2")
    print("Warehouse1: ", w1.products.all())
    print("Warehouse2: ", w2.products.all())

    products_to_transfer = w1.products.filter(category__name="Books")
    print(products_to_transfer)

    if (len(products_to_transfer) > 0):
        transfer_products(origin=w1, destination=w2, products=products_to_transfer)
    else:
        products_to_transfer = w2.products.filter(category__name="Books")
        transfer_products(origin=w2, destination=w1, products=products_to_transfer)

    print("Warehouse1: ", w1.products.all())
    print("Warehouse2: ", w2.products.all())

if __name__ == "__main__":
    main()
