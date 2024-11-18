#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module.
"""
from cells import Cell

class PathBalloon:
    def __init__(self) -> None:
        self.altHistory: list[int] # [1, 0, 0, 1, 1, -1]
        self.cellsHistory: list[Cell]