"""
Generate Moltemplate (.lt) files and corresponding monomer XYZ files for
polymer chains based on a specified segment pattern.

The script reads two command-line arguments:
    1. n (int): Number of repeats of the segment pattern per polymer.
    2. pat (str): A string of digits '1' and '2' representing sticker/spacer beads.

It produces:
    - polyA_n<n>.lt and polyB_n<n>.lt: Moltemplate definitions for A-type and B-type polymers.
    - polyA_n<n>_mono.xyz and polyB_n<n>_mono.xyz: Monomer geometry in XYZ format.

Usage (command line):
    python LT_writer.py <n> <seg_pattern>

Example:
    python LT_writer.py 10 2212212
"""

import sys
import numpy as np


def write_xyz(mol_name: str, bead_sequence: np.ndarray, type_names: dict[int, str]) -> None:
    """
    Write a monomer geometry in XYZ format.

    Args:
        mol_name (str): Base name for the output file (e.g., "polyA_n10").
        bead_sequence (np.ndarray): 1D array of bead types (integers).
        type_names (dict[int, str]): Mapping from bead type integer to atom name.

    Output:
        Creates a file "<mol_name>_mono.xyz" listing coordinates along the x-axis,
        one bead every 5 Å, all with y=z=0.
    """
    xyz_filename = f"{mol_name}_mono.xyz"
    num_beads = len(bead_sequence)

    with open(xyz_filename, 'w') as f:
        f.write(f"{num_beads}\n")
        f.write(f"{mol_name}\n")
        x_pos = 5.0
        for bead in bead_sequence:
            atom_type = type_names.get(int(bead), "X")
            f.write(f"{atom_type}  {x_pos:.3f}  0.000  0.000\n")
            x_pos += 5.0


def write_poly_lt(
    mol_name: str,
    bead_sequence: np.ndarray,
    type_names: dict[int, str],
    mass_map: dict[int, float]
) -> None:
    """
    Write a Moltemplate (.lt) file defining a polymer chain and its connectivity.

    Args:
        mol_name (str): Base name for the Moltemplate file (e.g., "polyA_n10").
        bead_sequence (np.ndarray): 1D array of bead types (integers).
        type_names (dict[int, str]): Mapping from bead type integer to Moltemplate atom name.
        mass_map (dict[int, float]): Mapping from bead type integer to atomic mass.

    Output:
        Creates a file "<mol_name>.lt" defining:
          - Masses for each bead type.
          - Atom definitions and charges (charges are set to 0 by default).
          - Bond definitions between consecutive beads.
          - Angle definitions between triplets of beads.
    """
    lt_filename = f"{mol_name}.lt"
    num_beads = len(bead_sequence)
    atom_ids = np.arange(1, num_beads + 1)

    with open(lt_filename, 'w') as f:
        f.write(f"{mol_name} {{\n\n")

        # Mass definitions
        f.write('write_once("Data Masses") {\n')
        for bead_type, atom_name in type_names.items():
            mass_value = mass_map.get(bead_type, 1.0)
            f.write(f"    @atom:{atom_name}  {mass_value}\n")
        f.write("}\n\n")

        # Atom definitions
        f.write('write("Data Atoms") {\n')
        for i, bead in enumerate(bead_sequence):
            atom_name = type_names.get(int(bead), "X")
            atom_id = atom_ids[i]
            f.write(f"    $atom:{atom_id} $mol:. @atom:{atom_name} 0 0 0 0\n")
        f.write("}\n\n")

        # Bond definitions
        f.write('write("Data Bonds") {\n')
        for i in range(num_beads - 1):
            f.write(f"    $bond:b{i+1} @bond:Bond $atom:{atom_ids[i]} $atom:{atom_ids[i+1]}\n")
        f.write("}\n\n")

        # Angle definitions
        f.write('write("Data Angles") {\n')
        for i in range(num_beads - 2):
            f.write(
                f"    $angle:a{i+1} @angle:Angle "
                f"$atom:{atom_ids[i]} $atom:{atom_ids[i+1]} $atom:{atom_ids[i+2]}\n"
            )
        f.write("}\n\n")

        f.write("}  # End of " + mol_name + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python LT_writer.py <n> <seg_pattern>")
        sys.exit(1)

    _, n_str, pattern_str = sys.argv

    try:
        n = int(n_str)
    except ValueError:
        print(f"Error: <n> must be an integer, got '{n_str}'")
        sys.exit(1)

    # Convert pattern_str into a list of integers
    try:
        segment_pattern = [int(ch) for ch in pattern_str]
    except ValueError:
        print("Error: <seg_pattern> must be a string of digits (e.g. '2212212')")
        sys.exit(1)

    # Flatten to a repeated sequence of length n * len(pattern)
    bead_seq = np.tile(segment_pattern, n)

    # Define A-type polymer
    polyA_name = f"polyA_n{n}"
    type_map_A = {1: "A", 2: "AL"}
    mass_map_A = {1: 1000.0, 2: 1000.0}
    write_poly_lt(polyA_name, bead_seq, type_map_A, mass_map_A)
    write_xyz(polyA_name, bead_seq, type_map_A)

    # Define B-type polymer
    polyB_name = f"polyB_n{n}"
    type_map_B = {1: "B", 2: "BL"}
    mass_map_B = {1: 1000.0, 2: 1000.0}
    write_poly_lt(polyB_name, bead_seq, type_map_B, mass_map_B)
    write_xyz(polyB_name, bead_seq, type_map_B)

    polyC_name = f"polyC_n{n}"
    type_map_C = {1: "C", 2: "CL"}
    mass_map_C = {1: 1000.0, 2: 1000.0}
    write_poly_lt(polyC_name, bead_seq, type_map_C, mass_map_C)
    write_xyz(polyC_name, bead_seq, type_map_C)

    print(f"Generated polymers for segment count={n}, pattern={pattern_str}")
