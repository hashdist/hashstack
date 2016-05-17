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


  # Default compiler if none provided in command line
  ifeq ($(compiler),)
    compiler 	:= gcc
  endif

  ifeq ($(compiler),intel)
    CC	        :=  icc
    FC	        :=  ifort
    PFC	        :=  mpif90

    OPTLVL      := -O2 #-axT
    ifeq ($(TARG_METHOD),dbg)
      OPTLVL    := -g -traceback -DSTW_DEBUG
    endif
    ifeq ($(TARG_METHOD),mdbg)
      OPTLVL    := -g -traceback -CB -check uninit -fpe0 -DSTW_DEBUG
    endif
    COMMON_FLGS := $(OPTLVL) -FR $(PRECISION)  $(EXTRA_FLAGS)
    FFLAGS1	:= $(COMMON_FLGS)
    FFLAGS2	:= $(COMMON_FLGS) -DMPI -DPARALLEL
    FFLAGS3     := $(FFLAGS1) -DMPI
    IMODS	:=  -module
    MSGLIBS	:=
    ifeq ($(USE_PERF),yes)
      PERFLIBS	:= $(EXPANDED_LOCAL_LIB) -lparaperf -lpapi -lperfctr
    endif
  endif

  ifeq ($(compiler),gcc)
    FC          := gfortran
    CC          := gcc
    CXX		:= g++
    PFC		:= mpif90

    IMODS       := -I
    COMMON_FLGS := -g $(PRECISION) -ffree-form
    FFLAGS1     := $(COMMON_FLGS)
    FFLAGS2	:= $(COMMON_FLGS) -DMPI -DPARALLEL
    FFLAGS3     := $(FFLAGS1) -DMPI
  endif	

