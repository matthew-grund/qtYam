#
#   QtYam UI
#
# Copyright 2024 Matthew Grund
#
# Licensed under the BSD 2 Clause license;
# you may not use this file except in compliance with the License.
#
import os
import requests

import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtGui as qtg
import PySide6.QtNetwork as qtn
import widgets.styled as styled



def create_amp_playback_frame(parent: qtc.QObject):
    frame = qtw.QFrame()
    frame_name = "amp_playback_frame"
    nick_name = "Now Playing"
    frame.setObjectName(frame_name)
    frame.setAccessibleName(frame_name)
    frame.setFrameStyle(parent.frame_style)
    h_layout = qtw.QHBoxLayout(parent)
    parent.album_art_label = styled.styled_label(parent,"album art",18)
    h_layout.addWidget(parent.album_art_label)
    rh_layout = qtw.QVBoxLayout(parent)
    title = styled.styled_label(parent,"playback",20)
    title.setAlignment(qtc.Qt.AlignmentFlag.AlignLeft | qtc.Qt.AlignmentFlag.AlignVCenter)
    title.setText(nick_name)
    rh_layout.addWidget(title)
    
    spacer_1 = styled.styled_frame(parent,"spacer 1")
    rh_layout.addWidget(spacer_1)

    parent.playback_song_label = styled.styled_label(parent,"<song>",22)
    parent.playback_song_label.setAlignment(qtc.Qt.AlignmentFlag.AlignLeft | qtc.Qt.AlignmentFlag.AlignVCenter)
    rh_layout.addWidget(parent.playback_song_label)

    parent.playback_album_label = styled.styled_label(parent,"<album>",20)
    parent.playback_album_label.setAlignment(qtc.Qt.AlignmentFlag.AlignLeft | qtc.Qt.AlignmentFlag.AlignVCenter)
    rh_layout.addWidget(parent.playback_album_label)

    parent.playback_artist_label = styled.styled_label(parent,"<artist>",20)
    parent.playback_artist_label.setAlignment(qtc.Qt.AlignmentFlag.AlignLeft | qtc.Qt.AlignmentFlag.AlignVCenter)
    rh_layout.addWidget(parent.playback_artist_label)
    h_layout.addLayout(rh_layout)
    frame.setLayout(h_layout)
    return frame
