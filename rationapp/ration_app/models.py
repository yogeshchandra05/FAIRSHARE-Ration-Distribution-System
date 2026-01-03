from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# -------------------------------------------
# User Authentication and Profile
# -------------------------------------------

class UserAuth(models.Model):
    ROLE_CHOICES = [
        ('shopkeeper', 'Shopkeeper'),
        ('citizen', 'Citizen'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    
    # Personal info
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        blank=True, 
        null=True,
        help_text="Enter age in years"
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    # Contact info
    phone = models.CharField(max_length=15)
    address_line = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="Not Provided",
        help_text="House No. / Street / Area"
    )
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)


    # Financial info
    income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Enter annual income in INR"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# -------------------------------------------
# Ration Card
# -------------------------------------------
class RationCard(models.Model):
    CATEGORY_CHOICES = [
        ('APL', 'Above Poverty Line'),
        ('BPL', 'Below Poverty Line'),
        ('AAY', 'Antyodaya Anna Yojana'),
    ]
    card_number = models.CharField(max_length=50, unique=True)
    user = models.OneToOneField(UserAuth, on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    issue_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_number} - {self.category}"


# -------------------------------------------
# Beneficiary
# -------------------------------------------
class Beneficiary(models.Model):
    ration_card = models.ForeignKey(RationCard, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[
        ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')
    ])
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    income = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


# -------------------------------------------
# Fair Price Shop
# -------------------------------------------
class FairPriceShop(models.Model):
    shop_name = models.CharField(max_length=100)
    shopkeeper = models.ForeignKey(UserAuth, on_delete=models.SET_NULL, null=True, related_name='shopkeeper')
    location = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=15)
    license_number = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.shop_name


# -------------------------------------------
# Warehouse / Godown
# -------------------------------------------
class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    capacity_in_tons = models.FloatField()
    manager_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.warehouse_name


# -------------------------------------------
# Supply Chain
# -------------------------------------------
class SupplyChain(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
    ]
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    shop = models.ForeignKey(FairPriceShop, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity_supplied = models.FloatField()
    supply_date = models.DateField()
    transport_mode = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.item_name} - {self.status}"


# -------------------------------------------
# Shop Stock
# -------------------------------------------
class Stock(models.Model):
    shop = models.ForeignKey(FairPriceShop, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    available_quantity = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item_name} ({self.available_quantity} {self.unit})"


# -------------------------------------------
# Transaction
# -------------------------------------------
class Transaction(models.Model):
    ration_card = models.ForeignKey(RationCard, on_delete=models.CASCADE)
    shop = models.ForeignKey(FairPriceShop, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity = models.FloatField()
    date_of_distribution = models.DateField(auto_now_add=True)
    month_year = models.CharField(max_length=20)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.ration_card.card_number} - {self.item_name}"


# -------------------------------------------
# Audit Log
# -------------------------------------------
class AuditLog(models.Model):
    user = models.ForeignKey(UserAuth, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    table_name = models.CharField(max_length=100)
    record_id = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.action} @ {self.timestamp}"
