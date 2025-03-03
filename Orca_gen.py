"""
================================================{ Orca Input files generator }=======================================================

File generates input files for Orca in range of some properties such as distance between 2 ions for now.
It makes a bunch of files in working directory, each file has information about used system, according to variated values X, Y, Z.
Also it creates .sh file for automatic launch.

Usage:
    python gen.py **options
===================================================================================================================================
        Option             Expected       Type                       Meaning                                         Default
===================================================================================================================================
    --cores|-c              value      :integer      Number of cores which will be used to MPI calculation.            max        
-----------------------------------------------------------------------------------------------------------------------------------
    --oversubscribe                     :string      Applying --oversubscribe option to ignore number of CPU's.        no
-----------------------------------------------------------------------------------------------------------------------------------
    --orca_path|-orca   path_to_file    :string      Path to Orca.                                                ~/q-e/bin/pw.x
----------------------------------------------------------------------------------------------------------------------------------- 
    --template|-t       path_to_file    :string      Path to template input file.                                 ./template.inp
-----------------------------------------------------------------------------------------------------------------------------------    
    --output|-o           directory     :string      Path to output directory.                                      ./outputs/
-----------------------------------------------------------------------------------------------------------------------------------      
    --coefficient|-cf       value      :float(0:1]   Coefficient of variety.                                           0.01
----------------------------------------------------------------------------------------------------------------------------------- 
    --num_of_points|-n      value        :odd        Variation volume. (Only odd numbers)                               11
----------------------------------------------------------------------------------------------------------------------------------- 
    --prefix|-p             value       :string      Prefix to all files, including .inp and .out files.              
----------------------------------------------------------------------------------------------------------------------------------- 
    --collect-energy|-col   yes/no      :string      Launch Orca Energy Collector after calculation                     no
===================================================================================================================================

Read more on github: https://github.com/leafforbrain/QE
created on 24.11.2024 at 17:57
@author: Nikita Sozykin (nikita.sozykin@mail.ru)
"""
import argparse
import numpy as np
import sys, os, shutil, re

class Generator():

#  Attributes:

    INPUT_TEMPLATE = None
    coeffs = []
    defaults = [None, None, None]
    x, y, z = None, None, None


#  Methods:
    def __init__(self):
        super().__init__()


    def create_argparser(self):    
        self.argparser = argparse.ArgumentParser()

        self.argparser.add_argument('-c', '--cores', default=os.cpu_count(), type=int)
        self.argparser.add_argument('--oversubscribe', action='store_true')
        self.argparser.add_argument('-orca', '--orca_path', default='~/q-e/bin/pw.x', type=str)
        self.argparser.add_argument('-t', '--template', default='template.inp', type=str)
        self.argparser.add_argument('-o', '--output', default='./outputs/', type=str)
        self.argparser.add_argument('-cf', '--coefficient', default=0.01, type=float)
        self.argparser.add_argument('-n', '--num_of_points', default=11, type=int)
        self.argparser.add_argument('-p', '--prefix', default='', type=str)
        self.argparser.add_argument('-col', '--collect_energy', default='no', type=str)


    def collect_args(self):
        self.namespace = self.argparser.parse_args(sys.argv[1:])
        
        
    def gather_defaults(self, parsed_inp_file: list) -> list:
        p = re.compile(r'([a-zA-Z]{1,2}) +((?:\$X(?:=\d+(?:\.\d*)?)?)|(?:\d.?\d*)) +((?:\$Y(?:=\d+(?:\.\d*)?)?)|(?:\d.?\d*)) +((?:\$Z(?:=\d+(?:\.\d*)?)?)|(?:\d.?\d*))')
        
        for i,val in enumerate(parsed_inp_file):
            match = re.search(p, val)

            if match:
                if match.groups()[1].startswith('$X='):
                    self.defaults[0] = float(match.groups()[1].replace('$X=', ''))
                if match.groups()[1].startswith('$Y='):
                    self.defaults[1] = float(match.groups()[1].replace('$Y=', ''))
                if match.groups()[1].startswith('$Z='):
                    self.defaults[2] = float(match.groups()[1].replace('$Z=', ''))

                new_line = ' '.join([i[:2] if '$' in i else i for i in match.groups()] + ['\n'])
                self.INPUT_TEMPLATE[i] = new_line
    
        
    def open_inp_template(self, path: str) -> list:
        with open(path) as file:
            self.INPUT_TEMPLATE = [line for line in file]
        self.gather_defaults(self.INPUT_TEMPLATE)
    
    
    def valuator(self):
        self.coeffs = [self.namespace.coefficient*(i-np.median(range(self.namespace.num_of_points))) for i in range(self.namespace.num_of_points)]
        self.coeffs = [round(i,3) for i in self.coeffs]
        
        self.x = [round(self.defaults[0]*(1+i), 5) for i in self.coeffs if self.defaults[0]]
        self.y = [round(self.defaults[1]*(1+i), 5) for i in self.coeffs if self.defaults[1]]
        self.z = [round(self.defaults[2]*(1+i), 5) for i in self.coeffs if self.defaults[2]]


    def recreate_dir(self, path):
        try: 
            shutil.rmtree(path)
            os.makedirs(path, exist_ok=True)
        except: os.makedirs(path, exist_ok=True)


    def generate_inputs(self):
        self.recreate_dir('./inputs')
        self.recreate_dir('./outputs')

        for i in list(range(self.namespace.num_of_points)):
            file = open(("./inputs/{prefix}".format(prefix=self.namespace.prefix) + "x" + str(self.coeffs[i]) + ".inp"), 'w')
            
            text = self.INPUT_TEMPLATE
            text = [k.replace('$X',str(self.x[i])) if '$X' in k else k for k in text]
            text = [k.replace('$Y',str(self.y[i])) if '$Y' in k else k for k in text]
            text = [k.replace('$Z',str(self.z[i])) if '$Z' in k else k for k in text]
            
            for i in text:
                file.write(i)
            file.close()
            
            
    def generate_launcher(self):
        file = open('launch.sh', 'w')
        for i in os.listdir('./inputs'):
            if self.namespace.cores > 1:
                run_command = 'mpirun -n {cores} --host localhost:{cores} '.format(cores = str(self.namespace.cores))
            else: run_command = ''
            if self.namespace.oversubscribe:
                run_command += '--oversubscribe '
            else: None
            if self.namespace.orca_path:
                run_command += '{orca_path} ./inputs/{inp_f} | tee {output}{out_f}\n'.format(orca_path = self.namespace.orca_path, 
                                                                                             inp_f = i,
                                                                                             output = self.namespace.output,
                                                                                             out_f = i.replace('.inp', '.out'))
           
            file.write(run_command)
        if self.namespace.collect_energy == 'yes':
            file.write('python Orca_Energy_Collector.py --output {output} --prefix {prefix}'.format(output = self.namespace.output,
                                                                                                  prefix = self.namespace.prefix))
        file.close()



if __name__ == "__main__":
    gen = Generator()
    gen.create_argparser()
    gen.collect_args()
    print(gen.namespace)
    gen.open_inp_template(gen.namespace.template)
    gen.valuator()
    gen.generate_inputs()
    gen.generate_launcher()