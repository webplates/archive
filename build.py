import itertools
from jinja2 import Environment, FileSystemLoader
import os
import shutil
import sys
from helper import *

DIST = "dist"
REPO = "webplates/php"

VERSIONS = ["5.5.38", "5.6.24", "7.0.9"]
BUILDS = ["fpm"]
DISTROS = ["alpine"]

EXCLUSIONS = set(itertools.product(VERSIONS, ["apache"], ["alpine"]))

MATRIX = set(itertools.filterfalse(lambda x: x in EXCLUSIONS, itertools.chain(
    itertools.product(VERSIONS, BUILDS, [None]),
    itertools.product(VERSIONS, [None], DISTROS),
    itertools.product(VERSIONS, [None], [None]),
    itertools.product(VERSIONS, BUILDS, DISTROS)
)))

NODE = ["6.3.1"]

# Prepare Jinja
env = Environment(loader=FileSystemLoader(os.path.dirname(os.path.realpath(__file__))))

# Clear the dist folder
if os.path.isdir(DIST):
    shutil.rmtree(DIST, ignore_errors=True)
os.mkdir(DIST)

paths = []
tags = []

# Build node containers
template = env.get_template('Dockerfile-node.template')

for element in MATRIX:
    for version in NODE:
        docker = template.render(parent=matrix_join(element, "-"), version=version, distro=element[2])
        path = DIST + "/" + matrix_join((minorize(element[0]),) + element[1:] + ("node", minorize(version)), "/")
        dockerfile = path + "/Dockerfile"
        os.makedirs(path, exist_ok=True)
        with open(dockerfile, "w") as f:
            f.write(docker)
        paths.append(path)
        tags.append(set(get_tags(element, itertools.product(["node"], [majorize(version), minorize(version), version]))))

with open(".auth", "r") as f:
    token = f.readline().rstrip()

delete_builds(REPO, token)
add_builds(REPO, token, paths, tags)

FORMAT = "%-35s %s"
print (FORMAT % ("PATH", "TAG"))

for c1, c2 in zip(paths, tags):
    for tag in c2:
        print ("%-35s %s" % (c1, tag))
