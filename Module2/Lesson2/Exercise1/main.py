"""**Complex Query:** Write a Django ORM query to retrieve all active products with a 
price between 50 and 200, belonging to either the "Electronics" or "Books" category."""
import os
import django
from django.db.models import Q

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lesson2.settings')
django.setup()

# Agora você pode importar e usar os models
from store.models import Product

def main():
    products = Product.objects.filter((Q(category__name='Electronics') | Q(category__name='Books')) 
                                      & Q(price__gt=50) & Q(price__lt=200))

    for p in products:
        print(f"{p.id} - {p.name} ({p.category.name}) - R${p.price}")

if __name__ == "__main__":
    main()
