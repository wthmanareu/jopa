from PIL import Image, ImageDraw


def board(board, name):
    imgToCopy = Image.open("static/img/start filed/startfiled.png")
    new_image = imgToCopy.copy()
    draw = ImageDraw.Draw(new_image)
    x, y = 61, 41
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 1:
                draw.rectangle([i * 38 + x, j * 38 + y, i * 38 + 38 + x - 1, j * 38 + 38 + y - 1], fill="black")
            if board[i][j] == 2:
                draw.rectangle([i * 38 + x, j * 38 + y, i * 38 + 38 + x - 1, j * 38 + 38 + y - 1], fill="gray")
            if board[i][j] == 3:
                draw.rectangle([i * 38 + x, j * 38 + y, i * 38 + 38 + x - 1, j * 38 + 38 + y - 1], fill="red")
            y += 2
        x += 2
        y = 41
    new_image.save(f'static/img/imagesForShipGame/{name}.png', "PNG")
    return f'static/img/imagesForShipGame/{name}.png'