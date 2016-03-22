# $Id: cmplrflags.mk 943 2010-01-29 15:32:02Z vparr $
########################################################################
#Convert LOCAL_LIBRARY to EXPANDED_LOCAL_LIB
########################################################################

EXPANDED_LOCAL_LIB := $(subst :, ,   $(LOCAL_LIBRARY))
EXPANDED_LOCAL_LIB := $(strip        $(EXPANDED_LOCAL_LIB))
EXPANDED_LOCAL_LIB := $(foreach dir, $(EXPANDED_LOCAL_LIB), -L$(dir))
EXPANDED_LOCAL_LIB := $(subst //,/,  $(EXPANDED_LOCAL_LIB))

########################################################################
#Convert LOCAL_INCLUDE to EXPANDED_LOCAL_INC
########################################################################

EXPANDED_LOCAL_INC := $(subst :, ,      $(LOCAL_INCLUDE))
EXPANDED_LOCAL_INC := $(strip           $(EXPANDED_LOCAL_INC))
EXPANDED_LOCAL_INC := $(foreach dir,    $(EXPANDED_LOCAL_INC), -I$(dir))
EXPANDED_LOCAL_INC := $(subst //,/,     $(EXPANDED_LOCAL_INC))

PRECISION = -DUSE_DOUBLE
DEBUG     = -DDEBUG_PRINTING

ifneq ($(TARG_COMPILER),)
  compiler := $(TARG_COMPILER)
endif

ifeq ($(TARG_METHOD),)
  TARG_METHOD := $(METHOD)
  ifeq ($(TARG_METHOD),)
    TARG_METHOD := opt
  endif
endif

OPTNAME := $(TARG_METHOD)
ifneq (,$(TARGET))
  OPTNAME := $(TARGET)
endif


ifneq (,$(findstring SEPARATE_SWEEPS,$(TARGET)))
  EXTRA_FLAGS := -DSEPARATE_SWEEPS
endif



########################################################################
# Compiler Flags of Diamond on ERDC DSRC system
#
# ADDED BY:	Matt Malej
#
# Last Updated:	January 30, 2013

ifeq ($(PROTEUS_ARCH),hpc_util)

  # Default compiler if none provided in command line
  ifeq ($(compiler),)
    compiler := utils
  endif

  # ERDC Utility Server using standard compilers
  ifeq ($(compiler),utils)
    FC          :=  pgf90
    PFC         :=  mpif90
    CC          :=  pgcc
    CFLAGS      := 
    OPTLVL      := -fastsse -Minline=name:prop:splint:wkfnc
#   OPTLVL    := -gopt -O0  -C -Ktrap=fp -Minline=name:prop:splint:wkfnc
    ifeq ($(TARG_METHOD),dbg)
      OPTLVL    := -gopt -O0 -Minline=name:prop:splint:wkfnc -DSTW_DEBUG
    endif
    ifeq ($(TARG_METHOD),mdbg)
      OPTLVL    := -gopt -O0  -C -Ktrap=fp -Minline=name:prop:splint:wkfnc -DSTW_DEBUG
    endif
    COMMON_FLGS := $(OPTLVL) -Mfree $(EXTRA_FLAGS)
    FFLAGS1     := $(COMMON_FLGS) $(PRECISION)
    FFLAGS2     := $(COMMON_FLGS) -DMPI -DPARALLEL $(PRECISION)
    FFLAGS3     := $(FFLAGS1) -DMPI
    CFLAGS      := 
    IMODS       := -module
    MSGLIBS     :=
  endif

endif



