import requests
from os import getenv


def create_post_on_fb(path_to_picture, message_for_posting):
    access_token = getenv('ACCESS_TOKEN_FOR_FB')
    fb_group_id = getenv('FB_GROUP_ID')
    url = 'https://graph.facebook.com/{}/photos'.format(fb_group_id)

    data = {
        'access_token': access_token,
        'caption': message_for_posting,
    }
    with open(path_to_picture, 'rb') as picture:
        files = {'photo': picture}
        requests.post(url, data=data, files=files)




