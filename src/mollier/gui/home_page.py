"""
The welcome page: the app's icon and name, one line on what it does, and a
card for each tool. Everything sits in one centred column so the page reads
top to bottom, and the column scrolls rather than clips on a short window.
"""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QLabel, QPushButton, QScrollArea, QSizePolicy, QWidget,
)

from . import layout as ly
from .icons import app_pixmap, glyph_pixmap
from .theme import Tokens

DESCRIPTION = (
    "Thermophysical properties of pure fluids and mixtures, from CoolProp. "
    "Fix a state, find saturation conditions, follow a process path or draw "
    "a property diagram."
)


class ToolCard(QPushButton):
    """A whole-card button: the tool's icon, its name and what it does."""

    def __init__(self, label: str, glyph: str, description: str,
                 parent: QWidget | None = None):
        super().__init__(parent)
        self.setProperty("variant", "card")
        self.setCursor(Qt.PointingHandCursor)
        self.setAccessibleName(label)
        self.setAccessibleDescription(description)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        row = ly.hbox(self, margin=Tokens.MARGIN_GROUP,
                      spacing=Tokens.MARGIN_GROUP)
        glyph_label = QLabel()
        glyph_label.setPixmap(glyph_pixmap(glyph, Tokens.ICON_CARD,
                                           Tokens.INK_SECONDARY))
        row.addWidget(glyph_label, 0, Qt.AlignVCenter)

        text = ly.vbox(spacing=2)
        name = QLabel(label)
        name.setProperty("role", "strong")
        text.addWidget(name)
        text.addWidget(ly.caption(description))
        row.addLayout(text, 1)

        # The labels are decoration on the button: clicks and hover belong
        # to the card, not to whichever label the pointer happens to cross.
        for child in self.findChildren(QLabel):
            child.setAttribute(Qt.WA_TransparentForMouseEvents, True)

    def sizeHint(self) -> QSize:
        # QPushButton sizes itself from its own text, which is empty here;
        # the child layout is what actually needs the room.
        return self.layout().sizeHint()

    def minimumSizeHint(self) -> QSize:
        return QSize(0, self.layout().minimumSize().height())

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int) -> int:
        return self.layout().totalHeightForWidth(width)


class HomePage(QScrollArea):
    """Welcome page. Emits the page index of the tool the user picked."""

    open_page = Signal(int)

    COLUMN_W = 560

    def __init__(self, tools, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.NoFrame)

        body = QWidget()
        body.setObjectName("homePage")
        outer = ly.vbox(body)
        outer.addStretch(1)

        column = QWidget()
        column.setMaximumWidth(self.COLUMN_W)
        column.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        stack = ly.vbox(column, spacing=Tokens.SPACING_ROW)

        logo = QLabel()
        logo.setPixmap(app_pixmap(Tokens.ICON_HERO))
        logo.setAlignment(Qt.AlignCenter)
        stack.addWidget(logo)
        stack.addSpacing(Tokens.SPACING_ROW)

        welcome = ly.title("Welcome to Mollier")
        welcome.setAlignment(Qt.AlignCenter)
        stack.addWidget(welcome)

        lead = QLabel(DESCRIPTION)
        lead.setProperty("role", "lead")
        lead.setWordWrap(True)
        lead.setAlignment(Qt.AlignCenter)
        stack.addWidget(lead)
        stack.addSpacing(Tokens.SPACING_SECTION - Tokens.SPACING_ROW)

        for index, (_key, label, glyph, description) in tools:
            card = ToolCard(label, glyph, description)
            card.clicked.connect(
                lambda _checked=False, i=index: self.open_page.emit(i))
            stack.addWidget(card)

        # The column takes the width up to its maximum; the stretches either
        # side share whatever is left, which centres it.
        centre = ly.hbox(spacing=0)
        centre.addStretch(1)
        centre.addWidget(column, 1000)
        centre.addStretch(1)
        outer.addLayout(centre)
        outer.addStretch(1)
        self.setWidget(body)
