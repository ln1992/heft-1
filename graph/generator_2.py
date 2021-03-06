# Generates cost matrices based on given number of nodes and processors

from graph import random_comp_matrix, random_comm_matrix

nodes = 1000;
processors = 5;

# generates comp matrices

# for y in range(1001,5000): 
# for x in range(1,processors+1):
# 	random_comp_matrix(x, 1615,15) 
# random_comm_matrix(1615,50)	

# for x in range(1,processors+1):
# 	random_comp_matrix(x, 4583,15) 
# random_comm_matrix(4583,50)	

for x in range(1,processors+1):
	random_comp_matrix(x, 2899,15) 
random_comm_matrix(2899,50)	



# 771, 108,1202,135,3,19603,3467,1095,7719,12498,3271,29227,2899,1615,4583,2068