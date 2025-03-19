from dash import dcc


def add_loading_overlay(elements, use_parent_className: bool = True):
    return dcc.Loading(
        children=elements,
        className="",
        parent_className="h-full grow" if use_parent_className else "",
        overlay_style={
            "visibility": "visible",
            "filter": "blur(2px)",
            "position": "absolute",
            "top": "0",
            "left": "0",
            "width": "100%",
            "height": "100%",
        }
        if use_parent_className
        else {
            "visibility": "visible",
            "filter": "blur(2px)",
        },
        # overlay_style={"visibility": "visible", "filter": "blur(2px)"},
        type="default",
        color="var(--primary-color)",
        # color="black",
    )
