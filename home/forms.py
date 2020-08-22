from django import forms


class searchForm(forms.Form):
    query = forms.CharField(max_length=100)
    catid = forms.IntegerField()