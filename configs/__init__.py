import os

from configs import path_define
from utils.unidata_util import UnidataDB

unidata_db = UnidataDB(os.path.join(path_define.unidata_dir, 'Blocks.txt'))
