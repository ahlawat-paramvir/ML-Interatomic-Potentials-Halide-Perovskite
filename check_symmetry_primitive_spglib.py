from ase.io import read, write
import spglib as spg
from ase.atoms import Atoms

atoms = read('POSCAR_final')
cell, positions, numbers = spg.refine_cell(atoms, symprec=1e-03)
refined_atoms = Atoms(numbers, scaled_positions=positions, cell=cell, pbc=True)

pcell, ppositions, pnumbers = spg.find_primitive(atoms, symprec=1e-03)
primitive_atoms = Atoms(pnumbers, scaled_positions=ppositions, cell=pcell, pbc=True)


print(refined_atoms)
print(primitive_atoms)
