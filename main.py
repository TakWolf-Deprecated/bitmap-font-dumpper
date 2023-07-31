import logging
import math
import os

import unidata_blocks
from PIL import ImageFont, Image, ImageDraw
from fontTools.ttLib import TTFont

from configs import path_define
from utils import fs_util, glyph_util

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('main')


def dump_font(
        font_file_path: str,
        outputs_dir: str,
        rasterize_size: int = None,
        rasterize_offset: tuple[int, int] = (0, 0),
):
    fs_util.delete_dir(outputs_dir)
    fs_util.make_dirs(outputs_dir)

    font = TTFont(font_file_path)
    image_font = ImageFont.truetype(font_file_path, rasterize_size)

    canvas_height = math.ceil((font['hhea'].ascent - font['hhea'].descent) / font['head'].unitsPerEm * rasterize_size)

    for code_point, glyph_name in font.getBestCmap().items():
        canvas_width = math.ceil(font['hmtx'].metrics[glyph_name][0] / font['head'].unitsPerEm * rasterize_size)
        if canvas_width <= 0:
            continue

        image = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
        ImageDraw.Draw(image).text(rasterize_offset, chr(code_point), fill=(0, 0, 0, 255), font=image_font)

        block = unidata_blocks.get_block_by_code_point(code_point)
        block_dir_name = f'{block.code_start:04X}-{block.code_end:04X} {block.name}'
        glyph_file_to_dir = os.path.join(outputs_dir, block_dir_name)
        hex_name = f'{code_point:04X}'
        if block.code_start == 0x4E00:  # CJK Unified Ideographs
            glyph_file_to_dir = os.path.join(glyph_file_to_dir, f'{hex_name[0:-2]}-')
        glyph_file_to_path = os.path.join(glyph_file_to_dir, f'{hex_name}.png')

        fs_util.make_dirs(glyph_file_to_dir)
        image.save(glyph_file_to_path)
        glyph_data = glyph_util.load_glyph_data_from_png(glyph_file_to_path)[0]
        glyph_util.save_glyph_data_to_png(glyph_data, glyph_file_to_path)
        logger.info("Dump glyph: '%s'", glyph_file_to_path)


def main():
    dump_font(
        font_file_path=os.path.join(path_define.fonts_dir, 'SourceHanSerifOTF/OTF/SimplifiedChinese/SourceHanSerifSC-Heavy.otf'),
        outputs_dir=os.path.join(path_define.outputs_dir, 'SourceHanSerifOTF'),
        rasterize_size=32,
        rasterize_offset=(0, -2),
    )


if __name__ == '__main__':
    main()
