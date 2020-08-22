from django.contrib import messages
from django.db.models import query
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from home.models import Setting, ContactForm, ContactF
from home.forms import searchForm
from product.models import Category, Product, Images, comment
import json

def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    products_slider = Product.objects.all().order_by('id')[:4]
    products_newist = Product.objects.all().order_by('-id')[:4]
    products_pick = Product.objects.all().order_by('?')[:4]
    page = "home"
    context = {'setting': setting,
               'page': page,
               'products_slider': products_slider,
               'category': category,
               'products_newist': products_newist,
               'category': category,
               'products_pick': products_pick}
    return render(request, 'index.html', context)


def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactF()  # create relation with model
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    form = ContactForm
    category = Category.objects.all()
    context = {'setting': setting, 'form': form, 'category': category}
    return render(request, 'contact.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'category': category}
    return render(request, 'about.html', context)


def category_products(request, id, slug):
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    context = {
        'category': category,
        'products': products,
    }
    return render(request,'category_products.html',context)


def search(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    if request.method == 'POST':
        form = searchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query)  #key sinstive SELECT * FROM product WHERE title LIKE '%query%'
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid)

            category = Category.objects.all()
            context = {'products': products,'query':query,
                       'category': category }
            return render(request, 'search_products.html', context)
    return HttpResponseRedirect('/')





def auto_search(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    products = Product.objects.filter(title__icontains=q)
    results = []
    for rs in products:
      product_json = {}
      product_json = rs.title
      results.append(product_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def product_detail(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = comment.objects.filter(product_id=id,status='True')
    context = {
        'category': category,
        'product': product,
        'images': images,
        'comments': comments,
        'setting': setting,
    }
    return render(request,'product_detail.html',context)
