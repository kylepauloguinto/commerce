from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .models import Listing
from .models import Category
from .models import Bids
from .models import Comments


def index(request):
    if request.method == "POST":
        if request.user.id != None:
            item = request.POST["item_id"]
            search_item = Listing(pk=item)
            if_exist = True
            try:
                search_user_id = search_item.user.get(id=request.user.id)
            except:
                if_exist = False

            if if_exist:
                search_item.user.remove(request.user.id)
            else:
                search_item.user.add(request.user.id)
        else:
            return render(request, "auctions/login.html")
    
    return render(request, "auctions/index.html", {
        "list": Listing.objects.all
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
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
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
    if request.method == "POST":
        if request.POST.get("placeBid"):
            bids = Bids()
            bids.listingId_id = item
            bids.amount = request.POST["price"]
            bids.bidder_id = request.user.id
            bids.save()
        elif request.POST.get("comment"):
            comment = Comments()
            comment.commentListingId_id = item
            comment.commentTitle = request.POST["commentTitle"]
            comment.commentDescription = request.POST["commentDescription"]
            comment.commentUser_id = request.user.id
            comment.save()


    getBid = Bids.objects.filter(listingId=item).first()
    search_item = Listing.objects.get(pk=item)
    commentList = Comments.objects.filter(commentListingId=item)

    if getBid == None:
        getBid = search_item.price
    else:
        getBid = getBid.amount

    return render(request, "auctions/item.html", {
        "item": search_item,
        "bidAmount": getBid,
        "commentList": commentList
    })

def watchlist(request):
    if request.method == "POST":
        item = request.POST["item_id"]
        search_item = Listing(pk=item)
        search_item.user.remove(request.user.id)


    search_item = Listing.objects.filter(user__id=request.user.id)
    return render(request, "auctions/watchlist.html", {
        "list": search_item
    })
def listing(request):
    search_item = Listing.objects.filter(name__id=request.user.id)
    return render(request, "auctions/listing.html", {
        "list": search_item
    })

def create(request):
    if request.method == "POST":
        listing = Listing()
        listing.title = request.POST["title"]
        listing.category_id = request.POST["category"]
        listing.price = request.POST["price"]
        listing.description = request.POST["description"]
        listing.image = request.POST["image"]
        listing.closeChecker = False
        listing.name_id = request.user.id
        listing.save()

        return HttpResponseRedirect(reverse("index"))

    search_item = Category.objects.all()
    return render(request, "auctions/create.html", {
        "categories": search_item
    })