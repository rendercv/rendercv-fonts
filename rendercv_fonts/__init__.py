"""
Some fonts for RenderCV.
"""

import pathlib

__version__ = "0.3.0"

package_folder_path = pathlib.Path(__file__).parent

# Make a list of all the folders (except __pycache__) in the package folder:
available_font_families = [
    folder.name
    for folder in package_folder_path.iterdir()
    if folder.is_dir() and folder.name != "__pycache__"
]
path_of = {
    font_famiy: package_folder_path / font_famiy
    for font_famiy in available_font_families
}
paths_to_font_folders = [path for path in path_of.values()]
