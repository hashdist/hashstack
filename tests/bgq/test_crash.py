import os, pickle
import numpy
import numpy as np
from numpy.testing import *
from numpy.compat import asbytes
import datetime

print "step 1"
a = np.array(['2011-03-16', '1920-01-01', '2013-05-19'], dtype='M')
print "step 2"
assert_equal(str(a), "['2011-03-16' '1920-01-01' '2013-05-19']")

print "step 3"
a = np.array(['2011-03-16T13:55Z', '1920-01-01T03:12Z'], dtype='M')

print "step 4"
assert_equal(np.array2string(a, separator=', ',
                             formatter={'datetime': lambda x :
                                            "'%s'" % np.datetime_as_string(x, timezone='UTC')}),
             "['2011-03-16T13:55Z', '1920-01-01T03:12Z']")
