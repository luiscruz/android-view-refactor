import click
import xml.etree.ElementTree as ET
from lxml import etree

INVALID_PARAMS = {
    "layout_x"                      : ["AbsoluteLayout"],
    "layout_y"                      : ["AbsoluteLayout"],
    "layout_weight"                 : ["LinearLayout", "ActionMenuView", "AppBarLayout", "ListRowHoverCardView", "ListRowView", "NumberPicker", "RadioGroup", "SearchView", "TabWidget", "TableLayout", "TableRow", "TextInputLayout", "ZoomControls"],
    "layout_column"                 : ["GridLayout", "TableLayout", "TableRow"],
    "layout_columnSpan"             : ["GridLayout",],
    "layout_row"                    : ["GridLayout",],
    "layout_rowSpan"                : ["GridLayout",],
    "layout_span"                   : ["TableRow"], # DANGER - check lint source code
    "layout_alignLeft"              : ["RelativeLayout"],
    "layout_alignStart"             : ["RelativeLayout"],
    "layout_alignRight"             : ["RelativeLayout"],
    "layout_alignEnd"               : ["RelativeLayout"],
    "layout_alignTop"               : ["RelativeLayout"],
    "layout_alignBottom"            : ["RelativeLayout"],
    "layout_alignParentTop"         : ["RelativeLayout"],
    "layout_alignParentBottom"      : ["RelativeLayout"],
    "layout_alignParentLeft"        : ["RelativeLayout"],
    "layout_alignParentStart"       : ["RelativeLayout"],
    "layout_alignParentRight"       : ["RelativeLayout"],
    "layout_alignParentEnd"         : ["RelativeLayout"],
    "layout_alignWithParentMissing" : ["RelativeLayout"],
    "layout_alignBaseline"          : ["RelativeLayout"],
    "layout_centerInParent"         : ["RelativeLayout"],
    "layout_centerVertical"         : ["RelativeLayout"],
    "layout_centerHorizontal"       : ["RelativeLayout"],
    "layout_toRightOf"              : ["RelativeLayout"],
    "layout_toEndOf"                : ["RelativeLayout"],
    "layout_toLeftOf"               : ["RelativeLayout"],
    "layout_toStartOf"              : ["RelativeLayout"],
    "layout_below"                  : ["RelativeLayout"],
    "layout_above"                  : ["RelativeLayout"],
}
NAMESPACE = "{http://schemas.android.com/apk/res/android}"

@click.command()
@click.option('--refactor/--check', default=True, help='Whether transformations will take place.')
@click.argument('input')
def tool(refactor, input):
    """Tool to refactor Android XML views."""
    tree = etree.parse(input)
    for node in tree.iter():
        for attr_name, _ in node.attrib.items():
            attr_name = attr_name.replace(NAMESPACE,"")
            mandatory_parent_view_groups = INVALID_PARAMS.get(attr_name)
            if mandatory_parent_view_groups is not None:
                parent_view_group = node.getparent()
                if parent_view_group is not None and parent_view_group.tag not in mandatory_parent_view_groups:
                    if refactor:
                        pass
                    else:
                        error_msg = "{}:{} Warning: Invalid layout param in a {}: {} [ObsoleteLayoutParam]".format(input, node.sourceline, parent_view_group.tag, attr_name)
                        click.secho(
                            error_msg,
                            err=True,
                            fg="red",
                        )
