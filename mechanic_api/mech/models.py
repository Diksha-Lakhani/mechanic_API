from django.db import models
from django.core.validators import RegexValidator

#making the databases here

class Mechanic(models.Model):           #databse table definition
    phone_validator = RegexValidator(           #checks for exactly 10 digits in the phone number
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10, validators=[phone_validator])
    location = models.CharField(max_length=255)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    is_open = models.BooleanField(default=True)
    services = models.CharField(
        max_length=500,
        help_text="Comma-separated list of services, e.g. 'Oil Change, Tire Repair'"
    )

    def __str__(self):      #returns objects as actual names in the admin panel (not as Mechanic object (1) but as John Cena)
        return self.name

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    vehicle_number_validator = RegexValidator(
        regex=r'^[A-Z0-9\- ]{4,15}$',       #can contain digits,hyphen,space and letters between 4 to 15 characters
        message="Enter a valid vehicle number (letters, numbers, spaces, hyphens only)."
    )

    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(
        max_length=10,
        validators=[Mechanic.phone_validator]
    )
    vehicle_number = models.CharField(
        max_length=15,
        validators=[vehicle_number_validator]
    )
    mechanic = models.ForeignKey(
        Mechanic,
        on_delete=models.CASCADE,       #if a mechanic is deleted, their services will be deleted too
        related_name='service_requests'
    )
    service = models.CharField(max_length=100)
    problem_description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)        #automatically time stamps current date an dtime when it is first created

    def __str__(self):          #displays at django's admin panel
        return f"{self.customer_name} - {self.service} ({self.status})"

    