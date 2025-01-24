# Projet Polyhash

## The team

- TEIGNE Gabriel - Project leader and developper - gabriel.teigne@etu.univ-nantes.fr
- DANIAUD Tom - Developper - tom.daniaud@etu.univ-nantes.fr
- PETIOT Florian - Developper and video editor - florian.petiot@etu.univ-nantes.fr
- DEMAURE Côme - Developper and redactor - come.demaure@etu.univ-nantes.fr


## Description

This project aims to solve the HashCode 2015 topic provided by Google France.
The aim is to optimize the movement of Internet-providing balloons to cover receptors for as long as possible.
To achieve this, we need to decide how to move the balloons based on the wind map available at various altitudes.


## Task distribution

**TEIGNE Gabriel**
- Tree strategy optimisation
- Test sets
- Add visualisation

**DANIAUD Tom**
- Tree strategy implementation
- Simulation creation

**DEMAURE Côme**
- Adding history and an undo of visualisation

**PETIOT Florian**
- Object implementation


## How to install

1. Clone the repository :
   ```sh
   git clone https://gitlab.univ-nantes.fr/E225805Q/polyhash2024.git
   ```
2. Install dependencies :
   ```sh
   pip install -r requirements.txt
   ```

## How to execute

To run the project, use the following command:

```sh
python polyhash.py challenge_name.in output_name.txt
```

The challenge file must be in the challenges/ folder.


## Strategy implemented

We have implemented the following strategies to optimize our solutions:

1. **Balloon path optimization**:
   - For each balloon, we try to find the path that yields the most points.
   - This path influences the next best paths, since there's no need to pass through the same receivers at the same time.
   - To avoid exponential complexity, each level of the tree is limited to a certain number of nodes.
   - This number increases linearly with each new level (500, 1,000, 1,500, ...).
   - If the number of nodes exceeds the maximum value, only the nodes with the highest score are retained.
   - A depth threshold is set to select the most profitable path.
   - If two paths are equally profitable, one of them is chosen at random.
   - Once this path has been determined, a new tree is recreated from it, and the strategy is repeated until the end of the simulation.


We also carried out other strategies to test how well the simulation worked / to serve as a comparison with our main strategy:

2. **Application of Djikstra's algorithm** :
   - When the balloon starts moving, we look for the target closest to the balloon using Djikstra's algorithm.
   - Once we've reached the target, we search for the nearest target in the same way.
   - We repeat this process until the end of the simulation.

3. **Random strategy** :
  - At each new turn, the ball chooses the next legal move at random.


## Performances

### Best result : 509 000 points

using the "Balloon path optimization" strategy

Depth : 200
Width : 350

- Execution time : 1:43:21
- Memory usage : 4Go


## Organisation du Code

The project is structured using an object-oriented paradigm, as follows:

```
polyhash2024/
├── polyhash.py
├── simulation.py
├── cellMap.py
├── objects/
│   ├── __init__.py
│   ├── balloon.py
│   ├── cell.py
│   ├── targetCell.py
│   └── wind.py
├── brain/
│   ├── __init__.py
│   ├── randomBrain.py
│   ├── closestBrain.py
│   ├── treeBrain.py
│   └── verifyBrain.py
├── visual/
│   ├── playSimulation.py
│   ├── vectorField.py
│   └── hotmap.py
├── challenges/
│   └── nom_challenge.in
├── test/
│   └── test_fichier.py
└── README.md
```


## Bugs and known limitations

- Cutting the tree forces us to choose one of the best paths at the end of the Nth round, which is not optimal. This choice is made randomly and past performance does not prejudge future performance.
- We cannot run the program to create the entire d_final challenge tree with a width of 400 in a reasonable time. For us, this is due to the fact that using python and the object paradigm makes managing elements in memory slow.
- When we split the tree into several sub-trees, the final score calculation differs from that calculated during the simulation (between 50 and 200 points difference on the d_final challenge). This does not seem to affect the decision-making process.


## Other informations

- One big improvement that could be made is to create and use a single tree by updating the balloon points. This would greatly reduce the creation time and allow deeper and wider trees to be created in a similar amount of time.
- Change the language to C++ to allow billions of operations to be performed more quickly.