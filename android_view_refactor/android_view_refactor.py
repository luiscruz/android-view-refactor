import click
from lxml import etree
from android_constants import ANDROID_VIEW_GROUPS  # supported ViewGroups

INVALID_PARAMS = {
    "layout_x":                       ["AbsoluteLayout"],
    "layout_y":                       ["AbsoluteLayout"],
    "layout_weight":                  [
        "LinearLayout",
        "ActionMenuView",
        "AppBarLayout",
        "ListRowHoverCardView",
        "ListRowView",
        "NumberPicker",
        "RadioGroup",
        "SearchView",
        "TabWidget",
        "TableLayout",
        "TableRow",
        "TextInputLayout",
        "ZoomControls"
    ],
    "layout_column":                  [
        "GridLayout",
        "TableLayout",
        "TableRow"
    ],
    "layout_columnSpan":              ["GridLayout"],
    "layout_row":                     ["GridLayout"],
    "layout_rowSpan":                 ["GridLayout"],
    # DANGER - check lint source code
    "layout_span":                    ["TableRow"],
    # -----
    "layout_alignLeft":               ["RelativeLayout"],
    "layout_alignStart":              ["RelativeLayout"],
    "layout_alignRight":              ["RelativeLayout"],
    "layout_alignEnd":                ["RelativeLayout"],
    "layout_alignTop":                ["RelativeLayout"],
    "layout_alignBottom":             ["RelativeLayout"],
    "layout_alignParentTop":          ["RelativeLayout"],
    "layout_alignParentBottom":       ["RelativeLayout"],
    "layout_alignParentLeft":         ["RelativeLayout"],
    "layout_alignParentStart":        ["RelativeLayout"],
    "layout_alignParentRight":        ["RelativeLayout"],
    "layout_alignParentEnd":          ["RelativeLayout"],
    "layout_alignWithParentMissing":  ["RelativeLayout"],
    "layout_alignBaseline":           ["RelativeLayout"],
    "layout_centerInParent":          ["RelativeLayout"],
    "layout_centerVertical":          ["RelativeLayout"],
    "layout_centerHorizontal":        ["RelativeLayout"],
    "layout_toRightOf":               ["RelativeLayout"],
    "layout_toEndOf":                 ["RelativeLayout"],
    "layout_toLeftOf":                ["RelativeLayout"],
    "layout_toStartOf":               ["RelativeLayout"],
    "layout_below":                   ["RelativeLayout"],
    "layout_above":                   ["RelativeLayout"],
}
NAMESPACE = "{http://schemas.android.com/apk/res/android}"


@click.command()
@click.option(
    '--refactor/--check', default=True,
    help='Whether refactor will change input.'
)
@click.option(
    '--comment', default=False, is_flag=True,
    help='Leave a comment for each refactoring.'
)
@click.argument('input')
def tool(refactor, comment, input):
    """Tool to refactor Android XML views."""
    parser = etree.XMLParser(
       remove_blank_text=True
    )
    tree = etree.parse(input, parser)
    tree_has_changed = False
    for node in tree.iter():
        for attr_name, _ in node.attrib.items():
            attr_simplename = attr_name.replace(NAMESPACE, "")
            mandatory_parent_view_groups = INVALID_PARAMS.get(attr_simplename)
            if mandatory_parent_view_groups is not None:
                parent_view_group = node.getparent()
                if parent_view_group is not None\
                    and parent_view_group.tag in ANDROID_VIEW_GROUPS\
                        and parent_view_group.tag\
                        not in mandatory_parent_view_groups:
                    error_msg = "{}:{} Warning: Invalid layout param in\
                     a {}: {} [ObsoleteLayoutParam]".format(
                        input,
                        node.sourceline,
                        parent_view_group.tag,
                        attr_simplename
                    )
                    click.secho(
                        error_msg,
                        err=True,
                        fg="red",
                    )
                    if refactor:
                        if comment is not None:
                            comment = etree.Comment(
                                "Removed ObsoleteLayoutParam: {}"
                                .format(attr_simplename)
                            )
                            node.append(comment)
                        node.attrib.pop(attr_name)
                        tree_has_changed = True
    if refactor and tree_has_changed:
        output = etree.tostring(
            tree,
            xml_declaration=True,
            pretty_print=True,
            encoding=tree.docinfo.encoding,
        )
        output = output.replace("\" ", "\"\n")
        with open(input+"new", "w") as f:
            parent_tag_line = None
            parent_line_ident = None
            for i, line in enumerate(output.splitlines()):
                line_stripped = line.lstrip(" ")
                line_ident = len(line) - len(line_stripped)
                if parent_tag_line is not None:
                    if line_ident == 0 and line[:2] != "</":
                        line = (parent_line_ident + 2)*" " + line
                    else:
                        parent_tag_line = line
                        parent_line_ident = line_ident
                        line_stripped = line.lstrip()
                        if line_stripped[:4] != "<!--"\
                                and line_stripped[:2] != "</":
                            line = "\n" + line
                else:
                    parent_tag_line = line
                    parent_line_ident = line_ident
                print >>f, line
