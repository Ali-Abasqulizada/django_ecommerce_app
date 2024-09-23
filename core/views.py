from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from . import models, forms
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def index(request):
    return render(request, 'core/index.html')

def shop(request):
    product_list = models.Product.objects.all().order_by('-created_at')
    paginator = Paginator(product_list, 9)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    categories = models.Category.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'core/shop.html', context)

def category(request, name):
    try:
        category_element = models.Category.objects.get(slug=name)
        categories = models.Category.objects.all()
        product_list = models.Product.objects.filter(category=category_element).order_by('-created_at')
        paginator = Paginator(product_list, 9)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
        context = {
            'category': category_element,
            'slug': name,
            'categories': categories,
            'products': products
        }
        return render(request, 'core/category.html', context)
    except:
        messages.warning(request, 'Category does not exits')
    return redirect('core:shop')

def product(request, name):
    try:
        product_element = models.Product.objects.get(slug=name)
        categories = models.Category.objects.all()
        reviews = models.Review.objects.filter(product=product_element).select_related('user').order_by('-created_at')
        if request.user.is_authenticated:
            my_review = reviews.filter(user=request.user).first()
            form = forms.ReviewForm(instance=my_review or None)
        else:
            form = forms.ReviewForm()
        context = {
            'product': product_element,
            'categories': categories,
            'form': form,
            'reviews': reviews
        }
        return render(request, 'core/product.html', context)
    except:
        messages.warning(request, 'Product does not exits')
    return redirect('core:shop')

@login_required()
def add_cart(request, name):
    if request.method == 'GET':
        return redirect('core:shop')
    try:
        cart_product = models.Product.objects.get(slug=name)
        quantity = request.POST.get('quantity')
        if int(quantity) > cart_product.count:
            messages.warning(request, 'Could not add to cart because there are not enough products in stock')
        else:
            models.Cart.objects.create(user=request.user, product=cart_product, quantity=quantity)
            messages.success(request, 'Product added to cart successfully')
        return redirect('core:product', name=name)
    except:
        messages.error(request, 'An error occurred')
    return redirect('core:shop')

@login_required()
def cart(request):
    cart_items = models.Cart.objects.filter(user=request.user).order_by('-created_at')
    for cart in cart_items:
        if cart.quantity > cart.product.count:
            cart.product.available = False
        cart.total_price = cart.quantity * cart.product.price
    context = {
        'carts': cart_items
    }
    return render(request, 'core/cart.html', context)

@login_required()
def delete_cart(request, id):
    if request.method == 'POST':
        cart_element = get_object_or_404(models.Cart, id=id, user=request.user)

        cart_total = cart_element.product.price * cart_element.quantity

        cart_element.delete()
        return JsonResponse({'success': True, 'cart_total': cart_total})

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

@login_required
def add_review(request, id):
    try:
        one_product = models.Product.objects.get(id=id)
        form = forms.ReviewForm(request.POST or None)
        if form.is_valid():
            rating = form.cleaned_data.get('rating')
            comment = form.cleaned_data.get('comment')
            existing_review = models.Review.objects.filter(user=request.user, product=one_product).first()
            if existing_review:
                old_average_rating = one_product.average_rating * one_product.review_count
                old_average_rating -= existing_review.rating
                old_average_rating += rating
                one_product.average_rating = old_average_rating / one_product.review_count
                one_product.change_category_count = False
                one_product.save()
                existing_review.rating = rating
                existing_review.comment = comment
                existing_review.save()
                messages.success(request, 'Review updated successfully!')
            else:
                old_average_rating = one_product.average_rating * one_product.review_count
                old_average_rating += rating
                one_product.review_count += 1
                one_product.average_rating = old_average_rating / one_product.review_count
                one_product.change_category_count = False
                one_product.save()
                models.Review.objects.create(
                    user=request.user,
                    product=one_product,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, 'Review added successfully!')
        return redirect('core:product', name=one_product.slug)
    except:
        messages.error(request, 'Product does not exits!')
    return redirect('core:shop')

def search_shop(request):
    keyword = request.GET.get('keyword', '')
    filter_type = request.GET.get('filter', '')
    product_list = models.Product.objects.filter(name__contains=keyword)
    if filter_type == 'oldest':
        product_list = product_list.order_by('created_at')
    elif filter_type == 'rating':
        product_list = product_list.order_by('-average_rating')
    elif filter_type == 'product':
        product_list = product_list.order_by('name')
    else:
        product_list = product_list.order_by('-created_at')
    paginator = Paginator(product_list, 9)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    categories = models.Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'keyword': keyword,
        'filter': filter_type
    }
    return render(request, 'core/shop.html', context)

def search_category(request, name):
    try:
        category_element = models.Category.objects.get(slug=name)
        keyword = request.GET.get('keyword', '')
        filter_type = request.GET.get('filter', '')
        product_list = models.Product.objects.filter(category=category_element, name__contains=keyword)
        if filter_type == 'oldest':
            product_list = product_list.order_by('created_at')
        elif filter_type == 'rating':
            product_list = product_list.order_by('-average_rating')
        elif filter_type == 'product':
            product_list = product_list.order_by('name')
        else:
            product_list = product_list.order_by('-created_at')
        paginator = Paginator(product_list, 9)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
        categories = models.Category.objects.all()
        context = {
            'products': products,
            'categories': categories,
            'keyword': keyword,
            'filter': filter_type,
            'category': category_element,
            'slug': name
        }
        return render(request, 'core/category.html', context)
    except:
        messages.warning(request, 'Category does not exits')
    return redirect('core:shop')

def contact_me(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        phone = request.POST.get('customer_phone')
        customer_message = request.POST.get('customer_message')
        context = {
            'name': customer_name,
            'email': customer_email,
            'phone': phone,
            'message': customer_message
        }
        mail_subject = 'Someone send you a message'
        mail_body = render_to_string('core/mail_to_ali.html', context)
        email = EmailMessage(
            mail_subject,
            mail_body,
            to=['ali.abasqulu@gmail.com']
        )
        email.content_subtype = 'html'
        email.send()
        messages.info(request, 'Your message has been sent successfully')
    return render(request, 'core/contact_me.html')
