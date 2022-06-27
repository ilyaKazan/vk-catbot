import vk_api, requests
from random import randint
from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType, VkLongpollMode

vk = vk_api.VkApi(token='YOUR_TOKEN_HERE')
vk._auth_token()

sessionLongPoll = VkLongPoll(vk, mode=VkLongpollMode.GET_ATTACHMENTS)
upload = VkUpload(vk)


def download_image(url, file_name):
    img_response = requests.get(url)
    file = open(file_name, "wb")
    file.write(img_response.content)
    file.close()


def upload_image(url, name, peer_id):
    download_image(url, name)
    photo = upload.photo_messages(name), peer_id)
    return photo


def get_cat(peer_id):
    photo = upload_image("http://thiscatdoesnotexist.com", "cat.jpg", peer_id)
    return vk.method("messages.send", {"peer_id": peer_id, "attachment": "photo{}_{}".format(
        photo[0]['owner_id'], photo[0]['id']), "random_id": randint(0, 20000000)})


def get_person(peer_id):
    photo = upload_image("https://thispersondoesnotexist.com/image", "person.jpg", peer_id)
    return vk.method("messages.send", {"peer_id": peer_id, "attachment": "photo{}_{}".format(
        photo[0]['owner_id'], photo[0]['id']), "random_id": randint(0, 20000000)})


commands = {
    "кот": get_cat,
    "чел": get_person,
}

while True:
    for event in sessionLongPoll.listen():
        if (event.type == VkEventType.MESSAGE_NEW) and (not event.from_me):
            msg = vk.method("messages.getById", values={"message_ids": [event.message_id]})["items"][0]
            text = msg["text"].lower()

            if text in commands:
                commands[text](event.peer_id)
