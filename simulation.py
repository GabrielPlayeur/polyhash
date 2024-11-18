#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module.
"""
from cell import Cell
from wind import Wind
from balloon import Balloon

class Simulation:
    def __init__(self) -> None:
        self.R: int
        self.C: int
        self.A: int
        self.NB_ROUND: int
        self.current_round: int
        self.map: tuple[tuple[Cell]]
        self.balloons: set[Balloon]

        self.initMap
        self.initNeighborh


    def nextTurn(self) -> None:
        for balloon in self.balloons:
            # balloon.moveAlt() Choix de simulation
            self.moveBalloon(balloon)
            balloon.chooseAction() # Choix de simulation
            balloon.next()

    def moveBalloon(self, balloon: Balloon) -> None:
        cell = balloon.cell
        wind = cell.getWinds(balloon.alt)
        if cell.x+wind.x > self.R : #TODO
            self.balloons.remove(balloon)
            return
        x = 0
        y = 0
        balloon.cell = self.map[x][y]
