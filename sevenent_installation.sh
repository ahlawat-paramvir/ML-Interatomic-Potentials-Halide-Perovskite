srun -p k2-gpu-interactive -N 1 -n 1 --gres gpu:a100:1 --time=3:00:00 --mem=20G --pty bash
# load modules
module load compilers/gcc/9.3.0
module load mpi/openmpi/4.1.1/gcc-9.3.0
module load libs/atlas/3.10.3/gcc-9.3.0
module load apps/cmake/3.25.1/gcc-9.3.0
godule load libs/nvidia-cuda/11.8.0/bin
module load apps/intel-basekit/2021.1-beta09
module load mkl/latest
module load apps/anaconda3/2021.05/bin

conda create -n sevennet
source activate sevennet

# install pytorch with matching cuda (11.7, 11.8 or 12.3) on kelvin
pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu118
pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.3.0+cu118.html
pip install torch_geometric

#pip install torch-scatter -f https://data.pyg.org/whl/torch-2.3.0+cu118.html

# install sevennet 
git clone https://github.com/MDIL-SNU/SevenNet.git
cd SevenNet
path_to_SevenNet_root=$(pwd)
pip install .

# Ensure the LAMMPS version (stable_2Aug2023). You can easily switch the version using git.
git clone https://github.com/lammps/lammps.git lammps_dir
cd lammps_dir
path_to_lammps_dir=$(pwd)
git checkout stable_2Aug2023

#Run patch_lammps.sh
cd ${path_to_SevenNet_root}
sh patch_lammps.sh ${path_to_lammps_dir}

#Build LAMMPS with cmake
cd ${path_to_lammps_dir}
mkdir build
cd build

# export following libraries required during lammps installation
export LD_LIBRARY_PATH=/users/pahlawat/.conda/envs/sevennet/lib/python3.10/site-packages/nvidia/nccl/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/users/pahlawat/.conda/envs/sevennet/lib/python3.10/site-packages/nvidia/cudnn/lib/:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/users/pahlawat/.conda/envs/sevennet/lib/python3.10/site-packages/nvidia/cuda_cupti/lib/:$LD_LIBRARY_PATH

cmake -D CMAKE_BUILD_TYPE=Release     -D CMAKE_INSTALL_PREFIX=$(pwd)  -D BUILD_OMP=yes     -D BUILD_SHARED_LIBS=yes     -D LAMMPS_EXCEPTIONS=yes     -D PKG_EXTRA-PAIR=yes     -D PKG_EXTRA-DUMP=yes     -D PKG_MOLECULE=yes     -D PKG_EXTRA-FIX=yes     -D CMAKE_PREFIX_PATH="`python3 -c 'import torch;print(torch.utils.cmake_prefix_path)'`"     -D MKL_INCLUDE_DIR=`python3 -c "import sysconfig;from pathlib import Path;print(Path(sysconfig.get_paths()[\"include\"]).parent)"` -D CUDA_TOOLKIT_ROOT_DIR=/opt/gridware/depots/54e7fb3c/el7/pkg/libs/nvidia-cuda/11.8.0/bin/  -D Python_EXECUTABLE=$(which python3)  ../cmake

make -j8
