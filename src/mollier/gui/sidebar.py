"""
The application's navigation rail.

Home, then the tools under a "Tools" heading that folds away. The rail is a
list of places rather than a row of buttons: labels align in a column, the
current page is marked by fill *and* weight *and* ink so the selection never
rests on a background tint alone, and the whole thing can be narrowed or
hidden when the content needs the width. Hidden, it leaves a thin strip
behind holding the way back.
"""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import QButtonGroup, QLabel, QSizePolicy, QWidget

from . import layout as ly
from .icons import app_pixmap, icon
from .theme import Tokens

HOME = ("home", "Home", "house",
        "Start here and pick a tool.")

# key, label, icon name, one-line description. The order is the navigation
# order.
TOOLS = (
    ("single_point", "Single point", "crosshair",
     "Properties of a pure fluid at a state fixed by two properties."),
    ("mixture", "Mixture", "blend",
     "Ideal-gas and humid-air mixture properties at a given state."),
    ("saturation", "Saturation", "droplet",
     "Saturated liquid and vapour properties at a temperature or pressure."),
    ("process_path", "Process path", "trending-up",
     "Properties along isobaric, isentropic, polytropic and other paths."),
    ("plotting", "Plotting", "chart-line",
     "T-S, P-H, P-V and H-S diagrams, phase envelopes and custom plots."),
)

# Every page, in stack order: the index into this is the page index.
PAGES = (HOME,) + TOOLS

HIDE_TIP = "Hide the sidebar (Ctrl+B)"
SHOW_TIP = "Show the sidebar (Ctrl+B)"


class Sidebar(QWidget):
    """Vertical navigation. Emits the index of the page the user picked."""

    selected = Signal(int)
    hide_requested = Signal()

    MIN_W = 168      # the longest label plus its icon, without eliding
    DEFAULT_W = 220

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setMinimumWidth(self.MIN_W)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        panel = ly.vbox(self, margin=Tokens.SPACING_ROW,
                        spacing=Tokens.SPACING_GROUP)

        brand_row = ly.hbox(spacing=Tokens.SPACING_ROW)
        brand_row.setContentsMargins(Tokens.SPACING_ROW, Tokens.SPACING_ROW,
                                     Tokens.SPACING_ROW, 0)
        logo = QLabel()
        logo.setPixmap(app_pixmap(Tokens.ICON_BRAND))
        brand_row.addWidget(logo)
        brand_row.addWidget(ly.brand("Mollier"))
        brand_row.addStretch()
        panel.addLayout(brand_row)

        nav = ly.vbox(spacing=2)   # destinations are one list, so tight
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        self._buttons = []

        nav.addWidget(self._nav_button(0, HOME))

        self.tools_toggle = ly.button("Tools", variant="section",
                                      on_click=self._on_tools_toggled)
        self.tools_toggle.setCheckable(True)
        self.tools_toggle.setChecked(True)
        self.tools_toggle.setIconSize(QSize(Tokens.ICON_SIZE,
                                            Tokens.ICON_SIZE))
        self.tools_toggle.setSizePolicy(QSizePolicy.Preferred,
                                        QSizePolicy.Fixed)
        nav.addSpacing(Tokens.SPACING_ROW)
        nav.addWidget(self.tools_toggle)

        self._tool_buttons = []
        for offset, page in enumerate(TOOLS, start=1):
            button = self._nav_button(offset, page)
            self._tool_buttons.append(button)
            nav.addWidget(button)

        panel.addLayout(nav)
        panel.addStretch()

        footer = ly.hbox()
        footer.addStretch()
        footer.addWidget(ly.icon_button(
            icon("chevrons-left"), tooltip=HIDE_TIP,
            on_click=self.hide_requested.emit))
        panel.addLayout(footer)

        self._buttons[0].setChecked(True)
        self.set_tools_expanded(True)

    def _nav_button(self, index: int, page: tuple):
        _key, label, glyph, _description = page
        button = ly.button(label, variant="nav")
        button.setCheckable(True)
        button.setIcon(icon(glyph))
        button.setIconSize(QSize(Tokens.ICON_SIZE, Tokens.ICON_SIZE))
        button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        button.setToolTip(label)
        button.clicked.connect(lambda _checked: self.selected.emit(index))
        self._group.addButton(button, index)
        self._buttons.append(button)
        return button

    def _on_tools_toggled(self) -> None:
        self.set_tools_expanded(self.tools_toggle.isChecked())

    def set_tools_expanded(self, expanded: bool) -> None:
        """Fold or unfold the tool list under its heading."""
        self.tools_toggle.setChecked(expanded)
        self.tools_toggle.setIcon(
            icon("chevron-down" if expanded else "chevron-right"))
        self.tools_toggle.setToolTip(
            "Collapse the tool list" if expanded else "Expand the tool list")
        for button in self._tool_buttons:
            button.setVisible(expanded)

    def tools_expanded(self) -> bool:
        return self.tools_toggle.isChecked()

    def set_current(self, index: int) -> None:
        """Mark a page as current without re-emitting the selection."""
        if 0 <= index < len(self._buttons):
            # A current page hidden inside a folded section would leave the
            # rail with no visible selection.
            if index > 0 and not self.tools_expanded():
                self.set_tools_expanded(True)
            self._buttons[index].setChecked(True)

    def current(self) -> int:
        return self._group.checkedId()


class SidebarStrip(QWidget):
    """What stays visible while the rail is hidden: one button to bring it
    back, at the same bottom position as the button that hid it."""

    show_requested = Signal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("sidebarStrip")
        self.setAttribute(Qt.WA_StyledBackground, True)
        margin = Tokens.SPACING_ROW // 2
        # Width set to fit the button exactly, plus the 1 px right rule.
        self.setFixedWidth(Tokens.CONTROL_HEIGHT + 2 * margin + 1)
        column = ly.vbox(self, margin=margin)
        column.setContentsMargins(margin, margin, margin + 1,
                                  Tokens.SPACING_ROW)
        column.addStretch()
        column.addWidget(ly.icon_button(
            icon("chevrons-right"), tooltip=SHOW_TIP,
            on_click=self.show_requested.emit))
