from argparse import ArgumentParser
from os import getcwd


def IncrementProjectVersion(file):

    with open(file, "w") as configuration_file:
        config = configuration_file.readlines()

    for line in config: