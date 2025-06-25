"""
Compute the radius of gyration (Rg) from a Packmol-generated XYZ file,
and update a colvars template file accordingly. The script reads:
1. xyz_file       : Packmol output XYZ (e.g., "IC_tmp.xyz")
2. colvars_template: Path to a template .colvars file (e.g., "N400_Rg_L700.colvars")
3. L              : Box half-length (integer)
4. n              : Number of repeats of the segment pattern
5. NA             : Number of A-type chains
6. NB             : Number of B-type chains
7. seg_pattern    : Segment pattern string (e.g., "2212212")

It writes out a new colvars file named "N200_Rg_L<L>.colvars".
"""

import numpy as np
import sys
import re
import math
from numpy import mean, sqrt, array 


def calc_RadGy(posArr):
    """
    Compute the center of mass and radius of gyration (Rg) for a set of positions.

    Args:
        posArr (np.ndarray): An (N,3) array of atomic coordinates.

    Returns:
        tuple:
        - com (np.ndarray): A length-3 array representing the center-of-mass.
        - Rg (float): The radius of gyration (Å).
    """
    com = mean(posArr, axis=0)
    Rg2 = mean(np.sum((posArr - com) ** 2, axis=1))
    return com, sqrt(Rg2)


def parseXYZfile(file):
    """
    Read a Packmol-generated XYZ file and return an (N,3) array of float coordinates.

    The first two lines (atom count and comment) are skipped; parsing begins at line 3.

    Args:
        file (str): Path to the XYZ file.

    Returns:
        np.ndarray: An (N,3) array of floating-point coordinates.
    """
    with open(file, 'r') as tf:
        lines = tf.readlines()

    tmp_arr = array([line.split() for line in lines[2:]])
    return tmp_arr[:, 1:].astype(np.float32)


def fixAtomNumbers(n, NA, NB, seg):
    """
    Construct the 'atomNumbers' line for the colvars file, listing atom indices at half-chain boundaries.

    Each polymer chain has length len(seg) * n. We insert a number for every half-chain.

    Args:
        n (int): Number of repeats of the segment pattern per chain.
        NA (int): Number of A-type chains.
        NB (int): Number of B-type chains.
        seg (list[int]): List of bead types (e.g., [2,2,1,2,2,1,2]).

    Returns:
        str: A formatted "atomNumbers { ... }" string with newline.
    """
    chainLen = len(seg) * int(n)
    numAtoms = chainLen * (int(NA) + int(NB))
    indices = []
    step = chainLen // 2
    for idx in range(step, numAtoms + 1, step):
        indices.append(str(idx))
    return "            atomNumbers {" + " ".join(indices) + "}\n"


def getBoxDim(posArr):
    """
    Compute the extents (x_length, y_length, z_length) of the bounding box from given positions.

    Args:
        posArr (np.ndarray): An (N,3) array of coordinates.

    Returns:
        tuple[int, int, int]: (x_length, y_length, z_length), each rounded to nearest integer.
    """
    x, y, z = posArr[:, 0], posArr[:, 1], posArr[:, 2]
    return round(max(x) - min(x)), round(max(y) - min(y)), round(max(z) - min(z))


def updateCV(cvfile, Rg, L, n, NA, NB, seg):
    """
    Read a colvars template file, adjust Rg-dependent parameters, and write a new colvars file.

    Replacements performed:
    - 'upperBoundary' → Rg + 10
    - 'upperWalls'    → Rg + 5
    - 'atomNumbers'   → newly generated line via fixAtomNumbers()

    Args:
        cvfile (str): Path to the template .colvars file.
        Rg (float): Computed radius of gyration.
        L (str or int): Box half-length (used in output filename).
        n (str or int): Number of repeats of the segment pattern.
        NA (str or int): Number of A-type chains.
        NB (str or int): Number of B-type chains.
        seg (str): Segment pattern string (e.g., "2212212").

    Writes:
        "N200_Rg_L<L>.colvars" with updated boundary and atomNumbers lines.
    """
    Rg = int(round(Rg))

    with open(cvfile, 'r') as tf:
        lines = tf.readlines()

    for i, line in enumerate(lines):
        if re.search('upperBoundary', line):
            lines[i] = f"    upperBoundary {Rg + 10}\n"
        if re.search('upperWalls', line):
            lines[i] = f"    upperWalls {Rg + 5}\n"
        if re.search('atomNumbers', line):
            lines[i] = fixAtomNumbers(n, NA, NB, seg)

    ofile = f"N200_Rg_L{L}.colvars"
    with open(ofile, 'w') as tmpf:
        tmpf.writelines(lines)


if __name__ == "__main__":
    _, xyzFile, cvfile, L, n, NA, NB, seg = sys.argv

    posArr = parseXYZfile(xyzFile)
    com, Rg = calc_RadGy(posArr)
    updateCV(cvfile, Rg, L, n, NA, NB, seg)

    print()
    print("File: ", xyzFile)
    print(f"RadGy ~ {int(round(Rg))} A")
    print("Dimension length (x,y,z): ", getBoxDim(posArr))
