import dataclasses
import uuid

import pytest
from PySide2.QtCore import Qt

from randovania.games.game import RandovaniaGame
from randovania.gui.preset_settings.logic_settings_window import LogicSettingsWindow
from randovania.interface_common.preset_editor import PresetEditor


@pytest.mark.parametrize("game", [RandovaniaGame.PRIME1, RandovaniaGame.PRIME2, RandovaniaGame.PRIME3])
def test_on_preset_changed(skip_qtbot, preset_manager, game):
    # Setup
    base = preset_manager.default_preset_for_game(game).get_preset()
    preset = dataclasses.replace(base,
                                 uuid=uuid.UUID('b41fde84-1f57-4b79-8cd6-3e5a78077fa6'),
                                 base_preset_uuid=base.uuid)
    editor = PresetEditor(preset)
    window = LogicSettingsWindow(None, editor)

    # Run
    window.on_preset_changed(editor.create_custom_preset_with())


def test_starting_location_world_select(skip_qtbot, default_preset):
    # Setup
    preset = dataclasses.replace(default_preset,
                                 uuid=uuid.UUID('b41fde84-1f57-4b79-8cd6-3e5a78077fa6'),
                                 base_preset_uuid=default_preset.uuid)
    editor = PresetEditor(preset)
    window = LogicSettingsWindow(None, editor)
    skip_qtbot.addWidget(window)

    # Run
    checkbox_list = window._starting_location_for_world
    window.on_preset_changed(editor.create_custom_preset_with())
    assert len(checkbox_list) == 10
    temple_grounds_checkbox = checkbox_list["Temple Grounds"]
    assert temple_grounds_checkbox.checkState() == Qt.PartiallyChecked
    skip_qtbot.mouseClick(temple_grounds_checkbox, Qt.LeftButton)
    assert temple_grounds_checkbox.checkState() == Qt.Checked
    assert len(editor.configuration.starting_location.locations) == 39
    skip_qtbot.mouseClick(temple_grounds_checkbox, Qt.LeftButton)
    assert temple_grounds_checkbox.checkState() == Qt.Unchecked
    assert len(editor.configuration.starting_location.locations) == 0
    skip_qtbot.mouseClick(temple_grounds_checkbox, Qt.LeftButton)
    window.on_preset_changed(editor.create_custom_preset_with())
    assert temple_grounds_checkbox.checkState() == Qt.Checked
    assert len(editor.configuration.starting_location.locations) == 39
