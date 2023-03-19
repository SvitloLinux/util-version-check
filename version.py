import subprocess
import string
import sys

from packaging import version as VER

__title__ = "critical development tools"
__summary__ = "Tools script to list version numbers of critical development tools"
__uri__ = "https://github.com/SvitloLinux/util-version-check"
__version__ = "0.1"
__author__ = "Yurii Kachaniuk - Ukraine"
__email__ = "wku@ukr.net"
__license__ = "BSD-2-Clause or Apache-2.0"
__copyright__ = "2023 %s" % __author__




def clear(s):
    s = s.replace("\n", "  ")
    whitelist = string.ascii_letters + string.digits + ' ' + "-."
    new_s = ''.join(c for c in s if c in whitelist)
    return new_s


def version(name: str, cmd: str, min: str, max: str, patern: str, m: str):
    sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    rc = sp.wait()
    o, e = sp.communicate()

    def r1(cmd: str, min: str, max: str, patern: str, info: str, m: str):
        info = clear(info)
        rez = eval(patern)(info).strip()
        if type(rez) == list:
            print(f"list {rez=}")
            sys.exit(1)

        rez = rez.strip()
        if m == ">":
            z = VER.parse(rez) > VER.parse(min)
        else:
            z = VER.parse(rez) < VER.parse(min)

        print(f"Name {name}, version: {rez}, min: {min}, max: {max}| ", rez, m, min, " |", z)
        return z, name

    if rc == 0:
        if bool(o) == True:
            return r1(cmd, min, max, patern, o, m)
        if bool(e) == True:
            return r1(cmd, min, max, patern, e, m)
    else:
        print(f"error {cmd=}: ", e)
        return False, name


D = [
    {"name": "perl", "cmd": "perl -V:version", "min": "5.8.8", "max": None, "patern": "lambda x: x.split('version')[1]",
     "m": ">"},
    {"name": "gzip", "cmd": "gzip --version", "min": "1.3.12", "max": None, "patern": "lambda x: x.split()[1]",
     "m": ">"},
    {"name": "ld", "cmd": "echo -n 'Binutils: '; ld --version | head -n1 | cut -d' ' -f3-", "min": "2.14", "max": None,
     "patern": "lambda x: x.split()[5]", "m": ">"},
    {"name": "java", "cmd": "java -version", "min": "10.0.18", "max": None, "patern": "lambda x: x.split()[2].strip()",
     "m": ">"},
    {"name": "chown", "cmd": "chown --version", "min": "6.9", "max": None, "patern": "lambda x: x.split()[3]",
     "m": ">"},
    {"name": "linux", "cmd": "cat /proc/version | head -n1", "min": "5.10.0", "max": None,
     "patern": "lambda x: x.split()[2].split('-')[0]", "m": ">"},
    {"name": "ld", "cmd": "ld -v", "min": "2.14", "max": None, "patern": "lambda x: x.split()[-1]", "m": ">"},
    {"name": "diff", "cmd": "diff --version", "min": "2.8.1", "max": None, "patern": "lambda x: x.split()[3]",
     "m": ">"},
    {"name": "find", "cmd": "find --version", "min": "4.2.31", "max": None, "patern": "lambda x: x.split()[3]",
     "m": ">"},
    {"name": "gawk", "cmd": "gawk --version", "min": "4.0.1", "max": None, "patern": "lambda x: x.split()[2]",
     "m": ">"},
    {"name": "gcc", "cmd": "gcc --version", "min": "9.3.0", "max": "12.2.0", "patern": "lambda x: x.split()[3]",
     "m": ">"},
    {"name": "g++", "cmd": "g++ --version", "min": "9.3.0", "max": "12.2.0", "patern": "lambda x: x.split()[3]",
     "m": ">"},
    {"name": "grep", "cmd": "grep --version", "min": "2.5.1a", "max": None, "patern": "lambda x: x.split()[3]",
     "m": ">"},
    {"name": "m4", "cmd": "m4 --version", "min": "1.4.10", "max": None, "patern": "lambda x: x.split()[3]", "m": ">"},
    {"name": "make", "cmd": "make --version", "min": "4.0", "max": None, "patern": "lambda x: x.split()[2]", "m": ">"},
    {"name": "patch", "cmd": "patch --version", "min": "2.5.4", "max": None, "patern": "lambda x: x.split()[2]",
     "m": ">"},
    {"name": "python", "cmd": "python --version", "min": "2.0", "max": None, "patern": "lambda x: x.split()[1]",
     "m": ">"},
    {"name": "python3", "cmd": "python3 --version", "min": "3.7", "max": None, "patern": "lambda x: x.split()[1]",
     "m": ">"},
    {"name": "sed", "cmd": "sed --version", "min": "4.1.5", "max": None, "patern": "lambda x: x.split()[3]", "m": ">"},
    {"name": "tar", "cmd": "tar --version", "min": "1.22", "max": None, "patern": "lambda x: x.split()[3]", "m": ">"},
    {"name": "makeinfo", "cmd": "makeinfo --version", "min": "4.7", "max": None, "patern": "lambda x: x.split()[3]",
     "m": ">"},
    {"name": "bison", "cmd": "bison --version", "min": "3.5.0", "max": None, "patern": "lambda x: x.split()[3]",
     "m": ">"},
]

if __name__ == '__main__':
    print("#" * 70)
    for i in D:
        a, b = version(**i)
        if not a:
            print("NOT Success", b)
            sys.exit(1)
    print("#" * 70)
    print(" Success")
