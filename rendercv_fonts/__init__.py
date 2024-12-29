"""
Some fonts for RenderCV.
"""

import pathlib

__version__ = "0.1.0"

available_font_families = ["SourceSans3"]
path_of = {
    font_famiy: pathlib.Path(__file__).parent / font_famiy
    for font_famiy in available_font_families
}
paths_to_font_folders = [
    pathlib.Path(__file__).parent / font_family
    for font_family in available_font_families
]
