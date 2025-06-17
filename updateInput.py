"""
updateInput.py

Modify a LAMMPS input template file to set correct filenames and colvars references,
and then generate a SLURM submission script.

Usage:
    python updateInput.py <template_input_file> <L>

Where:
    - template_input_file (str): Path to a LAMMPS .in template (e.g., "Template_input.in").
    - L (int): Box half-length (used to name output files).

The script performs:
  1. Replace "variable fName string ..." → "b70_N200_L<L>".
  2. Replace "read_data ..." → "b70_N200_L<L>.data extra/special/per/atom 50".
  3. Replace "fix CV_Rg ..." → "N200_Rg_L<L>.colvars".
  4. Write out "b70_N200_L<L>.in".
  5. Write a SLURM script "submit_b70_N200_L<L>.sh".
"""

import re
import sys


def writeInputFile(file, L):
    """
    Read the LAMMPS input template and substitute the appropriate filenames.

    After substitution, writes the new file "b70_N200_L<L>.in".

    Args:
        file (str): Path to the template .in file.
        L (int): Box half-length to include in filenames.

    Behavior:
      - Locates a line starting with "variable fName string" and replaces
        the value with "b70_N200_L<L>".
      - Locates the "read_data" line and replaces it with
        "read_data b70_N200_L<L>.data extra/special/per/atom 50".
      - Locates the "fix CV_Rg all colvars" line and replaces it with
        "fix CV_Rg all colvars N200_Rg_L<L>.colvars output ${fName}".
    """
    lines = []
    with open(file, 'r') as tf:
        lines = tf.readlines()
        for i, line in enumerate(lines):
            if re.search('variable fName string', line):
                lines[i] = f'variable fName string b70_N200_L{L} \n'

            if re.search('read_data', line):
                lines[i] = f'read_data b70_N200_L{L}.data extra/special/per/atom 50 \n'

            if re.search('fix CV_Rg all colvars', line):
                lines[i] = (
                    f'fix CV_Rg all colvars N200_Rg_L{L}.colvars'
                    ' output ${fName} \n'
                )

    with open(f'b70_N200_L{L}.in', 'w') as tmf:
        tmf.writelines(lines)


def writeSubmitScript(L):
    """
    Generate a SLURM submission script named "submit_b70_N200_L<L>.sh" for LAMMPS.

    The submission script requests:
      - Job name: L<L>_b70
      - 28 MPI tasks
      - Walltime: 3 days
      - Partition: sapphire
      - 400 MB per CPU
      - Output to "%x_%j.out" and error to "%x_%j.err"
      - Email to name@organization.edu on job END

    Args:
        L (int): Box half-length (used to form input filename and job name).
    """
    infile = f'b70_N200_L{L}.in'

    with open(f'submit_b70_N200_L{L}.sh', 'w') as tf:
        tf.write('#!/bin/bash\n')
        tf.write(f'#SBATCH --job-name=L{L}_b70\n')
        tf.write(f'#SBATCH -n  28\n')
        tf.write('#SBATCH -t 3-00:00:00 # DD-HH:MM:SS\n')
        tf.write('#SBATCH -p sapphire\n')
        tf.write(f'#SBATCH --mem-per-cpu=400\n')
        tf.write('#SBATCH -o %x_%j.out\n')
        tf.write('#SBATCH -e %x_%j.err\n')
        tf.write('#SBATCH --mail-type=END\n')
        tf.write('#SBATCH --mail-user=name@organization.com\n\n')
        tf.write('module load gcc/12.2.0-fasrc01 openmpi/4.1.4-fasrc01\n\n')
        tf.write(
            f'srun -n $SLURM_NTASKS --mpi=pmix '
            f'/n/home00/dkanovich/lammps-5Jun19/src/lmp_mpi -in {infile} \n'
        )


if __name__ == "__main__":
    _, file, L = sys.argv
    writeInputFile(file, L)
    writeSubmitScript(L)
