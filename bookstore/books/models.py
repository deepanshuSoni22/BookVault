# books/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='covers/')
    pdf_file = models.FileField(upload_to='pdfs/')
    upload_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title

class AccessRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    request_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    pdf_password = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        unique_together = ('user', 'book')
        
    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.status}"