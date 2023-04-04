import logging
import math
import os

from PIL import ImageFont, Image, ImageDraw
from fontTools.ttLib import TTFont

import configs
from configs import path_define
from utils import fs_util, glyph_util, gb2312_util

logger = logging.getLogger('main')


def dump_font(output_name, font_file_path, font_size, canvas_height, offset_xy, need_alphabet=None):
    """
    :param output_name: 输出文件夹名称
    :param font_file_path: 字体文件路径
    :param font_size: 字体尺寸
    :param canvas_height: 画布高度
    :param offset_xy: 偏移坐标
    :param need_alphabet: 需要的字母表字迹
    """
    dump_dir = os.path.join(path_define.outputs_dir, output_name)
    fs_util.make_dirs_if_not_exists(dump_dir)

    font = TTFont(font_file_path)
    image_font = ImageFont.truetype(font_file_path, font_size)

    cmap = font.getBestCmap()
    units_per_em = font['head'].unitsPerEm
    hhea = font['hhea']
    metrics = font['hmtx'].metrics

    alphabet = set()
    for code_point in cmap.keys():
        alphabet.add(chr(code_point))
    alphabet = list(alphabet)
    alphabet.sort()
    alphabet_file_path = os.path.join(dump_dir, 'alphabet.txt')
    with open(alphabet_file_path, 'w', encoding='utf-8') as file:
        file.write(''.join(alphabet))
    logger.info(f'make {alphabet_file_path}')

    for code_point, glyph_name in cmap.items():
        c = chr(code_point)

        if need_alphabet is not None:
            if c not in alphabet:
                continue

        uni_hex_name = f'{code_point:04X}'
        unicode_block = configs.unidata_db.get_block_by_code_point(code_point)
        block_dir_name = f'{unicode_block.begin:04X}-{unicode_block.end:04X} {unicode_block.name}'

        canvas_width = math.ceil(font_size * metrics[glyph_name][0] / units_per_em)
        if canvas_width <= 0:
            canvas_width = font_size

        glyph_file_dir = os.path.join(dump_dir, 'glyphs', block_dir_name)
        fs_util.make_dirs_if_not_exists(glyph_file_dir)
        glyph_file_path = os.path.join(glyph_file_dir, f'{uni_hex_name}.png')

        image = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        ImageDraw.Draw(image).text(offset_xy, chr(code_point), fill=(0, 0, 0), font=image_font)
        image.save(glyph_file_path)
        glyph_data = glyph_util.load_glyph_data_from_png(glyph_file_path)[0]
        glyph_util.save_glyph_data_to_png(glyph_data, glyph_file_path)
        logger.info(f'dump {glyph_file_path}')

        dop_file_dir = os.path.join(dump_dir, 'dops', block_dir_name)
        fs_util.make_dirs_if_not_exists(dop_file_dir)
        dop_file_path = os.path.join(dop_file_dir, f'{uni_hex_name}.txt')

        dop_txt = ''
        for glyph_data_row in glyph_data:
            for alpha in glyph_data_row:
                if alpha > 0:
                    dot = '◼'
                else:
                    dot = '◻'
                dop_txt += dot
            dop_txt += '\n'
        print(f'char: {c}')
        print(dop_txt)
        with open(dop_file_path, 'w', encoding='utf-8') as file:
            file.write(dop_txt)
        logger.info(f'make {dop_file_path}')


def main():
    dump_font(
        output_name='fusion-pixel-font-monospaced',
        font_file_path=os.path.join(path_define.fonts_dir, 'fusion-pixel-font-monospaced/fusion-pixel-monospaced.otf'),
        font_size=12,
        canvas_height=12,
        offset_xy=(0, 0),
        need_alphabet=gb2312_util.get_alphabet(),
    )


if __name__ == '__main__':
    main()
