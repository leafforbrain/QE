"""
Created on 30.05.2024 at 23:33
Energy Collector QE
@author: Nikita Sozykin (nikita.sozykin@mail.ru)
"""
import argparse
import tabulate
import re
import numpy as np
import os, sys

class Collector():
    
    def create_argparser(self):
        self.argparser = argparse.ArgumentParser()
        self.argparser.add_argument('--output', default = './outputs/', type = str)
        self.argparser.add_argument('--header', default = ['Expansion, %', 'Energy, Ry', 'E-E(min), eV'])
        self.argparser.add_argument('--range')
        self.argparser.add_argument('--name_template', default = 'compound+delim+expansion_coef')
        self.argparser.add_argument('--norm_value')
        self.argparser.add_argument('--linspace', type = str)
        self.argparser.add_argument('--prefix', default = '', type = str)
        
    def collect_args(self):
        self.namespace = self.argparser.parse_args(sys.argv[1:])

    def last_number(self, string):
        number = int(re.findall(r'\d+', string)[-1])
        return number

    def extract_energies(self):
        file = open('collected_energies.txt', 'w')
        range = []
        energies_Ry = []
        
        files_list = sorted(os.listdir(self.namespace.output), key=self.last_number)
        for i in files_list:
            print(i)
            with open(self.namespace.output + i) as output:
                __parsed = [line.rstrip() for line in output]
            for k in __parsed:
                if all(x in k.split() for x in ['!','total','energy','=']):
                    energies_Ry.append(float(k.split()[-2]))
                if self.namespace.range == 'from_file':
                    if all(x in k.split() for x in ['celldm(1)=','celldm(2)=','celldm(3)=']):
                        range.append(float(k.split()[1]))
            
        energies_eV = [i*13.605691930242388 for i in energies_Ry]
        energies_eV = [i-min(energies_eV) for  i in energies_eV]
        
        if self.namespace.range:
            range = self.namespace.range
        else:
            if self.namespace.linspace:
                data = self.namespace.linspace[1:-1].split(',')
                data = [float(i) for i in data]
                range = np.arange(data[0], data[1], data[2])
            else:
                pass
        
        range = [round(i,6) for i in range]
        print(range)
        
        table = np.transpose(np.vstack((range, energies_Ry, energies_eV)))
        file.write(tabulate.tabulate(table, headers = self.namespace.header, floatfmt = ('.3f', '.8f', '.8f'), colalign = ('right', 'right', 'right')))
        file.close()
        
if __name__ == '__main__':
    collector = Collector()
    collector.create_argparser()
    collector.collect_args()
    collector.extract_energies()
        