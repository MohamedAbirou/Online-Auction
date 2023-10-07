from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.contrib import messages
from .forms import AddListingForm

from .models import *


def index(request):
    active_listings = Listing.objects.filter(is_active=True)[:8]
    closed_listings = Listing.objects.filter(is_active=False)[:8]
    watchlist = []
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        watchlist = profile.watchlist.all()

    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
        "closed_listings": closed_listings,
        "watchlist": watchlist
    })

def about(request):
    return render(request, 'auctions/about.html')

def contact(request):
    return render(request, 'auctions/contact.html')

def profile(request):
    watchlist = []
    if request.user.is_authenticated:
        user_listings = Listing.objects.filter(user=request.user)
        profile, created = Profile.objects.get_or_create(user=request.user)
        watchlist = profile.watchlist.all()
        
    paginator = Paginator(user_listings, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
        
    return render(request, "auctions/profile.html", {
        "profile": profile,
        "watchlist": watchlist,
        "user_listings": page_obj
    })


@login_required
def watchlist(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    watchlist = profile.watchlist.all()

    paginator = Paginator(watchlist, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "auctions/watchlist.html", {
        "watchlist": page_obj,
        "profile": profile,
    })

@login_required
def delete_from_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    profile, _= Profile.objects.get_or_create(user=request.user)

    if listing in profile.watchlist.all():
        profile.watchlist.remove(listing) 

    return redirect("watchlist")


def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.user == listing.user:
        listing.delete()

    return redirect("profile")



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return redirect("index")


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
        return redirect("index")
    else:
        return render(request, "auctions/register.html")


def listings(request, category=None):
    categories = Category.objects.all()
    listings = Listing.objects.filter(is_active=True)
    watchlist = []
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        watchlist = profile.watchlist.all()

    if category:
        request.session['category'] = category
        category_obj = get_object_or_404(Category, name=category)
        listings = listings.filter(category=category_obj)

    paginator = Paginator(listings, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not listings:
        return render(request, "auctions/listings.html", {
            "message": "Products not found!",
            "categories": categories
        })

    return render(request, "auctions/listings.html", {
        "listings": page_obj,
        "categories": categories,
        "watchlist": watchlist
    })


def listing_detail(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comments = Comment.objects.filter(listing=listing)
    bids = Bid.objects.filter(listing=listing)
    active_listings = Listing.objects.filter(is_active=True)[:4]
    watchlist = []
    if request.user.is_authenticated:
        profile, created = Profile.objects.get_or_create(user=request.user)
        watchlist = profile.watchlist.all()

    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "active_listings": active_listings,
        "comments": comments,
        "user": request.user,
        "bids": bids,
        "watchlist": watchlist
    })



@login_required
def add_comment(request, listing_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            listing = Listing.objects.get(id=listing_id)
            comment_text = request.POST['comment_text']

            if user and listing and comment_text:
                comment = Comment(user=user, listing=listing, comment_text=comment_text)
                comment.save()

            return redirect('listing_detail', listing_id=listing.id)
        else:
            return redirect('login_view')
    

@login_required
def add_listing(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    watchlist = profile.watchlist.all()
    if request.method == 'POST':
        form = AddListingForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_url = form.cleaned_data['image_url']
            if image and image_url:
                form.add_error(None, "Please only provide either an image file or an image URL, not both.")
            else:
                listing = form.save(commit=False)
                listing.user = request.user
                listing.save()
                return redirect('index')
    else:
            form = AddListingForm()
    
    return render(request, 'auctions/add_listing.html', {
        "form": form,
        "watchlist": watchlist
    })
    
@login_required
def add_to_watchlist(request, listing_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            listing = Listing.objects.get(id=listing_id)

            if user and listing:
                profile, created = Profile.objects.get_or_create(user=user)
                profile.watchlist.add(listing)

            return redirect('listing_detail', listing_id=listing.id)
        else:
            return redirect('login_view')
        
@login_required
def place_bid(request, listing_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            listing = Listing.objects.get(id=listing_id)

            if not listing.is_active:
                messages.error(request, "This auction is already closed.")
                return redirect('listing_detail', listing_id=listing.id)

            bid_amount = float(request.POST['bid_amount'])

            bids = Bid.objects.filter(listing=listing)
            highest_bid = None
            for bid in bids:
                if highest_bid is None or bid.bid_amount > highest_bid:
                    highest_bid = bid.bid_amount

            if user and listing and bid_amount:
                if highest_bid is None or bid_amount > highest_bid:
                    bid = Bid(user=user, listing=listing, bid_amount=bid_amount)
                    bid.save()
                    messages.success(request, 'Your bid has been placed successfully.')
                    listing.current_bid = bid_amount
                    listing.winner = user
                    listing.save(update_fields=['current_bid', 'winner'])
                else:
                    messages.error(request, 'Your bid must be higher than the current bid.')
                    return redirect('listing_detail', listing_id=listing.id)

            return redirect('listing_detail', listing_id=listing.id)
        else:
            return redirect('login_view')



@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    # Check if the current user is the creator of the listing
    if request.user != listing.user:
        messages.error(request, "You are not authorized to close this auction.")
        return redirect('listing_detail', listing_id=listing.id)

    # Check if the listing is still active
    if not listing.is_active:
        messages.error(request, "This auction is already closed.")
        return redirect('listing_detail', listing_id=listing.id)

    # Close the auction and set the winner
    listing.is_active = False
    highest_bid = listing.bids.order_by('-bid_amount').first()
    if highest_bid:
        listing.winner = highest_bid.user
    else:
        messages.warning(request, "No bids were placed on this auction.")
    listing.save()

    messages.success(request, "The auction has been closed successfully.")
    return redirect('listing_detail', listing_id=listing.id)