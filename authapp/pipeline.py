from collections import OrderedDict
from urllib.parse import urlunparse, urlencode

import requests
from django.utils import timezone

from authapp.models import ShopUserProfile, ShopUser


def save_user_profile(backend, user, response, *args, **kwargs):
    """
    Функция, которая запускается когда, идет авторизация через социальную сеть
    """
    if backend.name != 'vk-oauth2':
        return
    '''https://api.vk.com/method/METHOD?PARAMS&access_token=TOKEN&v=V'''
    '''https://api.vk.com/method/users.get?user_ids=210700286&
    fields=bdate&access_token=533bacf01e11f55b536a565b57531ac114461ae8736d6506a3&v=5.131'''
    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join((
                              'bdate',
                              'sex',
                              'about',
                              'photo_100',
                          )),
                          access_token=response['access_token'],
                          v='5.131')),
                          None,
                          ))

    resp = requests.get(api_url)

    if resp.status_code != 200:
        return
    ''' получаем такой ответ
    {
  "response": [
    {
      "id": 210700286,
      "first_name": "Lindsey",
      "last_name": "Stirling",
      "bdate": "21.9.1986"
    }
  ]
}
    '''
    data = resp.json()['response'][0]
    if data['sex']:
        user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 \
            else ShopUserProfile.FEMALE

    if data['about']:
        user.shopuserprofile.about_me = data['about']


    user.save()