import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from api.models import User,Product,Order,OrderItem


class Command(BaseCommand):
    help='Create application data'

    def handle(self,*args,**kwargs):

        user=User.objects.filter(username='admin').first()
        if  not user:
            user=User.objects.create_superuser(username='admin',password='test')


        products=[
            Product(name="A scanner Darkly", description=lorem_ipsum.paragraph(),price=Decimal('12.99'),stock=4),
            Product(name="Coffe Machine", description=lorem_ipsum.paragraph(),price=Decimal('70.99'),stock=4),
            Product(name="Velvet Underground & Nico", description=lorem_ipsum.paragraph(),price=Decimal('15.99'),stock=4),
            Product(name="Enter the Wu-Tang (36 Chambers)", description=lorem_ipsum.paragraph(),price=Decimal('17.99'),stock=4),
            Product(name="Digital Camera", description=lorem_ipsum.paragraph(),price=Decimal('350.99'),stock=4),
            Product(name="Watch", description=lorem_ipsum.paragraph(),price=Decimal('500.05'),stock=4)
        ]    


        Product.objects.bulk_create(products)
        products=Product.objects.all()


        for _ in range(3):
            order=Order.objects.create(user=user)
            for product in random.sample(list(products),2):
                OrderItem.objects.create(
                    order=order, product=product, quantity=random.randint(1, 3)
                )