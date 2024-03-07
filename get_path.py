from os import path
import sys

# Add the parent directory of 'models' to the Python path
models_parent_dir = path.abspath(path.join(path.dirname(__file__), '..', '..'))
print("*******models_parent_dir:\t {}".format(models_parent_dir))

sys.path.append(models_parent_dir)
print("*******path.append:\t {}".format(sys.path.append(models_parent_dir)))

BASE_DIR = path.dirname(path.realpath(__file__))
print("*******BASE_DIR:\t {}".format(BASE_DIR))

GRAND_CHILD_DIR = path.join(BASE_DIR, "api/v1")
print("*******GRAND_CHILD_DIR:\t {}".format(GRAND_CHILD_DIR))
