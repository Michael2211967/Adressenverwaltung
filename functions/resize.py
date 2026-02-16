def resize_picture(width, height, wish_width=400):
        wish_height = wish_width * height // width
        return (wish_width, wish_height)
