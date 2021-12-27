from django.contrib.auth.forms import AuthenticationForm

from authapp.models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self):
        super(ShopUserLoginForm, self).__init__()
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        