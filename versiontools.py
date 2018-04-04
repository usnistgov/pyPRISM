import subprocess,shlex

default_path = './pyPRISM/version.py'
def get_version(version_path = default_path):
    py_version = get_python_version(version_path)
    git_version = get_git_version()

    if git_version is not None:
        print('==> Using git version')
        version = git_version
    else:
        print('==> Using python version')
        version = py_version

    return version

def get_python_version(version_path = default_path):
    with open(version_path,'r') as f:
        exec(f.read(),globals())
    print('==> Got version {} from python.'.format(version))
    return str(__version__)
  
def get_git_version():
    try:
        version = subprocess.check_output(shlex.split('git describe --dirty'))
        version = version.strip()
        version = version.decode('utf-8')
    except subprocess.CalledProcessError:
        version = None
        print('==> Could not get git version')
    else:
        print('==> Got version {} from git repo.'.format(version))
    return version

def write(version,file='pyPRISM/version.py'):
    with open(file,'w') as f:
      f.write('__version__ = \'{}\'\n'.format(version))
      f.write('version = \'{}\'\n'.format(version))
    print('==> Updated version to {} in file: {}'.format(version,file))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Versioning Tools')
    parser.add_argument('--update', 
                        action='store_true',
                        help='Update pyPRISM/version.py')

    args = parser.parse_args()

    version = get_version()

    if args.update:
        write(version)
