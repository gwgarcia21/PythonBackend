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

def main():
    w1 = Warehouse.objects.get(name="Warehouse 1")

    # Adicionar produtos ao armazém
    p1 = Product.objects.get(name="Laptop")
    p2 = Product.objects.get(name="Python for Beginners")
    p3 = Product.objects.get(name="Fiction Novel")

    w1.products.add(p1, p2, p3)

    # Ver produtos no armazém
    warehouses = w1.products.all()

    print(warehouses)

    # Ver armazéns onde o produto está
    warehouses_p1 = p1.warehouses.all()

    print(warehouses_p1)

if __name__ == "__main__":
    main()
