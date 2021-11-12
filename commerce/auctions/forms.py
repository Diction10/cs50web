from django import forms
from .models import *
from django.forms import ModelForm


class CreateListingForm(ModelForm):
    class Meta:
        model = AuctionListings
        # fields = '__all__'
        # exclude = ['date_created']
        fields = ['item_name', 'item_description', 'item_price', 'item_image', 'item_url', 'category']

        # Override the name of the field
        labels = {
            'item_name': ('Title'),
            'item_description': ('Description'),
            'item_price': ('Starting Bid'),
            'item_image': ('Image'),
            'item_url': ('Url'),
            'category': ('Category'),
        }


class BidForm(ModelForm):
    class Meta:
        model = Bids
        fields = ['item_bid']

        # Override the name of the field
        labels = {
            'item_bid': ('Bid')
        }



class CommentForm(ModelForm):
    class Meta:
        model = Comments
        # fields = '__all__'
        # exclude = ['date_created']
        fields = ['item_comment']

        # Override the name of the field
        labels = {
            'item_comment': ('Comment')
        }