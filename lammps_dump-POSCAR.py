from ase.io import read, write
from ase.io.espresso import read_espresso_out
from ase.visualize import view

in_filename = './output.dump'
out_filename = './POSCAR_final'

all_atoms = read(in_filename, format='lammps-dump-text', index='-1')
write(out_filename, all_atoms, append=False, format='vasp', vasp5=True, direct=True)
view(all_atoms)
