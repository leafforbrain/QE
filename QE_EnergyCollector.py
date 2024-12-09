"""
Created on 30.05.2024 at 23:33
Energy Collector QE
@author: Nikita Sozykin (nikita.sozykin@mail.ru)
"""
import argparse
import os, sys

class Collector():
    
    def create_argparser(self):
        self.argparser = argparse.ArgumentParser()
        self.argparser.add_argument('--output', default='./outputs/', type=str)
        self.argparser.add_argument('--prefix', default='', type=str)
        
    def collect_args(self):
        self.namespace = self.argparser.parse_args(sys.argv[1:])

    def extract_energies(self):
        file = open('collected_energies.txt', 'w')
        file.write('Expansion, %\t\tEnergy, eV\n')
        
        result = ''
        for i in os.listdir(self.namespace.output):
            result += str(float(i.replace(self.namespace.prefix, '').replace('.out', '').replace('x', ''))*100)
            with open(self.namespace.output + i) as output:
                __parsed = [line.rstrip() for line in output]
            for k in __parsed:
                if all(x in k.split() for x in ['!','total','energy','=']):
                    result += '\t\t\t\t' + str(round(float(k.split()[-2])*13.605691930242388, 6)) + '\n'
            file.write(result)
            result = ''
        file.close()
        
if __name__ == '__main__':
    collector = Collector()
    collector.create_argparser()
    collector.collect_args()
    collector.extract_energies()
        