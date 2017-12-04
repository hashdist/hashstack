# HashStack <#>
[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/hashdist/hashstack?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

HashStack is a collection of software profiles that builds on various architectures (Linux, Windows, Mac, clusters, ...) and allows optional reuse of system-wide packages (compilers, LAPACK, Python, ...).

To build these profiles, you need the [hit](https://github.com/hashdist/hashdist) tool from HashDist.
Read [hit's documentation](http://hashdist.readthedocs.org/) about how to use it.

## Usage

### Install Hashdist

Make sure the `hit` tool is in your path. For example if your `~/bin` directory is in `$PATH`, you can do:
```
cd repos
git clone https://github.com/hashdist/hashdist
cd ~/bin
ln -s ~/repos/hashdist/bin/hit .
```
or you can execute in the `hashdist` directory: ``export PATH=`pwd`/bin:$PATH`` (but then you need to put this commnand somewhere in your `.bashrc` or reexecute it by hand each time).

Now you can initialize HashDist with the following command:

```
hit init-home
```

### Use Hashstack

This will install one particular profile:
```
git clone https://github.com/hashdist/hashstack
cd hashstack
cp cloud.sagemath.yaml default.yaml
hit build
```
You can now for example run the IPython Notebook as follows:
```
./default/bin/ipython notebook
```

### Conda Python in Hashstack (experimental)

The recipe for Python supports a conda based version of Python. Using
a conda based version of Python allows using conda to install packages
in the profile while in develop mode.


#### Specifying the conda installation to use

When using conda python, supply the path for the conda installation to
use using the "conda_prefix" parameter. This should be the place where
conda (anaconda or miniconda) was installed. The conda executable to use
will be <conda-prefix>/bin/conda.


#### Using the conda version of Python

In your profile file use, use "conda: true" in the python package:

```
packages:
  python:
    conda: true
	pyver: '2.7'
```

The pyver will be used to select which version of python to install
(as would without conda). Supported versions for conda are 2.7, 3.3,
3.4, 3.5 and 3.6.


#### Installing conda packages inside your profile (in develop mode)

Just use conda install with the '-p' parameter pointing to the profile
in question.

Bear in mind that conda automatically handles dependencies, and that
conda might not be aware of software installed in your profile that
has not been installed by conda.

For example, to install NumPy into a profile linked as "default":

```
conda install -p default numpy
```


