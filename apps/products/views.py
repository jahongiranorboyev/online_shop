from decimal import Decimal
from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from apps.cart.models import Cart
from apps.comments.models import ProductComment
from apps.features.models import Feature, FeatureValue
from apps.products.models import Product
from apps.wishlist.models import Wishlist


def product_detail(request, pk):
    """
    View to display the detailed page of a product, including comments and features.
    """
    product = get_object_or_404(Product, pk=pk)
    comments = ProductComment.objects.filter(product_id=product.id).order_by('-created_at')

    # Handle pagination for comments
    comment_page = request.GET.get('comment_page', 1)
    comment_page_obj = Paginator(comments, 3).get_page(comment_page)

    # Handle cart quantity for authenticated users
    if not request.user.is_authenticated:
        user_cart_quantity = 0
    else:
        try:
            user_cart_quantity = Cart.objects.get(user=request.user, product_id=pk).quantity
        except Cart.DoesNotExist:
            user_cart_quantity = 0

    # Increment product view count on GET request
    if request.method == 'GET':
        product.seen_count += 1
        product.save()

    # Context for rendering the product detail page
    context = {
        'product': product,
        'comments': comments,
        'comment_page': comment_page_obj,
        'user_cart_quantity': user_cart_quantity,
        'page': 'detail',

    }
    return render(request=request, template_name='detail.html', context=context)


def product_by_feature(request, pk):
    """
    Redirects to the product detail page based on the feature filter.
    """
    return redirect('products:detail-page', pk=pk)


def product_list(request: WSGIRequest) -> HttpResponse:
    """
    Displays the product list with filtering options for categories, search, and features.
    """
    user = request.user
    user_cart = []
    user_wishlist = []
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Handle cart and wishlist for authenticated users
    if user.is_authenticated:
        user_cart = Cart.objects.filter(user=user).values_list('product', flat=True)
        user_wishlist = Wishlist.objects.filter(user=user).values_list('product', flat=True)

    # Store cart and wishlist in session
    request.session['user_cart'] = list(user_cart)
    request.session['user_wishlist'] = list(user_wishlist)

    # Retrieve search text and category ID from session
    search_text = request.session.get('search_text', None)
    cat_id = request.session.get('cat_id', None)
    queryset = Product.objects.order_by('-pk')

    if cat_id:
        queryset = queryset.filter(category_id=cat_id)

    if search_text:
        queryset = queryset.filter(title__icontains=search_text)

    # Handle filters based on date, rating, and views
    data = request.GET.get('date')
    rating = request.GET.get('rating')
    sort = request.GET.get('sort')

    if data:
        try:
            # Convert the date string to a timezone-aware datetime
            naive_date = timezone.datetime.strptime(data, "%Y-%m-%d")
            aware_date = timezone.make_aware(naive_date, timezone.get_current_timezone())
            queryset = queryset.filter(created_at=aware_date)
        except ValueError:
            pass

    filters = Q()
    if rating:
        try:
            rating_value = Decimal(rating) if rating else None
            if rating_value is not None:
                filters &= Q(avg_rating=rating_value)
        except (ValueError, TypeError):
            pass

    if sort == 'views':
        queryset = queryset.order_by('-seen_count')

    # Apply filters to queryset
    if filters:
        queryset = queryset.filter(filters)

    if min_price:
        queryset = queryset.filter(price__gte=min_price)

    if max_price:
        queryset = queryset.filter(price__lte=max_price)

    # Pagination setup for product listing
    page_number = request.GET.get('page', 1)
    paginate_obj = Paginator(queryset, 9)
    page_obj = paginate_obj.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'page': 'shop',
        'user_wishlist': user_wishlist,
        'user_cart': user_cart,
    }

    return render(request=request, template_name='shop.html', context=context)
