import os


def get_image_url(command):
    folder_path = "./images/"

    words = command.split()
    for file_name in os.listdir(folder_path):
        for word in words:
            if file_name.startswith(word) and file_name.endswith(".jpg"):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    return f"{file_path}"
                return "Image not found"


print(get_image_url("i need t_t_follower_2"))
