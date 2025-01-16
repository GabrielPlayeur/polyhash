import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrow
from simulation import Simulation
from polyparser import parseChallenge
from polysolver import stringifySolution, saveSolution
from objects import TargetCell
from brain import RandomBrain

class Visual:
    def __init__(self, name):
        self.name = name
        self.targets = []
        self.circles = []
        self.arrows = []
        self.previous_positions = []
        self.cntGraphPts = 0

        self.colorConv = {"red": (1.0,0.0, 0.0),
                          "blue": (0,0.0, 1.0),
                          "green": (0,0.5019607843137255,0.0)}

        self.sim = Simulation(parseChallenge(f"./challenges/{name}.in"), RandomBrain())
        self.saved = False

    def create(self):
        self.initElements()

        # Connecter la gestion des événements clavier
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

        plt.title('Grille avec des ballons')
        plt.xlabel('Colonnes')
        plt.ylabel('Lignes')
        plt.show()

    def initElements(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        # Initialisation de la figure et des axes
        self.ax.set_xlim(-0.5, self.sim.COLUMNS - 0.5)
        self.ax.set_ylim(-0.5, self.sim.ROWS - 0.5)
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()

        # Ajouter les zones des targets
        self._initTargets()
        # Ajouter les ballons
        self._initBalloons()
        # Dessiner la grille
        for x in range(self.sim.COLUMNS + 1):
            self.ax.axvline(x - 0.5, color='black', linewidth=0.5)
        for y in range(self.sim.ROWS + 1):
            self.ax.axhline(y - 0.5, color='black', linewidth=0.5)

    def _initTargets(self):
        self.targets = []
        for row in self.sim.map.map:
            for cel in row:
                if len(cel.targets) == 0:
                    continue
                rect = Rectangle(
                    (cel.col - 0.5, cel.row - 0.5),  # Coin inférieur gauche
                    1,  # Largeur
                    1,  # Hauteur
                    color='green',
                    alpha=0.5
                )
                if isinstance(cel, TargetCell):
                    rect.set_color("red")
                    self.targets.append((cel,rect))
                self.ax.add_patch(rect)

    def _initBalloons(self):
        self.circles = []
        self.arrows = []
        self.previous_positions = []
        for bal in self.sim.balloons:
            x_offset = bal.cell.col + np.random.uniform(-0.2, 0.2)
            y_offset = bal.cell.row + np.random.uniform(-0.2, 0.2)
            circle = Circle((x_offset, y_offset), 0.1, color='red', alpha=0.7)
            self.ax.add_patch(circle)
            self.circles.append(circle)
            # Ajouter des flèches initiales (vecteurs nuls au départ)
            arrow = FancyArrow(x_offset, y_offset, 0, 0, width=0.05, color='red', alpha=0.6)
            self.ax.add_patch(arrow)
            self.arrows.append(arrow)
            self.previous_positions.append((bal.cell.col, bal.cell.row))

    def _updateColor(self, element, color: str):
        faceColor = element.get_facecolor()
        if self.colorConv.get(color) == (faceColor[0],faceColor[1],faceColor[2]) :
            return
        element.set_color(color)

    def update(self):
        # Enregistrer les positions actuelles des ballons
        lastP = self.sim.resultData.nbPoints
        # Avancer la simulation


        self.sim.nextTurn()


        lstTar = set()
        for tarVec in self.targets:
            tar, rec = tarVec[0], tarVec[1]
            if len(tar.coverBy)>0:
                self._updateColor(rec,'blue')
                lstTar.add(tar)
            else:
                self._updateColor(rec, 'red')
        self.cntGraphPts += len(lstTar)

        nextPrevPos = []
        # Mettre à jour les positions des ballons
        for bal, circle, prev_pos, arr in zip(self.sim.balloons, self.circles, self.previous_positions, self.arrows):
            new_x, new_y = bal.cell.col, bal.cell.row
            nextPrevPos.append((new_x, new_y))
            if bal.cell is self.sim.map.outsideCell:
                if circle.get_center() != (-1,-1):
                    circle.set_center((-1, -1))
                    arr.set_data(x=-1, y=-1, dx=-1, dy=-1)
                continue
            new_x, new_y = bal.cell.col, bal.cell.row
            old_x, old_y = prev_pos
            dx = new_x - old_x
            dy = new_y - old_y
            arr.set_data(x=old_x, y=old_y, dx=dx, dy=dy)
            # Mise à jour de la position du cercle
            if new_x!=old_x or new_y!=old_y:
                circle.set_center((new_x, new_y))
        self.previous_positions = nextPrevPos

        plt.title(f'Grille avec des ballons: {self.sim.current_round} | {self.sim.resultData.nbPoints} = {lastP} + {self.sim.resultData.nbPoints-lastP} ({self.cntGraphPts})')
        self.fig.canvas.draw_idle()  # Redessine les éléments graphiques

    def undo(self):
        #Reculer la simulation
        self.sim.prevTurn()

        for tarVec in self.targets:
            tar, rec = tarVec[0], tarVec[1]
            if len(tar.coverBy)>0:
                self._updateColor(rec,'blue')
            else:
                self._updateColor(rec, 'red')

        nextPrevPos = []
        # Mettre à jour les positions des ballons
        for bal, circle, prev_pos, arr in zip(self.sim.balloons, self.circles, self.previous_positions, self.arrows):
            new_x, new_y = bal.cell.col, bal.cell.row
            nextPrevPos.append((new_x, new_y))
            if bal.cell is self.sim.map.outsideCell:
                if circle.get_center() != (-1,-1):
                    circle.set_center((-1, -1))
                    arr.set_data(x=-1, y=-1, dx=-1, dy=-1)
                continue
            arr.set_data(x=new_x, y=new_y, dx=0, dy=0)
            # Mise à jour de la position du cercle
            circle.set_center((new_x, new_y))
        self.previous_positions = nextPrevPos
        
        plt.title(f'Grille avec des ballons: {self.sim.current_round}')
        self.fig.canvas.draw_idle()  # Redessine les éléments graphiques


    def on_key(self, event):
        if event.key == 'r' and self.sim.current_round > 0:  # Appuyer sur espace reculer d'un tour
            self.undo()
        elif self.sim.current_round==self.sim.ROUNDS:
            if not self.saved:
                print(self.sim.resultData.nbPoints)
                saveSolution(name+".txt", stringifySolution(self.sim.resultData,self.sim.ROUNDS))
                self.saved = True
        elif event.key == ' ' or event.key == 'z':  # Appuyer sur espace pour avancer d'un tour
            self.update()
        if event.key.lower() == 'q':  # Appuyer sur Q pour quitter
            plt.close(self.fig)

if __name__ == '__main__':
    name = "d_final"
    name = "a_example"
    name = "b_small"
    name = "c_medium"
    v = Visual(name)
    v.create()