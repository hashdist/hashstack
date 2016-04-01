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

# ERDC Diamond
ifeq ($(PROTEUS_ARCH),diamond)

  # Default compiler if none provided in command line
  ifeq ($(compiler),)
    compiler := intel
  endif

  ifeq ($(compiler),intel)
    FC          :=  ifort
    PFC         :=  mpif90
    CC          :=  icc
    OPTLVL     := -O2 -axT -Winline -finline-limit=1000
    ifeq ($(TARG_METHOD),dbg)
#     OPTLVL    := -g -traceback
#     OPTLVL    := -g -traceback  -DSTW_DEBUG
      OPTLVL    := -g -traceback -CB -check uninit -fpe0
    endif
    ifeq ($(TARG_METHOD),mdbg)
      OPTLVL    := -g -traceback -CB -check uninit -fpe0  -DSTW_DEBUG
    endif
    COMMON_FLGS := $(OPTLVL) -FR $(PRECISION)  $(EXTRA_FLAGS)
    #COMMON_FLGS := $(OPTLVL) -FR $(PRECISION)  $(EXTRA_FLAGS) -DBDY_DEBUG
    FFLAGS1     := $(COMMON_FLGS)
    FFLAGS2     := $(COMMON_FLGS) -DMPI -DPARALLEL
    #FFLAGS2    := $(COMMON_FLGS) -DMPI -DSEPARATE_SWEEPS
    FFLAGS3     := $(FFLAGS1) -DMPI
    IMODS       := -module
    MSGLIBS     := -lmpi
    ifeq ($(USE_PERF),yes)
      PERFLIBS  := $(EXPANDED_LOCAL_LIB) -lparaperf -lpapi -lperfctr
    endif
  endif

endif



