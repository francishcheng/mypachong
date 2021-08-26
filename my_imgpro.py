from PIL import Image

def add_bgc(I):
    im = Image.open(I)

    fill_color = (0, 0, 64)  # your new background color

    im = im.convert("RGBA")  # it had mode P after DL it from OP
    if im.mode in ('RGBA', 'LA'):
        background = Image.new(im.mode[:-1], im.size, fill_color)
        background.paste(im, im.split()[-1])  # omit transparency
        im = background

    im.convert("RGB")
    return im