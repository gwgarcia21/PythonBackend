import os
import django

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lesson2.settings')
django.setup()

# Agora você pode importar e usar os models
from store.models import Product

def main():
    products = Product.objects.select_related('category').all()

    for p in products:
        print(f"{p.id} - {p.name} ({p.category.name}) - R${p.price}")

if __name__ == "__main__":
    main()
