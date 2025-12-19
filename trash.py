from PIL import Image

def white_background_to_transparent_background(path):
    img = Image.open(path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for r, g, b, a in datas:
        # всё почти белое считаем фоном
        if r > 240 and g > 240 and b > 240:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append((r, g, b, a))

    img.putdata(new_data)
    img.save(path, "PNG")