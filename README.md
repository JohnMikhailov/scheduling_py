# scheduling_py
simple solution for scheduling problem

To run the script, you have to create instance of bee_colony_algorithm class;
example: 

import bee_colony_algorithm as bca
import input_output

result = bca.bca()
input_output.write(result[0][0])

This chunk of code will start whole algorithm and save solution in 'output.txt' file.
