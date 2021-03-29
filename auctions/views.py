from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User
from .models import Listing
from .models import Category
from .models import Bids
from .models import Comments
import re


def index(request):
    user_watch = None
    category = ""
    listing = Listing.objects.all
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            listing = Listing.objects.filter(category=category)
        elif request.POST.get("category") == "null":
            category = request.POST.get("category")
            listing = Listing.objects.filter(category__isnull=True) 

        if request.user.is_authenticated:
            if request.POST.get("removeWatchlist") or request.POST.get("addWatchlist") : 
                item = request.POST["item_id"]
                search_user_id = User.objects.get(id=request.user.id)

                if_exist = True
                try:
                    search_item = search_user_id.watchlist.get(id=item)
                except:
                    if_exist = False

                if if_exist:
                    search_user_id.watchlist.remove(item)
                else:
                    search_user_id.watchlist.add(item)
                    
            elif request.POST.get("closeBid"):
                item = request.POST["item_id"]
                search_item = Listing.objects.get(pk=item)
                search_item.closeChecker = True
                search_item.save()
        else:
            if not request.POST.get("search"):
                return render(request, "auctions/login.html")

    if request.user.is_authenticated:
        user_watch = User.objects.get(pk=int(request.user.id)).watchlist.all()
    
    search_item = Category.objects.all()
    return render(request, "auctions/index.html", {
        "list": listing,
        "watchlist": user_watch,
        "categories": search_item,
        "ctgry": category
    })

