import subprocess,shlex

def get_python_version():
    with open('pyPRISM/version.py','r') as f:
        exec(f.read(),globals())
    print('==> Got version {} from python.'.format(version))
    return __version__
  
def get_git_version():
    try:
        version = subprocess.check_output(shlex.split('git describe')).strip()
    except subprocess.CalledProcessError:
        version = None
        print('==> Could not get git version')
    else:
        print('==> Got version {} from git repo.'.format(version))
    return version

def write(version,file='pyPRISM/Version.py'):
    with open(file,'w') as f:
      f.write('\n__version__ = \'{}\'\n'.format(version))
      f.write('version = \'{}\'\n'.format(version))
    print('==> Updated version to {} in file: {}'.format(version,file))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Versioning Tools')
    parser.add_argument('--update', 
                        action='store_true',
                        help='Update pyPRISM/version.py')

    args = parser.parse_args()

    py_version = get_python_version()
    git_version = get_git_version()

    if args.update:
        if git_version is not None:
            version = git_version
        else:
            version = py_version
        write(version)
