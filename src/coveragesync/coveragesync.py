import configparser
from typing import List

import setuptools


def fun_test() -> None:
    """Super powerful docstring"""
    modules = setuptools.find_packages("./src")

    print("\n".join(modules))

    with open(".gitignore", "r") as ignore_file:
        ignore_string = ignore_file.read()

    ignore_list = [line for line in ignore_string.split("\n") if line]

    print(ignore_list)

    config = configparser.ConfigParser()
    print(config.sections())
    config.read("setup.cfg")
    print(config.sections())
    print(config.get("coverage:run", "source_pkgs"))


def find_packages() -> List[str]:
    """Read the setup.cfg and return packages"""
    section = "options.packages.find"
    setup_config = configparser.ConfigParser()
    setup_config.read("setup.cfg")

    where = setup_config.get(section, "where", fallback=".")
    exclude = multi_to_list(setup_config.get(section, "exclude", fallback=""))
    include = multi_to_list(setup_config.get(section, "include", fallback="*"))

    # print(f"where: {where} | exclude: {exclude} | include: {include}")

    return setuptools.find_packages(where, exclude, include)


def multi_to_list(instr: str) -> List[str]:
    """Convert multi-line config values to list"""
    return [line.strip() for line in instr.split("\n") if line]


def update_coverage(package_list: List[str]) -> bool:
    """Updates (if exists) the coverage config to include package sources"""
    section = "coverage:run"
    setup_config = configparser.ConfigParser()
    setup_config.read("setup.cfg")

    # TODO: If section exists check

    current = multi_to_list(setup_config.get(section, "source_pkgs", fallback=""))

    new_list = sorted(package_list)
    changed = current != new_list

    setup_config.set(section, "source_pkgs", "\n" + "\n".join(new_list))

    with open("setup_new.cfg", "w") as configfile:
        setup_config.write(configfile)

    return changed


if __name__ == "__main__":
    changed = update_coverage(find_packages())
    print(f"Changes: {changed}")
