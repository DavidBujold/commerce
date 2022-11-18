from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, Category, Listing, Bids, Comments
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
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

class create_form(forms.ModelForm):
    class Meta:
        model= Listing
        fields= ['title','image','description','category','price']

class bid_form(forms.ModelForm):
    class Meta:
        model= Bids
        fields= ['bid']

class comment_form(forms.ModelForm):
    class Meta:
        model= Comments
        fields= ['title', 'comment']

@login_required
def create(request):
    if request.method =='POST':
        form= create_form(request.POST)
        if form.is_valid():
            new_listing = form.save(commit=False)
            new_listing.user = request.user
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            form= create_form()    
    return render(request, "auctions/create.html",{
        "form": create_form()
    })

def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": bid_form(),
        "comment_form": comment_form(),
        "comments": Comments.objects.filter(listing = listing)

    })

@login_required
def bid(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == 'POST':
        form= bid_form(request.POST)
        if form.is_valid():
            new_bid = form.save(commit=False)
            new_bid.listing = listing
            new_bid.user = request.user
            new_bid.save()
            if new_bid.bid > listing.price and new_bid.bid > listing.current_bid:
                new_bid.listing.current_bid = new_bid.bid
                listing.save()
                return HttpResponseRedirect(reverse("listing", args={listing_id}))

            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "form": bid_form(),
                    "error": "Please place a bid higher than the asking price and the current bid"

    })
        else:
            form= bid_form()
    return HttpResponseRedirect(reverse("listing", args={listing_id}))

def comment(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.method == 'POST':
        comment= comment_form(request.POST)
        if comment.is_valid():
            new_comment = comment.save(commit=False)
            new_comment.listing = listing
            new_comment.user = request.user
            new_comment.save()
            return HttpResponseRedirect(reverse("listing", args={listing_id}))
    

def is_active(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    winner = Bids.objects.filter(listing = listing).first()
    if request.method == 'POST':
        listing.active = False
        listing.winner = winner.user
        listing.save()
        return HttpResponseRedirect(reverse("listing", args={listing_id}))

def watcher(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        watchlist = request.user.watchlist
        if listing in watchlist.all():
            watchlist.remove(listing)
        else:
            watchlist.add(listing)
    return HttpResponseRedirect(reverse("listing", args={listing_id}))

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all(),
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories" : Category.objects.all(),
    })

def category(request, name):
    category = Category.objects.get(name = name)
    listings = Listing.objects.filter(
        category = category,
        active = True   
    )

    return render(request, "auctions/category.html", {
        "listings" : listings,
        "title" : category.name

    })
