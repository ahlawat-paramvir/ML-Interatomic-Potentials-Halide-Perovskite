# Partially adapated from Matlantis 
from ase import Atoms
from ase.calculators.calculator import Calculator
from ase.constraints import ExpCellFilter
from ase.optimize import FIRE
from ase.spacegroup.symmetrize import FixSymmetry
from ase.spacegroup.symmetrize import check_symmetry
from ase.build import bulk
from ase.build.tools import sort
import torch
from nequip.ase import NequIPCalculator
import sys
from ase.io import read, write

def opt_with_symmetry(
    atoms_in: Atoms,
    calculator: Calculator,
    fix_symmetry: bool = False,
    external_strain: bool = False,
) -> Atoms:
    atoms = atoms_in.copy()
    atoms.calc = calculator
    if fix_symmetry:
        atoms.set_constraint([FixSymmetry(atoms)])
    ECF = ExpCellFilter(atoms, external_strain=external_strain)
    opt = FIRE(ECF, logfile='relax.log')
    opt.run(fmax=1e-05)

    cell_diff = (atoms.cell.cellpar() / atoms_in.cell.cellpar() - 1.0) * 100
    print("Optimized Cell         :", atoms.cell.cellpar())
    print("Optimized Cell diff (%):", cell_diff)
    print("Scaled positions       :\n", atoms.get_scaled_positions())
    print(f"Epot after opt: {atoms.get_potential_energy()} eV")
    return atoms


atoms=read("POSCAR_init",format='vasp')
atoms=atoms.repeat((4,3,4))
atoms=sort(atoms)
write("supercell.vasp", atoms, vasp5=True, direct=True, format='vasp')

print("Initial symmetry at precision 1e-6")
check_symmetry(atoms, 1.0e-6, verbose=True)

calculator = NequIPCalculator.from_deployed_model(model_path="best.pth", device='cuda')

#calculator = NequIPCalculator.from_deployed_model(
#    model_path="best.pth",
#    species_to_type_name = {
#        "Cs": "Cs",
#        "I": "I",
#        "Sn": "Sn",
#    },
#    device='cuda'
#)

atoms_new = opt_with_symmetry(atoms, calculator, fix_symmetry=True, external_strain=False)

# We print out the initial symmetry groups at two different precision levels
print("Final symmetry at precision 1e-6")
check_symmetry(atoms_new, 1.0e-6, verbose=True)
write("POSCAR",atoms_new,format='vasp')


