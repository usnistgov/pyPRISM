from __future__ import print_function
import io
import os
from IPython.core import magic_arguments
from IPython.core.magic import  (
    Magics, compress_dhist, magics_class, line_magic, cell_magic, line_cell_magic
)

@magics_class
class typyMagics(Magics):
    @cell_magic
    def write_and_run(self, line, cell):
        """Write the contents of the cell to a file.
        
        The file will be overwritten unless the -a (--append) flag is specified.
        """
        self.shell.run_cell(cell)

        args = magic_arguments.parse_argstring(self.writefile, line)
        filename = os.path.expanduser(args.filename)

        if os.path.exists(filename):
            if args.append:
                print("Appending to %s" % filename)
            else:
                print("Overwriting %s" % filename)
        else:
            print("Writing %s" % filename)
        
        mode = 'a' if args.append else 'w'
        with io.open(filename, mode, encoding='utf-8') as f:
            f.write(cell)
