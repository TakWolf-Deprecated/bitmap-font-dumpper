import os

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

assets_dir = os.path.join(project_root_dir, 'assets')
fonts_dir = os.path.join(assets_dir, 'fonts')

build_dir = os.path.join(project_root_dir, 'build')
outputs_dir = os.path.join(build_dir, 'outputs')
