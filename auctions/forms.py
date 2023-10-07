from django import forms
from .models import Listing

class AddListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'current_bid', 'image_url', 'category', 'is_active']

    def __init__(self, *args, **kwargs):
        super(AddListingForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'title'
        self.fields['description'].widget.attrs['class'] = 'description'
        self.fields['starting_bid'].widget.attrs['class'] = 'starting-bid'
        self.fields['current_bid'].widget.attrs['class'] = 'current-bid'
        self.fields['image_url'].widget.attrs['class'] = 'image-url'
        self.fields['category'].widget.attrs['class'] = 'category'
        self.fields['is_active'].widget.attrs['class'] = 'is-active'