import subprocess
import re
from pathlib import Path
import logging
from doit.action import CmdAction
from doit import get_var


DATA_ENCRYPTED = Path("data/raw-private-encrypted")
DATA_PRIVATE = Path("data/raw-private")

SRC_PROCESSING = Path("src/data-processing")

EXT_SCRIPT = {".py", ".R", ".Rmd", ".sh"}

def get_scripts(folder):
    return get_files(folder, EXT_SCRIPT)
    
def get_files(folder, suffix=None):
    if isinstance(suffix, str):
        suffix = [suffix]
    path = Path.cwd()/folder
    if not path.is_dir():
        logging.warning(f"Skipping non-existent path {path}")
        return []
    return [f for f in path.iterdir() if (f.is_file() and ((suffix is None) or (f.suffix in suffix)))]


def parse_files(text):
    return [Path(x.strip()) for x in text.split(",")]

def get_headers(file: Path):
    for i, line in enumerate(open(file)):
        if not line.strip():
            continue
        if not line.startswith("#"):
            break
        if i ==0 and line.startswith("#!"):
            yield "COMMAND", line[2:].strip()
        m = re.match(r"#(\w+?):(.*)", line)
        if m:
            yield m.groups()[0].strip(), m.groups()[1].strip()


def task_install():
    """Install python/R dependencies as needed"""
    packrat = Path("packrat/packrat.lock")
    if packrat.is_file():
        yield {
            'name': f"Install R dependencies using {packrat}",
            'file_dep': [packrat],
            'actions': [f"Rscript -e 'if (!require(packrat)) install.packages(\"packrat\"); packrat::restore()'"]
        }
    requirements = Path("requirements.txt")
    if requirements.is_file():
        lib = Path.cwd()/"src"/"lib"
        yield {
            'name': f"Install python dependencies in virtual environment env from {requirements}",
            'file_dep': [requirements],
            'targets': ['env'],
            'actions': ["python3 -m venv env",
                        "env/bin/pip install -U pip wheel",
                        f"env/bin/pip install -r {requirements}",
                        f'export LIB=`ls env/lib`; echo "{lib}" > "env/lib/$LIB/site-packages/compendium_extra.pth"'],
            'verbosity': 2
        }


def _get_passphrase():
    if get_var('passphrase'):
        return get_var('passphrase')
    return None

def error_cannot_decrypt():
    raise Exception('Cannot decrypt files as no passphrase is given. Use `doit passphrase="Your passphrase"` to specify')

            
def task_decrypt():
    """Decrypt private files from raw-private-encrypted (provide passphrase with `doit passphrase="Your secret"`)"""
    gpg_files = get_files(DATA_ENCRYPTED, ".gpg")
    if gpg_files:
        passphrase = _get_passphrase()
        for inf in gpg_files:
            outf = DATA_PRIVATE/inf.stem
            if passphrase:
                action = f'mkdir -p {DATA_PRIVATE} &&  gpg --batch --yes --passphrase "{passphrase}" -o {outf} -d {inf}'
            else:
                action = error_cannot_decrypt
                

            yield {
                'name': outf,
                'file_dep': [inf],
                'targets': [outf],
                'actions': [action]
            }


def task_process():
    """Run processing scripts from src/data-processing"""
    for file in get_scripts(SRC_PROCESSING):
        headers = dict(get_headers(file))
        if "CREATES" in headers and "COMMAND" in headers:
            target = parse_files(headers["CREATES"])
            inf = parse_files(headers["DEPENDS"]) if "DEPENDS" in headers else None
            action = f"{headers['COMMAND']} {file}"
            if headers.get("PIPE", "F")[0].lower() == "t":
                if inf:
                    action = f"{action} < {inf}"
                action = f"{action} > {target}"
            if file.suffix == ".py":
                # Activate virtual environent before calling script
                action = f"(. env/bin/activate; {action})"
            action = f'{action} && echo "[OK] {file.name} completed" 1>&2'
                
            result = dict(
                basename=f"process:{file.name}",
                targets=target,
                actions=[action],
            )
            if 'DESCRIPTION' in headers:
                result['doc'] = headers['DESCRIPTION']

            if inf:
                result['file_dep'] = inf
            else:
                result['uptodate'] = [True]  # task is up-to-date if target exists
            yield(result)


def do_encrypt(args):
    if args.files:
        files = [Path(x).resolve() for x in  args.files]
        for f in files:
            if not f.parent == DATA_PRIVATE.resolve():
                raise ValueError(f"File {f} not in {DATA_PRIVATE}, so will not be encrypted!")
    else:
        files = get_files(DATA_PRIVATE)
    for file in files:
        outfile = DATA_ENCRYPTED/f"{file.name}.gpg"
        print(f"Encrypting {file} -> {outfile}")
        cmd = ['gpg', '--yes', '--symmetric', '--batch', '--passphrase', args.passphrase, "-o", outfile, file]
        subprocess.check_call(cmd)


if __name__ == '__main__':
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description = "Doit file for data compendium. Run `doit` to generate files and results rather than running this script. As author, you can use this script to generate documentation or encrypt private files. ")

    subparsers = parser.add_subparsers(help='Action to perform')
    
    encrypt = subparsers.add_parser('encrypt', help='Encrypt private files')
    encrypt.add_argument('passphrase', help='Passphrase for encryption')
    encrypt.add_argument('files', nargs="*", help='Files to encrypt (if blank, encrypt all private files)')
    encrypt.set_defaults(func=do_encrypt)

    if len(sys.argv) <= 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        args.func(args)
