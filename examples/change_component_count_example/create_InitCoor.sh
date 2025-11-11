n=10 # segment count
seg=2212212 # segment pattern

NA=100 # A-chain count
NB=100 # B-chain count 
NC=100

L=700

pck_inp='populate_tmp.inp'

pck_out='IC_tmp.xyz' 

cvfile='N400_Rg_L700.colvars'

sysName="b70_N200_L$L.lt" # double quote is needed for bash 

dataFile="b70_N200_L$L.data"

lmp_input='Template_input.in'

python3 LT_writer.py $n $seg 

python3 writePackmolInput.py $n $NA $NB $NC $L $pck_inp $pck_out

python3 writeSysLT.py $n $NA $NB $NC $L $sysName

packmol < $pck_inp

moltemplate.sh -xyz $pck_out $sysName -nocheck
python3 updateColVar.py $pck_out $cvfile $L $n $NA $NB $NC $seg
python3 updateInput.py $lmp_input $L 
python3 fix_datafiles.py $dataFile