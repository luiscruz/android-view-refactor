import click
from lxml import etree
from android_constants import ANDROID_VIEW_GROUPS #supported ViewGroups

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
@click.option('--refactor/--check', default=True, help='Whether refactor will change input.')
@click.option('--comment', default=False, is_flag=True, help='Leave a comment for each refactoring.')
@click.argument('input')
def tool(refactor, comment, input):
    """Tool to refactor Android XML views."""
    tree = etree.parse(input)
    for node in tree.iter():
        for attr_name, _ in node.attrib.items():
            attr_simplename = attr_name.replace(NAMESPACE,"")
            mandatory_parent_view_groups = INVALID_PARAMS.get(attr_simplename)
            if mandatory_parent_view_groups is not None:
                parent_view_group = node.getparent()
                if parent_view_group is not None\
                 and parent_view_group.tag in ANDROID_VIEW_GROUPS\
                 and parent_view_group.tag not in mandatory_parent_view_groups:
                    error_msg = "{}:{} Warning: Invalid layout param in a {}: {} [ObsoleteLayoutParam]".format(input, node.sourceline, parent_view_group.tag, attr_simplename)
                    click.secho(
                        error_msg,
                        err=True,
                        fg="red",
                    )
                    if refactor:
                        if comment:
                            node.append(
                                etree.Comment("Removed ObsoleteLayoutParam: {}".format(attr_simplename))
                            )
                        node.attrib.pop(attr_name)

    with open(input+"new", "w") as f:
        tree.write(
            f,
            xml_declaration=True,
            encoding=tree.docinfo.encoding,
            pretty_print=True,
        )