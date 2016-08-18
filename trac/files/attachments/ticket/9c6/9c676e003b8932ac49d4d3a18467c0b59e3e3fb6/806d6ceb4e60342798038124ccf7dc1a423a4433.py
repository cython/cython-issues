#!/usr/bin/env python

from puremodeinherit import *

derived = Derived()
print "derived.method():",
print derived.method()  # this one works

base = Base()
print "base.method():",
print base.method()  # this one does not
