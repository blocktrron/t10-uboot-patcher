#!/usr/bin/env python3
# pylint: disable=missing-module-docstring
import sys


def replace_password_hash(filename: str):
    """
    Replace the unknown SHA1 password hash for the Watchguard T10 U-Boot with the SHA1
    hash of '1234'
    :param filename:
    """
    sha1_unknown = bytes.fromhex("E597301A1D89FF3F6D318DBF4DBA0A5ABC5ECBEA")
    sha1_1234 = bytes.fromhex("7110EDA4D09E062AA5E4A390B0A572AC0D2C0220")
    uboot_size = 0x90000

    with open(filename, 'rb') as input_file:
        content = input_file.read()

    password_offset = content.find(sha1_unknown)
    if password_offset < 0:
        print("Password hash not found in provided file.")
        sys.exit(1)

    while password_offset > 0:
        if not password_offset < uboot_size:
            print("Password hash found after U-Boot partition. Not replacing password")
            sys.exit(1)
        password_offset = content.find(sha1_unknown, password_offset + 1)

    patched_file = content.replace(sha1_unknown, sha1_1234)

    with open(filename, 'wb') as output_file:
        output_file.write(patched_file)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} filename")
        sys.exit(1)

    replace_password_hash(sys.argv[1])
