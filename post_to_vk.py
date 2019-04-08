import vk_api
from os import getenv


def create_post_on_vk(path_to_picture, message_for_posting):
    login_for_vk = getenv('LOGIN_FOR_VK')
    password_for_vk = getenv('PASSWORD_FOR_VK')
    vk_group_id = getenv('VK_GROUP_ID')
    vk_album_id = getenv('VK_ALBUM_ID')
    vk_session = vk_api.VkApi(login_for_vk, password_for_vk)
    vk_session.auth()
    vk = vk_session.get_api()

    upload = vk_api.VkUpload(vk_session)
    photo = upload.photo(
        path_to_picture,
        album_id=vk_album_id,
        group_id=vk_group_id
    )
    vk.wall.post(
            message=message_for_posting,
            from_group=1,
            owner_id=photo[0]['owner_id'],
            attachments='photo{}_{}'.format(
            photo[0]['owner_id'], photo[0]['id'])
    )
