import pyimgur
import os

##############
# import keys
##############
os.chdir(os.path.expanduser("~/Documents/github/messenger_chat_bot"))
#id
with open("imgur/keys/client_id.txt", "r") as f:
    client_id = f.read()
#secret
with open("imgur/keys/client_secret.txt", "r") as f:
    client_secret = f.read()
#clean up
client_id     = client_id.strip()
client_secret = client_secret.strip()
#----------------------------------------------------------------------

##############
# get image info by id
##############
im    = pyimgur.Imgur(client_id)
image = im.get_image('S1jmapR')
print(image.title) # Cat Ying & Yang
print(image.link) # http://imgur.com/S1jmapR.jpg
#----------------------------------------------------------------------

##############
# upload image
##############
image_file_path = "A Filepath to an image on your computer"

im = pyimgur.Imgur(client_id)
uploaded_image = im.upload_image(PATH, title="Uploaded with PyImgur")
print(uploaded_image.title)
print(uploaded_image.link)
print(uploaded_image.size)
print(uploaded_image.type)
#----------------------------------------------------------------------
