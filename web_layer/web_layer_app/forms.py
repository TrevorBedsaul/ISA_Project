from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Username",'autofocus': 'autofocus','required': 'required'}),label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password",'required': 'required'}),label='')

class BookForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Title",'autofocus': 'autofocus','required': 'required'}),label='')
    ISBN = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"ISBN",'required': 'required'}),label='')
    author = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Author",'required': 'required'}),label='')
    price = forms.DecimalField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Price",'required': 'required'}),label='')
    year = forms.IntegerField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Year"}),label='')
    class_id = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Class ID"}),label='')
    edition = forms.IntegerField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Edition"}),label='')
    TYPE_CHOICES = (
        ("HC", "Hardcover"),
        ("PB", "Paperback"),
        ("LL", "Loose leaf"),
    )
    type_name = forms.ChoiceField(choices=TYPE_CHOICES, widget=forms.RadioSelect)

    CONDITION_CHOICES = (
        ("NW", "New"),
        ("UG", "Used, in good condition"),
        ("UB", "Used, in poor condition"),
    )
    condition = forms.ChoiceField(choices=CONDITION_CHOICES, widget=forms.RadioSelect)
