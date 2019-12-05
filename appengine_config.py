"""`appengine_config` gets loaded when starting a new application instance."""
import sys
import os.path
# add `lib` subdirectory to `sys.path`, so our `main` module can load
# third-party libraries.
from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder.
#vendor.add('lib')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
