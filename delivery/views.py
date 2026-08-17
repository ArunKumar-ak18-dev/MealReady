from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import User, Restaurent, Item, Cart


def welcome(request):
    return render(request, "index.html")

def open_signup(request):
    return render(request, "signup.html")

def open_signin(request):
    return render(request, "signin.html")

def signup(request):
    if request.method == 'POST':

        name = request.POST.get('username')
        pass1 = request.POST.get('password')
        gmail = request.POST.get('email')
        mobile1 = request.POST.get('mobile')
        address1 = request.POST.get('address')

        # Check empty fields
        if not name:
            return HttpResponse("Please enter username")

        if not pass1:
            return HttpResponse("Please enter password")

        if not gmail:
            return HttpResponse("Please enter email")

        if not mobile1:
            return HttpResponse("Please enter mobile number")

        if not address1:
            return HttpResponse("Please enter address")

        # Check duplicate email
        if User.objects.filter(email=gmail).exists():
            return HttpResponse(
                "This Email is already registered. Please use a different email."
            )

        # Check duplicate username
        if User.objects.filter(username=name).exists():
            return HttpResponse(
                "This username is already registered. Please use a different username."
            )

        # Check duplicate mobile
        if User.objects.filter(mobile=mobile1).exists():
            return HttpResponse(
                "This mobile number is already registered. Please use a different mobile number."
            )

        # Create user
        user = User(
            username=name,
            password=pass1,
            email=gmail,
            mobile=mobile1,
            address=address1
        )

        user.save()

        return render(request, "signin.html")

    else:
        return HttpResponse("Invalid Request")

def signin(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        pass1 = request.POST.get('password')
        username = request.POST.get('username')

        try:
            user = User.objects.get(mobile=mobile, password=pass1)
            request.session['username'] = user.username
            if mobile == "9014404052":
                return render(request, "admin_home.html")
            else:
                return render(request,"customer_home.html", {'username':user.username})
        except User.DoesNotExist:
            return HttpResponse("Invalid Username or Password")
    else:
        return HttpResponse("Invalid Request")

def open_add_restaurent(request):
    return render(request, "add_restaurent.html")

def add_restaurent(request):

    if request.method == 'POST':

        name = request.POST.get("name")
        picture = request.POST.get("picture")
        cuisine = request.POST.get("cuisine")
        rating = request.POST.get("rating")

        # Check whether any field is empty
        if not name or not picture or not cuisine or not rating:
            return HttpResponse("Invalid details. Please fill all the fields.")

        try:
            Restaurent.objects.get(name=name)

            return HttpResponse("Duplicate restaurant")

        except Restaurent.DoesNotExist:

            Restaurent.objects.create(
                name=name,
                picture=picture,
                cuisine=cuisine,
                rating=rating
            )

            return render(request, 'admin_home.html')

    else:
        return HttpResponse("Invalid Request")
    

def show_restaurents(request):
     restaurent_List = Restaurent.objects.all()
     return render(request, "show_restaurents.html", {"restaurent_List":restaurent_List})


def open_add_items(request,restaurant_id):
    restaurant = Restaurent.objects.get(id = restaurant_id)
    itemList = restaurant.items.all()
    return render(request, 'add_items.html', {"itemList":itemList, "restaurant" : restaurant})

def add_items(request,restaurant_id):
    restaurant = Restaurent.objects.get(id = restaurant_id)

    if request.method == 'POST':
      name = request.POST.get("name")
      des = request.POST.get("description")
      price = request.POST.get("price")
      veg = request.POST.get('vegetarian') == 'on'
      picture = request.POST.get('picture')
    
      try:
        Item.objects.get(name = name)
        return HttpResponse("Duplicate item!")
      except:
        Item.objects.create(
          restaurant = restaurant,
          name = name,
          description = des,
          price = price,
           veg = veg,
           picture = picture
        )

    return HttpResponse("Item added successfully")


def show_res_cus(request,username):
    restaurant = Restaurent.objects.all()
    return render(request,'customer_DashBoard.html',{"restaurant_list":restaurant,"username":username})

def open_update_restaurant(request,restaurant_id):
    restaurant = Restaurent.objects.get(id = restaurant_id)
    return render(request, 'update_restaurant.html', {"restaurant":restaurant})

def update_restaurant(request,restaurant_id):
    restaurant = Restaurent.objects.get(id = restaurant_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        picture = request.POST.get('picture')
        cuisine = request.POST.get('cuisine')
        rating = request.POST.get('rating')

        restaurant.name = name
        restaurant.picture = picture
        restaurant.cuisine = cuisine
        restaurant.rating = rating

        restaurant.save()
    return redirect('show_restaurents')    


def delete_restaurant(request, restaurant_id):
    restaurant = Restaurent.objects.get(id = restaurant_id)
    restaurant.delete()
    return redirect(request, 'show_restaurents')

def view_menu(request, restaurant_id, username):
    restaurant = Restaurent.objects.get(id=restaurant_id)
    itemList = restaurant.items.all()

    return render(request, "customer_items.html", {
        "restaurant": restaurant,
        "itemList": itemList,
        "username": username
    })

def add_to_cart(request, item_id, username):
    item = Item.objects.get(id = item_id)
    customer = User.objects.get(username = username)

    cart, created = Cart.objects.get_or_create(customer = customer)
    cart.items.add(item)
    return HttpResponse('added to cart')

def view_cart(request, username):
    customer = User.objects.get(username = username)
    cart = Cart.objects.filter(customer = customer).first()
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    return render(request, 'cart.html',{"itemList" : items, "total_price" : total_price, "username":username})

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

def orders(request, username):

    customer = get_object_or_404(User, username=username)

    cart = Cart.objects.filter(customer=customer).first()

    # Check if cart is empty
    if not cart or not cart.items.exists():
        return HttpResponse("Please add items to cart before placing an order.")

    # Fetch cart items and total price
    cart_items = cart.items.all()
    total_price = cart.total_price()

    # Clear cart after getting the details
    cart.items.clear()

    return render(request, 'orders.html', {
        'username': username,
        'customer': customer,
        'cart_items': cart_items,
        'total_price': total_price,
    })