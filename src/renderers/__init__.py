from typing import Literal

from .base_renderer import Renderer
from .gui_renderer import GUIRenderer
from .cli_renderer import CLIRenderer

def renderer_factory(renderer_type: Literal["cli"] | Literal["gui"]) -> type[Renderer]:

    if renderer_type == "cli": 
        return CLIRenderer
    else:  
        return GUIRenderer
