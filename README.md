# Hashstack <#>

Hashstack is a collection of software profiles that builds on various architectures (Linux, Windows, Mac, clusters, ...) and allows optional reuse of system-wide packages (compilers, Lapack, Python, ...).

To build these profiles, you need the [hit](https://github.com/hashdist/hashdist) tool from Hashdist.
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

### Use Hashstack

This will install one particular profile:
```
git clone https://github.com/hashdist/hashstack2
cd hashstack2
cp cloud.sagemath.yaml default.yaml
hit build
```
You can now for example run the IPython Notebook as follows:
```
default/bin/ipython notebook
```
