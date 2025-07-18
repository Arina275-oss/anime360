from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Category, Product, Promotion, SpecialOffer


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'shop/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    
    # Track recently viewed products in session (last 5 products)
    viewed_products = request.session.get('viewed_products', [])
    if product.id not in viewed_products:
        viewed_products.append(product.id)
        request.session['viewed_products'] = viewed_products[-5:]
    
    return render(request, 'shop/detail.html', {'product': product})


def new_arrivals(request):
    # Products added in the last 30 days
    date_threshold = timezone.now() - timedelta(days=30)
    new_products = Product.objects.filter(
        created__gte=date_threshold,
        available=True
    ).order_by('-created')
    
    return render(request, 'shop/product/new_arrivals.html', {
        'new_products': new_products,
        'section': 'new_arrivals'
    })


def promotion_list(request):
    active_promotions = Promotion.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).order_by('-start_date')
    
    return render(request, 'shop/promotion_list.html', {
        'promotions': active_promotions,
        'section': 'promotions'
    })


def promotion_detail(request, slug):
    promotion = get_object_or_404(
        Promotion,
        slug=slug,
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    )
    
    products = promotion.products.filter(available=True)
    
    return render(request, 'shop/promotion_detail.html', {
        'promotion': promotion,
        'products': products,
        'section': 'promotions'
    })


def special_offers(request):
    active_offers = SpecialOffer.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).select_related('product')
    
    return render(request, 'shop/special_offers.html', {
        'offers': active_offers,
        'section': 'special_offers'
    })



