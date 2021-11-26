import dataclasses
import logging
from functools import partial
from PySide2.QtGui import QPixmap

from PySide2.QtWidgets import QWidget
from randovania.games.cave_story.layout.cs_cosmetic_patches import CSCosmeticPatches, MusicRandoType, MyChar
from randovania.gui.dialog.base_cosmetic_patches_dialog import BaseCosmeticPatchesDialog
from randovania.gui.generated.cs_cosmetic_patches_dialog_ui import Ui_CSCosmeticPatchesDialog
from randovania.gui.lib.common_qt_lib import set_combo_with_value


class CSCosmeticPatchesDialog(BaseCosmeticPatchesDialog, Ui_CSCosmeticPatchesDialog):
    _cosmetic_patches: CSCosmeticPatches

    def __init__(self, parent: QWidget, current: CSCosmeticPatches):
        super().__init__(parent)
        self.setupUi(self)
        self._cosmetic_patches = current

        for i in range(4):
            self.music_type_combo.setItemData(i, list(MusicRandoType)[i])

        self.on_new_cosmetic_patches(current)
        self.connect_signals()
    
    def connect_signals(self):
        super().connect_signals()

        self.music_type_combo.currentIndexChanged.connect(self._on_music_type_changed)
        self.mychar_left_button.clicked.connect(self._mychar_left)
        self.mychar_right_button.clicked.connect(self._mychar_right)

    def on_new_cosmetic_patches(self, patches: CSCosmeticPatches):
        set_combo_with_value(self.music_type_combo, patches.music_rando.randomization_type)
        self._set_mychar(patches.mychar)

    def _on_mychar_changed(self, reverse: bool):
        new_mychar = self._cosmetic_patches.mychar.next_mychar(reverse)
        self._cosmetic_patches = dataclasses.replace(self._cosmetic_patches, mychar=new_mychar)
        self._set_mychar(new_mychar)
    
    def _mychar_left(self):
        self._on_mychar_changed(True)
    
    def _mychar_right(self):
        self._on_mychar_changed(False)
    
    def _set_mychar(self, new_mychar: MyChar):
        self.mychar_name_label.setText(new_mychar.value)
        self.mychar_img_label.setPixmap(QPixmap(str(new_mychar.ui_icon)))
        self.mychar_description_label.setText(new_mychar.description)
        self.mychar_description_label.setVisible(bool(new_mychar.description))
    
    def _on_music_type_changed(self):
        combo_enum: MusicRandoType = self.music_type_combo.currentData()
        music_rando = dataclasses.replace(self._cosmetic_patches.music_rando, randomization_type=combo_enum)
        self._cosmetic_patches = dataclasses.replace(self._cosmetic_patches, music_rando=music_rando)
        self.music_type_description_label.setText(combo_enum.description)

    def _persist_option_then_notify(self, attribute_name: str):
        def persist(value: int):
            self._cosmetic_patches = dataclasses.replace(
                self._cosmetic_patches,
                **{attribute_name: bool(value)}
            )
        return persist

    @property
    def cosmetic_patches(self) -> CSCosmeticPatches:
        return self._cosmetic_patches
    
    def reset(self):
        self.on_new_cosmetic_patches(CSCosmeticPatches())