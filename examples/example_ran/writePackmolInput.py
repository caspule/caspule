# arguments - n (segment count), NA (count of A-polymer), NB, Box Length (L), input fileName, xyz output filename
import sys 
import numpy as np

def generate_packmol_input(n, NA, NB, L, inp_file, outfile):
    """
    Generate a Packmol input script that places NA A-chains and NB B-chains in a cube of half-length L.
    """
    seed = np.random.randint(1, 100000)
    
    L = L-10 
    
    with open(f'{inp_file}', 'w') as tf:
        tf.write('tolerance  10\n')
        tf.write(f'seed             {seed}\n\n')
        tf.write('filetype xyz\n')
        tf.write(f'output  {outfile}\n\n')

        tf.write(f'structure polyA_n{n}_mono.xyz\n')
        tf.write(f'\tnumber {NA}\n')
        tf.write(f'\tinside box  {-L}  {-L} {-L}  {L} {L} {L}\n')
        tf.write('end structure\n\n')

        tf.write(f'structure polyB_n{n}_mono.xyz\n')
        tf.write(f'\tnumber {NB}\n')
        tf.write(f'\tinside box  {-L}  {-L} {-L}  {L} {L} {L}\n')
        tf.write('end structure\n')


if __name__ == "__main__":
    _, n, NA, NB, L, inp_file, outfile = sys.argv 
    n, NA, NB, L = int(n), int(NA), int(NB), float(L)
    generate_packmol_input(n, NA, NB, L, inp_file, outfile)
