from django.db import models
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Слаг')
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', 
    on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, verbose_name='Слаг')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='На складе')
    available = models.BooleanField(default=True, verbose_name='Доступен')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    def get_discounted_price(self):
        if hasattr(self, 'active_promotion'):
            discount = self.active_promotion.discount_percent / 100
            return self.price * (1 - discount)
        return self.price
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
    
    def get_discount(self):
        # Проверяем специальные предложения
        active_special_offer = self.special_offers.filter(is_active=True).first()
        if active_special_offer:
            return {
                'percent': active_special_offer.discount_percent,
                'discounted_price': active_special_offer.discounted_price,
                'end_date': active_special_offer.end_date
            }
        
        # Проверяем активные акции
        now = timezone.now()
        active_promotion = self.promotions.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).first()
        
        if active_promotion:
            return {
                'percent': active_promotion.discount_percent,
                'discounted_price': self.price * (100 - active_promotion.discount_percent) / 100,
                'end_date': active_promotion.end_date
            }
        
        return None

class SpecialOffer(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, 
                              verbose_name='Товар', related_name='special_offers')
    discount_percent = models.PositiveIntegerField(verbose_name='Процент скидки')
    start_date = models.DateTimeField(verbose_name='Начало акции')
    end_date = models.DateTimeField(verbose_name='Конец акции')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    
    class Meta:
        verbose_name = 'Специальное предложение'
        verbose_name_plural = 'Специальные предложения'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['-start_date']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"Спецпредложение на {self.product.name} - {self.discount_percent}%"
    
    def save(self, *args, **kwargs):
        now = timezone.now()
        if now < self.start_date or now > self.end_date:
            self.is_active = False
        else:
            self.is_active = True
        super().save(*args, **kwargs)
    
    @property
    def discounted_price(self):
        return self.product.price * (100 - self.discount_percent) / 100

class Promotion(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название акции")
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(verbose_name="Описание акции")
    start_date = models.DateTimeField(verbose_name="Дата начала")
    end_date = models.DateTimeField(verbose_name="Дата окончания")
    discount_percent = models.PositiveIntegerField(verbose_name="Процент скидки")
    products = models.ManyToManyField(Product, related_name='promotions')
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    image = models.ImageField(upload_to='promotions/', blank=True, null=True)

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['-start_date']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return self.title

    def is_currently_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date and self.is_active
    
    def save(self, *args, **kwargs):
        # Обновляем статус активности при сохранении
        self.is_active = self.is_currently_active()
        super().save(*args, **kwargs)
    

    
