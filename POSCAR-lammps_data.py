from ase.io import read, write
from ase.io.espresso import read_espresso_out
from ase.visualize import view
from ase.io.lammpsdata import write_lammps_data
from ase.build import bulk
from ase.build.tools import sort

out_filename = './structure.data'
in_filename = './POSCAR_init'

atoms=read("POSCAR_init",format='vasp')
atoms=atoms.repeat((4,3,4))
all_atoms=sort(atoms)

#all_atoms = read(in_filename, index='-1')
#write(out_filename, all_atoms, append=False, format='vasp', vasp5=True, direct=True)

#write_lammps_data(out_filename, all_atoms, atom_style = 'full', force_skew=True, units='metal')
write_lammps_data(out_filename, all_atoms, units='metal')

view(all_atoms)
