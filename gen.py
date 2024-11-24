"""
============ QE Input files generator ==============
created on 24.11.2024 at 17:57
@author: Nikita Sozykin (nikita.sozykin@mail.ru)

File generates input files for QE in range of some properties such as crystal parameters.
It makes a bunch of files in working directory, each file has information about crystal state.
With that it creates .bat file for automatic launch.

.bat file looks like:
mpirun -n NUM_OF_CORES --oversubscribe --host localhost:12 PWX_PATH < INPUT_FILE | tee OUTPUT_FILE
python gen.py --cores|-c N:num --pwx_path|-pwx X:str --input|-i X:str --output|-o X:str -s N:num -n N:num

python gen.py -c 0.01 -n 10
====================================================
"""
import argparse
import numpy as np
import sys

class Generator():

#  Attributes:
    NUM_OF_CORES = None
    PWX_PATH = None
    INPUT_FILE = None
    OUTPUT_FILE = None


#  Methods:
    def __init__(self):
        super().__init__()

    def create_argparser(self):    
        
        self.argparser = argparse.ArgumentParser()
        self.argparser.add_argument('-c', '--cores', default='oversubscribe')
        self.argparser.add_argument('-pwx', '--pwx_path', default='~/QE//q-e/bin/pw.x')
        self.argparser.add_argument('-i', '--input', default='test.inp')
        self.argparser.add_argument('-o', '--output', default='~/QE/output/test.out')
        self.argparser.add_argument('-coef', '--coefficient', default=0.05)
        self.argparser.add_argument('-n', '--num_of_points', default=11)
        
    def collect_args(self):
        self.namespace = self.argparser.parse_args(sys.argv[1:])
        
    def open_inp_file(self, path: str) -> list:
        with open(path) as file:
            self.INPUT_FILE = [line.rstrip() for line in file]
            
        for i in self.INPUT_FILE:
            if 'A = ' in i: self.defaults[0] = i.split()[2]
            elif 'B = ' in i: self.defaults[1] = i.split()[2]
            elif 'C = ' in i: self.defaults[2] = i.split()[2]
            
    def valuator(self):
        self.a = [self.namespace.coefficient*(i-np.median(range(self.namespace.num_of_points))) for i in range(self.namespace.num_of_points)]
        print(self.a)

if __name__ == "__main__":
    gen = Generator()
    gen.create_argparser()
    gen.collect_args()
    print(gen.namespace)
    gen.open_inp_file(gen.namespace.input)
    gen.valuator()