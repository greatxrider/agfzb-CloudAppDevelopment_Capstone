"""this is the models.py file for the djangoapp app"""
from django.db import models
from django.utils import timezone

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    """the CarMake class"""
    name = models.CharField(null=False, max_length=30, default='CarMake')
    description = models.CharField(null=False, max_length=1000, default='CarMake')
    objects = models.Manager() 
    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    """This is the CarModel class"""
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'WAGON'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'WAGON'),
    ]
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=50, default='CarModel')
    dealer_id = models.IntegerField(null=False, default=0)
    type = models.CharField(null=False, max_length=5, choices=CAR_TYPES, default=SEDAN)
    year = models.DateField(null=False, default=timezone.now)
    objects = models.Manager() 
    def __str__(self):
        return "Name: " + self.name + "," + \
               "Type: " + self.type + "," + \
               "Year: " + str(self.year) + "," + \
               "DealerId: " + str(self.dealer_id)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    """this is the CarDealer class"""
    def __init__(self, address, city, full_name, id, lat, long, short_name, state, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state full
        self.state = state
        # Dealer state abbre
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    """this is the DealerReview class"""
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, id):
        # Dealer id
        self.dealership = dealership
        # Review id
        self.name = name
        # Review purchase
        self.purchase = purchase
        # Review review
        self.review = review
        # Review purchase_date
        self.purchase_date = purchase_date
        # Review car_make
        self.car_make = car_make
        # Review car_model
        self.car_model = car_model
        # Review car_year
        self.car_year = car_year
        # Review id
        self.id = id

    def __str__(self):
        return "Dealer name: " + self.dealership
