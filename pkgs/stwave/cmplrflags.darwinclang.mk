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
# Compiler Flags for Mac OSX - Darwin 10.8 Mountain Lion  
#
# ADDED BY:  	  Matt Malej
#
# Last Updated:  January 23, 2013
#

ifeq ($(PROTEUS_ARCH),darwinclang)

  # Default compiler if none provided in command line                                  
  ifeq ($(compiler),)
    compiler    := clang
  endif

  IMODS       := -I
  OPTLVL      := -O2
  ifeq ($(TARG_METHOD),dbg)
    OPTLVL    := -g  -DSTW_DEBUG
  endif
  ifeq ($(TARG_METHOD),mdbg)
    OPTLVL    := -g  -DSTW_DEBUG
  endif

  COMMON_FLGS := $(OPTLVL) $(PRECISION) -ffree-form  $(EXTRA_FLAGS)
  FFLAGS1     := $(COMMON_FLGS) $(PRECISION)
  FFLAGS2     := $(COMMON_FLGS) -DMPI -DPARALLEL $(PRECISION)
  FFLAGS3     := $(FFLAGS1) -DMPI
  EXTRA_OBJS  := $(O_DIR)degree.o $(O_DIR)rindex.o

  ifeq ($(compiler),gcc)
    FC          := gfortran
    PFC		:= /usr/local/bin/mpif90
    CC          := gcc
    CXX		:= g++
    IMODS       := -I
    COMMON_FLGS := -g $(PRECISION) -ffree-form
    FFLAGS1     := $(COMMON_FLGS)
    FFLAGS2     := $(COMMON_FLGS) -DMPI -DPARALLEL
    FFLAGS3     := $(FFLAGS1) -DMPI
  endif

  ifeq ($(compiler),clang)
    FC          := gfortran
    PFC		:= /usr/local/bin/mpif90
    CC          := clang
    CXX         := clang++
    IMODS       := -I
    COMMON_FLGS := -g $(PRECISION) -ffree-form
    FFLAGS1     := $(COMMON_FLGS)
    FFLAGS2     := $(COMMON_FLGS) -DMPI -DPARALLEL
    FFLAGS3     := $(FFLAGS1) -DMPI
  endif
endif
