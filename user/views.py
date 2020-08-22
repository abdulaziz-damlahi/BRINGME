
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from home import models
from home.models import Setting, FAQ
from order.models import Order, OrderProduct
from product.models import Category, comment
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile


@login_required(login_url='/login')
def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'setting': setting,
               'profile': profile}
    return render(request, 'user_profile.html', context)


def login_form(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Error !! Username or Password is incorrect")
            return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.

    category = Category.objects.all()
    context = {'category': category
        , 'setting': setting}
    return render(request, 'login_form.html', context)


def signup_form(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, 'your account has benn established')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/signup')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form, 'setting': setting,
               }
    return render(request, 'signup_form.html', context)


def user_password(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        # category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form,'setting': setting, })


@login_required(login_url='/login')
def user_update(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(
            instance=request.user.userprofile)  # "userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'setting': setting,
        }
        return render(request, 'user_update.html', context)


def logout_fuc(request):
    logout(request)
    return HttpResponseRedirect('/')


def user_password(request):

        if request.method == 'POST':

            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return HttpResponseRedirect('/user')
            else:
                messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
                return HttpResponseRedirect('/user/password')
        else:
            category = Category.objects.all()
            form = PasswordChangeForm(request.user)
            setting = Setting.objects.get(pk=1)
            context = {
                'category': category,
                'setting': setting,
            }
            return render(request, 'user_password.html', {'form': form,'category': category })


def user_orders(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    orders=Order.objects.filter(user_id=current_user.id)
    context = {'category': category,
               'orders': orders,
               'setting': setting,
               }
    return render(request, 'order_user.html', context)


@login_required(login_url='/login') # Check login
def user_order_product_detail(request,id,oid):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id,user_id=current_user.id)
    context = {
        'category': category,
        'order': order,
        'setting': setting,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login') # Check login
def user_order_product(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
    context = {'category': category,
               'setting': setting,
               'order_product': order_product,
               }
    return render(request, 'user_order_products.html', context)


@login_required(login_url='/login') # Check login
def user_orderdetail(request,id):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        'category': category,
        'order': order,
        'setting': setting,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)



def user_comments(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    Comments = comment.objects.filter(user_id=current_user.id)
    context = {
        'setting': setting,
        'category': category,
        'Comments': Comments,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login') # Check login
def user_deletecomment(request,id):
    current_user = request.user
    comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')


def faq(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    faq = FAQ.objects.filter(status="True").order_by("ordernumber")
    context = {
        'category': category,
        'faq': faq,
        'setting': setting,
    }
    return render(request, 'faq.html', context)


def Resturants_home(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    faq = FAQ.objects.filter(status="True").order_by("ordernumber")
    context = {
        'category': category,
        'faq': faq,
        'setting': setting,
    }
    return render(request, 'Resturants.html', context)



