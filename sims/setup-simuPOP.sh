conda config --add channels conda-forge
conda update -q conda
conda info -a
if [[ ! -d "/opt/conda/envs/ftprime-benchmark" ]] ; then
	conda create -q -n ftprime-benchmark python=3.5
fi
wget https://raw.githubusercontent.com/ashander/ftprime/5ad8bcb3a49a19c9cfd52bdf615140af6f83d218/environment.yml
conda env update -q -n ftprime-benchmark -f environment.yml
source activate ftprime-benchmark
pip install --editable=git+https://github.com/ashander/ftprime.git@master#egg=ftprime
