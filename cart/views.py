from django.shortcuts import render, reverse, redirect
from django.contrib import messages


# Function Views
def view_cart(request):
    """Render Cart template & cart contents if any membership has been
    selected by user"""
    context = {
        'cart_page': 'active'
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request, id):
    print(id)
    """Add membership plan to cart"""
    plan_qty = 1

    cart = request.session.get('cart', {})
    cart[id] = cart.get(id, plan_qty)

    print(cart[id])
    request.session['cart'] = cart
    messages.success(request, 'Membership Plan added to Cart!')
    return redirect(reverse('membership'))


def del_from_cart(request):
    """Remove membership plan from cart, or in our case, as only one
    membership can be added to cart at any given time aka `clear cart`"""
    cart = request.session.get('cart', {})

    cart.clear()
    request.session['cart'] = cart
    messages.success(request, 'Cart has been emptied.')
    return redirect(reverse('membership'))
