"""Transaction: Create a function that transfers a specified quantity of a 
product from one warehouse to another, ensuring that both stock updates occur 
within a single transaction."""
import os
import django
# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lesson2.settings')
django.setup()

# Agora você pode importar e usar os models
from store.models import Warehouse

def main():
    new_warehouses = [
        Warehouse(name='Warehouse 1'),
        Warehouse(name='Warehouse 2'),
    ]
    Warehouse.objects.bulk_create(new_warehouses)

if __name__ == "__main__":
    main()
