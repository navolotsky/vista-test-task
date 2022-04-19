from functools import partial
from typing import Dict, List, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QValidator
from PyQt5.QtWidgets import QLineEdit

StateToColor = Dict[QValidator.State, Optional[QColor]]


class InputValidationHighlighterMixin:
    state_to_color: StateToColor = {
        QValidator.Acceptable: None,
        QValidator.Intermediate: QColor(Qt.yellow),
        QValidator.Invalid: QColor(Qt.red),
    }

    def setup_highlighting(self, line_edits_to_watch: Optional[List[QLineEdit]] = None,
                           state_to_color: Optional[StateToColor] = None,
                           intermediate_is_invalid_if_finished=True):
        if line_edits_to_watch is None:
            line_edits_to_watch = [attr for attr in vars(self).values() if isinstance(attr, QLineEdit)]

        if state_to_color is None:
            state_to_color = self.state_to_color

        if getattr(self, "_all_watched_line_edits", None) is None:
            self._all_watched_line_edits: Dict[QLineEdit, partial] = {}

        for line_edit in line_edits_to_watch:
            if line_edit.validator() is None:
                continue
            original_color = line_edit.palette().color(line_edit.backgroundRole())
            f = partial(self._validate_and_highlight, line_edit,
                        original_color, state_to_color, intermediate_is_invalid_if_finished)
            self._all_watched_line_edits[line_edit] = f
            line_edit.textEdited.connect(f)

    @staticmethod
    def _validate_and_highlight(line_edit, original_color, state_to_color, intermediate_is_invalid_if_finished,
                                text=None):
        if text is None:
            text = line_edit.text()
        state, *_ = line_edit.validator().validate(text, 0)
        if intermediate_is_invalid_if_finished and not line_edit.hasFocus() and state == QValidator.Intermediate:
            state = QValidator.Invalid

        color = state_to_color[state]
        if color is None:
            color = original_color
        palette = line_edit.palette()
        palette.setColor(line_edit.backgroundRole(), color)
        line_edit.setPalette(palette)
        return state

    def validate_and_highlight_all(self):
        not_correct = {}
        for line_edit, f in self._all_watched_line_edits.items():
            state = f()
            if state != QValidator.Acceptable:
                not_correct[line_edit] = state
        return not_correct
