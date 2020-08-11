from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from nurseryapp.models import tblplants, tblorder, tblreg
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home(request):
    return render(request, 'index.html')


def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass']
        try:
            if User.objects.get(email=email):
                user = User.objects.get(email=email)
            else:
                messages.warning(request, 'User Not Found!')
                return redirect('./login')
            pwd_valid = user.check_password(password)
            if pwd_valid:
                if user.is_staff:
                    login(request, user)
                    return redirect('./home')
                else:
                    login(request, user)
                    return redirect('./')
            else:
                messages.warning(request, 'Password is Wrong!')
                return redirect('./login')
        except User.DoesNotExist:
            messages.warning(request, 'User Not Found!')
            return redirect('./login')
    else:
        return render(request, 'login.html')


def user_registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['pass']
        confirm_password = request.POST['con-pass']
        if password != confirm_password:
            messages.warning(request, "Password or Confirm Password Does Not Match")
            return redirect('./registration')
        else:
            try:
                if User.objects.get(email=email):
                    messages.success(request, 'Email is already registered!! Please Login with your email .')
                    return redirect('./login')
            except User.DoesNotExist:
                a = User.objects.create_user(first_name=name, email=email,
                                             username=email,
                                             password=password)
                a.save()
                messages.success(request, 'Registration successful!!Please Login with your Account.')
                return redirect("./login")
    else:
        return render(request, 'registration.html')


def nurseries_registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['pass']
        confirm_password = request.POST['con-pass']
        address = request.POST['address']
        photo = request.FILES['photo']
        if password != confirm_password:
            messages.warning(request, "Password or Confirm Password Does Not Match")
            return redirect('./nurseries@')
        else:
            try:
                if User.objects.get(email=email):
                    messages.success(request, 'Email is already registered!! Please Login with your email .')
                    return redirect('./login')
            except User.DoesNotExist:
                a = User.objects.create_user(first_name=name, email=email,
                                             username=email,
                                             password=password, )
                b = tblreg(address=address, user_email=email, image=photo)
                a.is_staff = True
                a.save()
                b.save()
                messages.success(request, 'Registration successful!!Please Login with your Account.')
                return redirect("./login")
    else:
        return render(request, 'registration_nurseries.html')


def user_logout(request):
    logout(request)
    return render(request, 'logout.html')


def order_accept(request):
    return render(request, 'order_accept.html')


def order_done(request):
    del request.session['plant_id']
    del request.session['quantity']
    del request.session['name']
    del request.session['email']
    return render(request, 'order_done.html')


def nursery_home(request):
    if request.method == 'POST':
        order_id = request.POST['order_id']
        order_data = tblorder.objects.get(pk=order_id)
        plant_id = order_data.plant_id
        plant_data = tblplants.objects.get(pk=plant_id)
        available_quantity = plant_data.quantity
        b = tblorder.objects.get(pk=order_id)
        b.order_status = "1"
        b.save()
        stock = int(plant_data.quantity) - int(order_data.quantity)
        a = tblplants.objects.get(pk=plant_id)
        a.quantity = stock
        a.save()
        return redirect("./order_accept")
    else:
        user = User.objects.get(email=request.user)
        tasks_obj = tblplants.objects.raw('SELECT * FROM tblorder as tblo, tblplants as tblp WHERE tblp.user_id = %s', [user.id])
        print(tasks_obj)
        return render(request, 'nursery_home.html', {"alltasks": tasks_obj})


def addplants(request):
    if request.method == 'POST':
        name = request.POST['name']
        descriptions = request.POST['descriptions']
        price = request.POST['price']
        stock = request.POST['stock']
        photo = request.FILES['plant_photo']
        user = User.objects.get(email=request.user)
        a = tblplants(name=name, descriptions=descriptions, price=price, quantity=stock, user=user,
                      plant_image=photo)
        a.save()
        return redirect("./home")
    else:
        return render(request, 'addplants.html')


def nursery(request):
    user = "1"
    tasks_obj = User.objects.raw(
        'SELECT * FROM auth_user as au, tblreg as reg WHERE au.email=reg.user_email and is_staff = %s', [user])
    return render(request, 'nursery.html', {"alltasks": tasks_obj})


def shop(request):
    if request.method == 'POST':
        nursery_id = request.POST['nursery_id']
        tasks_obj = User.objects.raw('SELECT * FROM tblplants WHERE quantity > 0 and user_id = %s', [nursery_id])
        return render(request, 'shop.html', {"alltasks": tasks_obj})
    else:
        plant_id = request.GET['plant_id']
        return redirect('./shop_details?resp=%s' % plant_id)


def shop_details(request):
    if request.method == 'POST':
        request.session['plant_id'] = request.POST['plant_id']
        request.session['quantity'] = request.POST['quantity']
        return redirect('./checkout')
    else:
        plant_id = request.GET.get('resp')
        tasks_obj = User.objects.raw('SELECT * FROM tblplants WHERE id = %s', [plant_id])
        return render(request, 'shop_details.html', {"alltasks": tasks_obj})


def checkout(request):
    if request.method == 'POST':
        customer_name = request.POST['name']
        quantity = request.POST['quantity']
        amount = request.POST['amount']
        plant_id = request.POST['plant_id']
        user_id = request.POST['user_id']
        a = tblorder(customer_name=customer_name, quantity=quantity, amount=amount, plant_id=plant_id, user_id=user_id)
        a.save()
        return redirect("./order_done")
    else:
        request.session['name'] = request.user.first_name
        request.session['email'] = request.user.email
        plant_id = request.session['plant_id']
        tasks_obj = tblplants.objects.get(pk=plant_id)
        price = tasks_obj.price
        p_name = tasks_obj.name
        user_id = request.user.id
        t_price = int(price) * int(request.session['quantity'])
        return render(request, 'checkout.html',
                      {'price': price, 'p_name': p_name, 't_price': t_price, 'user_id': user_id})
