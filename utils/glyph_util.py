import png


def load_glyph_data_from_png(file_path):
    """
    从文件加载字形数据
    字形源文件为 PNG 图片，读取后进行二值化处理
    二值化仅使用颜色的 alpha 通道
    """
    width, height, bitmap, info = png.Reader(filename=file_path).read()
    glyph_data = []
    for bitmap_row in bitmap:
        glyph_data_row = []
        bitmap_row_len = len(bitmap_row)
        pixel_step = int(bitmap_row_len / width)
        for x in range(pixel_step - 1, bitmap_row_len, pixel_step):
            alpha = bitmap_row[x]
            if alpha > 127:
                glyph_data_row.append(1)
            else:
                glyph_data_row.append(0)
        glyph_data.append(glyph_data_row)
    return glyph_data, width, height


def save_glyph_data_to_png(glyph_data, file_path):
    """
    将字形数据保存到文件
    字形源文件为 PNG 图片，格式为 RGBA
    点阵位转换为不透明黑色，非点阵位转换为透明黑色
    """
    bitmap = []
    for glyph_data_row in glyph_data:
        bitmap_row = []
        for x in glyph_data_row:
            bitmap_row.append(0)
            bitmap_row.append(0)
            bitmap_row.append(0)
            if x == 0:
                bitmap_row.append(0)
            else:
                bitmap_row.append(255)
        bitmap.append(bitmap_row)
    image = png.from_array(bitmap, 'RGBA')
    image.save(file_path)
