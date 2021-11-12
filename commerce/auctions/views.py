from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.core.validators import ValidationError
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *


def index(request):
    # Query the Active listing DB for all active listing
    listings = AuctionListings.objects.all()
    
    return render(request, "auctions/index.html", {
        'listings': listings
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
            # Add Flash message 
            messages.success(request, f'Welcome {user}!')
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    # Add Flash message 
    messages.success(request, f'You have been logged out!')
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
        # Add Flash message 
        messages.success(request, f'Welcome {user}!')
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

# view to create listing
@login_required
def create_listing(request):
    form = CreateListingForm()
    
    # to create and save a new listing
    if request.method == 'POST':

        # ensure user is authenticated
        if request.user.is_authenticated:

            # GEt what the user has filled in the form
            listing = CreateListingForm(request.POST, request.FILES)

            # Check if form is valid
            if listing.is_valid():
                # save to database
                obj = listing.save(commit=False)
                # obj.item_image
                obj.user = request.user
                obj.save()

                # Add Flash message 
                messages.success(request, f'You have created {obj.item_name} successfully!')
                
                # after submission redirect to the home page
                return HttpResponseRedirect(reverse("index"))
    
    return render (request, 'auctions/create.html', {
        'form': form
    })



# watchlist view function
@login_required
def watchlist(request, name):
    # get the original bid price and item id of the item
    listing = AuctionListings.objects.get(item_name=name)

    
    if request.method == 'POST':

        # ensure user is authenticaed
        if request.user.is_authenticated:
            all_watchlists = []
            # query watchlist for added watchlist
            watchlists = Watchlist.objects.filter( user=request.user)
            for w in watchlists:
                all_watchlists.append(w.item_name.item_name)


            # if database is not empty
            if name not in all_watchlists:
                # add item to the watchlist
                add_watchlist = Watchlist(item_name=listing, is_added=True, user=request.user)
                # save to database
                add_watchlist.save()
                # flash message
                messages.success(request, f'You have added {name} to your watchlist!')
                # redirect to home page
                return HttpResponseRedirect(reverse("index"))
            else:
                
                return render(request, 'auctions/watchlist.html', {
                    'message': f'{name} has already been added to your watch list',
                    'name': name
                })   


                
@login_required
def remove_watchlist(request, name):

    # get the original bid price and item id of the item
    listing = AuctionListings.objects.get(item_name=name)

    # query watchlist for added watchlist
    watchlists = Watchlist.objects.get(item_name=listing, user=request.user)
    watchlists.is_added = False
    watchlists.delete()

    # Flash message
    messages.success(request, f'You have removed {name} from your watchlist!')

    # redirect to home page
    return HttpResponseRedirect(reverse("index"))

    
        
    
            

# bid view function
@login_required
def bid(request, name):
    # form = BidForm()

    # get the original bid price and item id of the item
    listing = AuctionListings.objects.get(item_name=name)
    listing_bid = listing.item_price
    item_id = listing.id
    

    # get the list of bidded price on the particular item
    
    # create an empty list
    list_of_user_bids = []

    # Query db for all the bids on the particular item
    bid_priced = Bids.objects.filter(item_name=item_id)

    # iterate through it to get the bids
    for bid in bid_priced:
        # add it to the empty list
        list_of_user_bids.append(bid.item_bid)


    if request.method == 'POST':

        # ensure user is signed in
        if request.user.is_authenticated:

            form = BidForm(request.POST)

            # get the bid price of user
            if form.is_valid():
                # user's bid input'
                bid = form.cleaned_data['item_bid']
            
                # check if bid is greater than or equal to starting bid
                if  bid >= listing_bid and bid > max(list_of_user_bids, default=0):
                    # save to database
                    obj = form.save(commit=False)
                    obj.item_name = listing
                    obj.user = request.user
                    obj.save()
                    # flash message
                    messages.success(request, f'You have bidded ${bid} on {name} successfully!')

                    # after submission redirect to the home page
                    return HttpResponseRedirect(reverse("index"))

                # else show a form error
                else:
                    if max(list_of_user_bids, default=0) == 0:
                         messages.warning(request, f'Your bid ${bid} has to be higher than ${listing_bid}!')
                    else:
                        # flash message
                        messages.warning(request, f'Your bid ${bid} has to be higher than ${listing_bid} and ${max(list_of_user_bids, default=0)}!')
                        # ValidationError(('Invalid value'), code='invalid')
                        form = BidForm()
                        print(form.errors)


    return render(request, 'auctions/bid.html', {
        'form': BidForm(),
        'name': name,
        'listing_bid': listing_bid,
        'highest_bid': max(list_of_user_bids, default=0)
    })


@login_required
def close_auction(request, name):
    
    if request.user.is_authenticated:
        # get highest bidder

        # get the item to close
        # item = AuctionListings.objects.get(item_name=name)
        item = AuctionListings.objects.get(item_name=name)
        
        # create an empty list for the bids made
        list_of_user_bids = []

        # create empty list for users who have bidded
        potential_winner = []

        # Query db for all the bids on the particular item
        bid_priced = Bids.objects.filter(item_name=item.id)

        # iterate through it to get the bids
        for bid in bid_priced:
          
            # add  to the potentital winner's list
            potential_winner.append(bid.item_name)
            # add it to the empty list
            list_of_user_bids.append(bid.item_bid)


        # the amount that won the bid
        winning_bid = max(list_of_user_bids, default=0)

        # check if there are no bids and no potential winner
        if potential_winner != []:
            # winner is the last person on the potential winner's list
            winner = potential_winner[-1]

        
        # set is_active to false
        item.is_active = False
        # save to database
        item.save()

        if winning_bid == 0:
            messages.success(request, f'No one has bidded on this listing!')
        else:
            # flash message
            messages.success(request, f'Auction Closed!!! Winner is {winner} with ${winning_bid}!')

        # reddirect to homepage
        return HttpResponseRedirect(reverse("index"))



# Listing and comment page view function
@login_required
def listing_page(request, name):

    # get the original bid price and item id of the item
    listing = AuctionListings.objects.get(item_name=name)

    # get the comments on a particular item from the db
    user_comments = Comments.objects.filter(item_name=listing.id)


    if request.method == 'POST':

        if request.user.is_authenticated:
            # get the user input (comment)
            form = CommentForm(request.POST)

            # validate the form
            if form.is_valid():
                comment = form.cleaned_data['item_comment']

                # save comment in db
                obj = form.save(commit=False)
                obj.item_name = listing
                obj.item_comment = comment
                obj.user = request.user
                obj.save()

                messages.success(request, f'Comment added successfully!')

                # after submission redirect to the listing page
                return render (request, 'auctions/listing_page.html', {
                    'listing': listing,
                    'form': CommentForm(),
                    'comments': user_comments,
                })

    return render (request, 'auctions/listing_page.html', {
        'listing': listing,
        'form': CommentForm(),
        'comments': user_comments,
    })

# The watchlist page
@login_required
def watchlist_page(request):
  
    # create a list of users who has added a watchlist  
    creator = []

    # query database for all the watchlist
    all_watchlist = Watchlist.objects.filter()

    for user in all_watchlist:
        if user.user not in creator:
            creator.append(user.user)    


    return render(request, "auctions/watchlist.html", {
        'users': creator,
        'watchlist': all_watchlist
    })


# The watchlist page
@login_required
def category(request):

    categories = []
    # get all the categories in the Auctions
    all_categories = AuctionListings.objects.all()
    
    for listing in all_categories:

        # if category does not exist add, otherwise don't add
        if listing.category not in categories:
            categories.append(listing.category)
            

    return render(request, "auctions/category.html", {
        'categories': categories,
    })


@login_required
def category_list(request, name):

    # get all the categories in the Auctions
    category_item = AuctionListings.objects.filter(category=name, is_active=True)
    print('CAT:', category_item)
    

    return render(request, "auctions/cat_item.html", {
        'caegory_item': category_item
    })
    
    
    

