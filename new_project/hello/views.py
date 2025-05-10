from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from hello.models import VinylRecord, Cart, CartItem, Category, Artist
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contacts(request):
    return render(request, 'contacts.html')

def map_view(request):
    return render(request, 'map.html')

def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

def catalog(request):
    products = VinylRecord.objects.all()
    return render(request, 'catalog.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('index')
        else:
            # Обработка ошибок формы
            for field, errors in form.errors.items():
                if field == '__all__':  # Общие ошибки (non_field_errors)
                    for error in errors:
                        messages.error(request, f"Ошибка: {error}")
                else:  # Ошибки конкретных полей
                    for error in errors:
                        messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_field = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(request, login=login_field, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вход выполнен успешно!')
                next_url = request.GET.get('next', reverse('index'))
                return redirect(next_url)
            else:
                messages.error(request, 'Неверный логин или пароль.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('index')

@login_required
def cart(request):
    cart_obj, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart_obj.items.all()
    total = sum(item.subtotal for item in cart_items)
    cart_data = {
        item.vinyl.id: {
            'name': item.vinyl.title,
            'artist': item.vinyl.artist.name,
            'category': item.vinyl.category.name,
            'price': float(item.vinyl.price),
            'image_url': item.vinyl.image_url,
            'quantity': item.quantity,
            'subtotal': float(item.subtotal),
        } for item in cart_items
    }
    return render(request, 'cart.html', {'cart': cart_data, 'total': float(total)})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(VinylRecord, id=product_id)
    cart_obj, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart_obj, vinyl=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'{product.title} добавлен в корзину.')
    return redirect('cart')

@login_required
def update_cart(request, product_id):
    cart_obj = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart_obj, vinyl__id=product_id)
    action = request.POST.get('action')
    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    elif action == 'decrease' and cart_item.quantity == 1:
        cart_item.delete()
    return redirect('cart')

@login_required
def clear_cart(request):
    cart_obj = get_object_or_404(Cart, user=request.user)
    cart_obj.items.all().delete()
    messages.success(request, 'Корзина очищена.')
    return redirect('cart')