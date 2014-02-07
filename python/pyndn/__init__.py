# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2014 Regents of the University of California.
# Author: Derek Kulinski <takeda@takeda.tk>
# Author: Jeff Burke <jburke@ucla.edu>
# Author: Jeff Thompson <jefft0@remap.ucla.edu>
# See COPYING for copyright and distribution information.

__all__ = ['interest', 'name']

import sys as _sys

try:
    from pyndn.interest import *
    from pyndn.name import *
except ImportError:
    del _sys.modules[__name__]
    raise
