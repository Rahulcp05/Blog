from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.core.mail import EmailMessage

from inventory.models import Item
from .forms import MyRegistrationForm, CommentForm, EditProfileForm,ItemForm


def index(request):
    items_list = Item.objects.all()
    #using pagination
    query = request.GET.get("s")
    if query:
        items_list=items_list.filter(title__icontains = query)
    paginator = Paginator(items_list, 10) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)

    return render(request, 'inventory/index.html', {'items': items, 'id': id})


def item_detail(request, id):
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        raise Http404("Item doesnt exist")
    if request.method == "POST":
        f = CommentForm(request.POST)
        if f.is_valid():
            c = f.save(commit=False)
            c.pub_date = timezone.now()
            c.name = request.user
            c.itemz = item
            c.save()
            return HttpResponseRedirect('/item/%s/' % id)

    else:
        f = CommentForm()
    args = {}
    args.update(csrf(request))
    args['itemz'] = item
    args['form'] = f
    args['user'] = request.user
    args['id'] = id
    args['item'] = item

    return render(request, 'inventory/item_detail.html',args)


def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/accounts/invalid')


def loggedin(request):
    return render_to_response('loggedin.html', {'full_name:request.user.username'})


def invalid_login(request):
    return render_to_response("invalid_login.html")


def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')


def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST,request=request)
        if form.is_valid():
            # form.save()
            save_it= form.save()
            email = save_it.email
            send_email(request, email)
            return HttpResponseRedirect('/accounts/register_check')

    args = {}
    args.update(csrf(request))
    args['form'] = MyRegistrationForm()
    return render_to_response('register.html', args)

def send_email(request, email):
    msg = EmailMessage('Account verification',
                       'Click the below link to activate your account.\n 127.0.0.1:8000/accounts/register_verification/ ', to=[email])
    msg.send()

# def send_email(request, email):
#     msg = EmailMessage('Account verification',
#                        'Click the below link to activate your account.\n mighty-reef-46503.herokuapp.com/accounts/register_verification/ ', to=[email])
#     msg.send()


def register_check(request):
    return render_to_response('register_check.html',{'user': request.user})

def register_verification(request):
    return render_to_response('account_verified.html')


def add_comment(request, id):
    a = Item.objects.get(id=id)

    if request.method == "POST":
        f = CommentForm(request.POST)
        if f.is_valid():
            c = f.save(commit=False)
            c.pub_date = timezone.now()
            c.name = request.user
            c.itemz = a
            c.save()
            return HttpResponseRedirect('/item/%s/' % id)

    else:
        f = CommentForm()
    args = {}
    args.update(csrf(request))
    args['itemz'] = a
    args['form'] = f
    args['user'] = request.user
    args['id'] = id
    return render_to_response("add_comment.html", args)


def profile(request):
    a = request.user
    c = {}
    c['user'] = a
    c['name'] = a.username
    c['email'] = a.email
    c['firstname'] = a.first_name
    c['lastname'] = a.last_name
    return render_to_response('profile.html', c)


def edit_profile(request):
    user = request.user
    form = EditProfileForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            return HttpResponseRedirect('/profile/')
    d = {}
    d['form'] = EditProfileForm()
    return render(request, "edit_profile.html", d)

def create(request):
    if request.POST:
        form = ItemForm(request.POST , request.FILES or None)
        if form.is_valid():
            # form.save()
            f=form.save(commit=False)
            f.author = request.user
            f.save()
            return HttpResponseRedirect('/')
    else:
        form = ItemForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    # if request.user.is_authenticated():
    args['user'] = request.user
    return render_to_response('create_item.html', args)
