#! /usr/bin/env python
import os

#set convenience variables for proteus
prefix           = os.getenv('ARTIFACT')
#define adh-specific variables that are needed
adh_dir          = os.getenv('PWD')
#adh requires parmetis 3.2
parmetis_dir     = os.getenv('PARMETIS_DIR') #'adh-ParMetis-3.2.0')
#adh requires UMFPACK 3.2
#umfpack_dir      = os.getenv('UMFPACK_DIR') #'adh-UMFPACK3.2')

CMAKE = 'cmake' #os.path.join(proteus,proteus_arch,'bin','cmake')

print os.path.join(os.getenv('MPI_DIR'),'lib')

adh_config_variables = {'MPI_LIBRARY':os.path.join(os.getenv('MPI_DIR'),'lib'),
                        'CMAKE_C_COMPILER':os.getenv('MPICC'),
                        'CMAKE_CXX_COMPILER':os.getenv('MPICXX'),
                        'CMAKE_Fortran_COMPILER':os.getenv('MPIF90'),
                        'BUILD_PRE_ADH':'ON',
                        'CMAKE_BUILD_TYPE':'Debug',
                        'DEBUG_LEVEL':'1',
                        'OUTPUT_FILE_FORMAT':'XMS',
                        'USE_PACKAGE_MPI':'OFF',
                        'USE_PACKAGE_PARMETIS':'OFF',
                        'USE_PACKAGE_UMFPACK':'OFF',
                        '_ADH_SEDIMENT':'OFF',
#                        'UMFPACK_INCLUDE_DIR':os.path.join(umfpack_dir),
#                        'UMFPACK_LIBRARY':os.path.join(umfpack_dir, 'umfpack.a'), #'libumfpack.a'),
                        'METIS_INCLUDE_DIR':os.path.join(parmetis_dir,'METISLib'),
                        'METIS_LIBRARY':os.path.join(parmetis_dir,'libmetis.a'),
                        'PARMETIS_LIBRARY':os.path.join(parmetis_dir,'libparmetis.a'),
                        'PARMETIS_INCLUDE_DIR':os.path.join(parmetis_dir),
                        }

def configure_preadh():
    print "configure pre_adh",os.path.join(os.getenv('MPI_DIR'),'lib')

    adh_config_variables['BUILD_PRE_ADH']       ='ON'
    adh_config_variables['USE_PACKAGE_MPI']     ='OFF'
    adh_config_variables['USE_PACKAGE_PARMETIS']='OFF'

    from string import Template
    temp = "{cmake} ".format(cmake=CMAKE)
    for key,val in adh_config_variables.iteritems():
        temp += " -D{name}=${name} ".format(name=key)
    #
    temp += " .."
    command_temp = Template(temp)

    command = command_temp.substitute(adh_config_variables)

    return command

def configure_adh():
    print "configure adh",os.path.join(os.getenv('MPI_DIR'),'lib')

    adh_config_variables['BUILD_PRE_ADH']       ='OFF'
    adh_config_variables['USE_PACKAGE_MPI']     ='OFF'
    adh_config_variables['USE_PACKAGE_PARMETIS']='ON'
    adh_config_variables['USE_PACKAGE_UMFPACK'] ='OFF'
    adh_config_variables['MPI_LIBRARY'] = os.path.join(os.getenv('MPI_DIR'),'lib'),

    from string import Template
    temp = "{cmake} ".format(cmake=CMAKE)
    for key,val in adh_config_variables.iteritems():
        temp += " -D{name}=${name} ".format(name=key)
    #
    temp += " .."
    command_temp = Template(temp)

    command = command_temp.substitute(adh_config_variables)

    return command

if __name__ == '__main__':
    import optparse, sys

    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("--pre-adh",
                      help="configure pre-adh",
                      action="store_true",
                      dest="pre_adh",
                      default=False)
    parser.add_option("-V","--verbose",
                      help="print out some information about what's being attempted",
                      action="store_true",
                      default=False)

    (opts,args) =parser.parse_args()

    import subprocess

    echo = opts.verbose
    print "opts.pre_adh",opts.pre_adh
    if opts.pre_adh:
        #first build pre_adh
        command = configure_preadh()
        build_dir = os.path.join(adh_dir,'build_preadh')
        if echo:
            print "Trying to configure pre_adh with {command} ".format(command=command)
    else:
        command = configure_adh()
        build_dir = os.path.join(adh_dir,'build')
        if echo:
            print "Trying to configure adh with {command} ".format(command=command)

    if not os.path.exists(build_dir):
        os.mkdir(build_dir)
    os.chdir(build_dir)


    fail = subprocess.call(command.split())

    if echo:
        print "configure returned fail = {0} ".format(fail)
    
    sys.exit(fail)