def allList(request):
    user_watch = None
    category = ""
    listing = Listing.objects.all
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data["category"]
            listing = Listing.objects.filter(category=category)
        elif request.POST.get("category") == "null":
            category = request.POST.get("category")
            listing = Listing.objects.filter(category__isnull=True) 
            
        if request.user.is_authenticated:
            if request.POST.get("removeWatchlist") or request.POST.get("addWatchlist") : 
                item = request.POST["item_id"]
                search_user_id = User.objects.get(id=request.user.id)

                if_exist = True
                try:
                    search_item = search_user_id.watchlist.get(id=item)
                except:
                    if_exist = False

                if if_exist:
                    search_user_id.watchlist.remove(item)
                else:
                    search_user_id.watchlist.add(item)
            elif request.POST.get("closeBid"):
                item = request.POST["item_id"]
                search_item = Listing.objects.get(pk=item)
                search_item.closeChecker = True
                search_item.save()
        else:
            if not request.POST.get("search"):
                return render(request, "auctions/login.html")

    if request.user.is_authenticated:
        user_watch = User.objects.get(pk=int(request.user.id)).watchlist.all()

    search_item = Category.objects.all()
    return render(request, "auctions/allList.html", {
        "list": listing,
        "watchlist": user_watch,
        "categories": search_item,
        "ctgry": category
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    messageList = []
    if request.method == "POST":
        error = False
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]

        if username == "" or username == None:
            messageList.append("Please input username.")
            error = True

        if firstname == "" or firstname == None:
            messageList.append("Please input firstname.")
            error = True

        if lastname == "" or lastname == None:
            messageList.append("Please input lastname.")
            error = True

        if password == "" or password == None:
            messageList.append("Please input password.")
            error = True

        if password != confirmation:
            messageList.append("Passwords must match.")
            error = True

        if error:
            return render(request, "auctions/register.html", {
                "username" : username,
                "firstname": firstname,
                "email": email,
                "lastname": lastname,
                "message": messageList
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def item(request, item):
    user_watch = None
    message = None
    bidAmount = 0
    if request.method == "POST":
        if request.user.is_authenticated:
            if request.POST.get("removeWatchlist") or request.POST.get("addWatchlist") : 
                item = request.POST["item_id"]
                search_user_id = User.objects.get(id=request.user.id)

                if_exist = True
                try:
                    search_item = search_user_id.watchlist.get(id=item)
                except:
                    if_exist = False

                if if_exist:
                    search_user_id.watchlist.remove(item)
                else:
                    search_user_id.watchlist.add(item)

            elif request.POST.get("placeBid"):
                bidAmount = request.POST["price"]
                getBid = Bids.objects.filter(listingId=item).first()
                search_item = Listing.objects.get(pk=item)
                
                if bidAmount == "" or bidAmount == None:
                    message = {"messageCode": "1001", "message": "Please input amount."}
                elif re.findall("\W", bidAmount):
                    message = {"messageCode": "1001", "message": "Please input correct numeric value."}
                elif re.findall("[a-zA-Z]", bidAmount):
                    message = {"messageCode": "1001", "message": "Please input numeric value."}
                elif int(bidAmount) == 0 :
                    message = {"messageCode": "1001", "message": "Please input amount more than 0."}
                elif int(bidAmount) > 9999999:
                    message = {"messageCode": "1001", "message": "Please input amount less than ¥9,999,999."}
                elif getBid == None:
                    if int(bidAmount) <= search_item.price :
                        message = {"messageCode": "1001", "message": "Please input amount more than starting price."}
                elif int(bidAmount) <= getBid.amount :
                    message = {"messageCode": "1001", "message": "Please input amount more than current price."}

                if message == None :
                    bids = Bids()
                    bids.listingId_id = item
                    bids.amount = bidAmount
                    bids.bidder_id = request.user.id
                    bids.save()
                    message = {"messageCode": "2001", "message": "Successfully add bid."}

            elif request.POST.get("comment"):
                comment = Comments()
                comment.commentListingId_id = item
                comment.commentTitle = request.POST["commentTitle"]
                comment.commentDescription = request.POST["commentDescription"]
                comment.commentUser_id = request.user.id
                comment.save()
            elif request.POST.get("closeBid"):
                search_item = Listing.objects.get(pk=item)
                search_item.closeChecker = True
                search_item.save()
        else:
            if not request.POST.get("view"):
                return render(request, "auctions/login.html")

    getBid = Bids.objects.filter(listingId=item).first()
    search_item = Listing.objects.get(pk=item)
    commentList = Comments.objects.filter(commentListingId=item)

    if request.user.is_authenticated:
        user_watch = User.objects.get(pk=int(request.user.id)).watchlist.all()

    if getBid == None:
        getBid = None   

    return render(request, "auctions/item.html", {
        "item": search_item,
        "bid": getBid,
        "commentList": commentList,
        "watchlist": user_watch,
        "message": message,
        "bidAmount": bidAmount
    })

def watchlist(request):
    if request.method == "POST":
        item = request.POST["item_id"]
        search_user_id = User.objects.get(id=request.user.id)
        search_user_id.watchlist.remove(item)

    search_item = Listing.objects.filter(user_watch=request.user.id)
    return render(request, "auctions/watchlist.html", {
        "list": search_item
    })
def listing(request):
    search_item = Listing.objects.filter(name__id=request.user.id)
    return render(request, "auctions/listing.html", {
        "list": search_item
    })

class NewTaskForm(forms.Form):
    category = forms.IntegerField(label="Category ID")

def create(request):
    messageList = []
    title = ""
    category = ""
    price = 0
    description = ""
    img = ""

    if request.method == "POST":
        if request.user.is_authenticated:
            error = False
            form = NewTaskForm(request.POST)
            title = request.POST["title"]
            price = request.POST["price"]
            description = request.POST["description"]
            img = request.POST["image"]

            if form.is_valid():
                category = form.cleaned_data["category"]

            if title == "" or title == None:
                messageList.append("Please input title.")
                error = True
            elif len(title) > 64:
                messageList.append("Please input title maximum of 64 characters.")
                error = True

            if price == "" or price == None:
                messageList.append("Please input amount.")
                error = True
            elif re.findall("\W", price):
                messageList.append("Please input correct numeric value.")
                error = True
            elif re.findall("[a-zA-Z]", price):
                messageList.append("Please input numeric value.")
                error = True
            elif int(price) == 0 :
                messageList.append("Please input amount more than 0.")
                error = True
            elif int(price) > 9999999:
                messageList.append("Please input amount less than ¥9,999,999.")
                error = True

            if description == "" or description == None:
                messageList.append("Please input description.")
                error = True
            elif len(description) > 900:
                messageList.append("Please input description maximum of 900 characters.")
                error = True


            if not error:
                listing = Listing()
                listing.title = title
                listing.category_id = category
                listing.price = price
                listing.description = description
                listing.image = img
                listing.closeChecker = False
                listing.name_id = request.user.id
                listing.save()

                return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html")

    search_item = Category.objects.all()
    return render(request, "auctions/create.html", {
        "categories": search_item,
        "message": messageList,
        "title": title,
        "ctgry": category,
        "price": price,
        "description": description,
        "img": img
    })

def category(request):
    if request.method == "POST":
        category = Category()
        category.title = request.POST["category"]
        category.save()

        return HttpResponseRedirect(reverse("index"))

    search_item = Category.objects.all()
    return render(request, "auctions/category.html", {
        "categories": search_item
    })