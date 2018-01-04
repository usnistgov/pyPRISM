import subprocess,shlex

default_version = 'v0.1'
default_short_version = 'v0.1'

def get_python_version():
  print('==> Attempting to get version from module...',)
  try:
    from pyPRISM import Version
  except ImportError:
    print('Failed!')
    version = default_version
    short_version = default_short_version
    print('==> Defaulting to version {}'.format(version))
  else:
    print('Success!')
    version = Version.version
    short_version = Version.short_version
    print('==> Got version {} from Version.py'.format(version))
  return version,short_version

  
def get_git_version():
  print('==> Attempting to get git version...',)
  try:
    version = subprocess.check_output(shlex.split('git describe')).strip()
  except subprocess.CalledProcessError:
    print('Failed!')
    version = default_version
    short_version = default_short_version
    print('==> Defaulting to version {}'.format(version))
  else:
    print('Success!')
    short_version = version.split('-')[0]
    print('==> Got version {} from git repo.'.format(version))
  return version,short_version


def write(version,short_version,file='pyPRISM/Version.py'):
  with open(file,'w') as f:
    f.write('version = \'{}\'\n'.format(version))
    f.write('short_version = \'{}\'\n'.format(short_version))
  print('==> Updated version to {} in file: {}'.format(version,file))


if __name__ == '__main__':
  old_version,old_short = get_python_version()
  new_version,new_short = get_git_version()
  if new_version and new_version!=old_version:
    write(new_version,new_short)
  else:
    print('==> Not modifying file!')
