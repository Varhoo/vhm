# coding: utf-8
from django import forms
from models import*


class TicketForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Ticket
        fields = ('title', 'text', 'priority', 'status', 'group')


class TicketFormEdit(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TicketFormEdit, self).__init__(*args, **kwargs)

    class Meta:
        model = Ticket
        fields = ('priority', 'status')


class CommentForm(forms.Form):
    text = forms.CharField(label='Text', widget=forms.Textarea)
    is_public = forms.BooleanField(
        label='Public', required=False, initial=False)
    upload_file = forms.FileField(
        label='Příloha', required=False, initial=False)
    # class Meta:
    #    model = Comment
