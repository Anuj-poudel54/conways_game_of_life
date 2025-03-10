from typing import Literal

from .base_renderer import Renderer
from .cli_renderer import CLIRenderer

def renderer_factory(renderer_type: Literal["cli"] | Literal["gui"]) -> type[Renderer]:

    if renderer_type == "cli": 
        return CLIRenderer
    else:  
        #importing so that on selecting cli mode, greeting from pygame won't show on terminal.
        from .gui_renderer import GUIRenderer 
        return GUIRenderer
