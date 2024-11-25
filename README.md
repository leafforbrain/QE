
# Quntum Espresso input generator for SCF calculations of potential curves. 
 ! THIS README WILL BE COMPLETED SOON !
 Usage:
    python gen.py **kwargs
===================================================================================================================================
        kwarg             Expected       Type                       Meaning                                          Default
===================================================================================================================================
    --cores|-c              value      :integer      Number of cores which will be used to MPI calculation,            max  
                                                     default value will apply argument --oversubscribe to 
                                                     MPI process, whereby max number of cores will be in work.       
-----------------------------------------------------------------------------------------------------------------------------------            
    --pwx_path|-pwx     path_to_file    :string      Path to pw.x calculation program.                            ~/q-e/bin/pw.x
----------------------------------------------------------------------------------------------------------------------------------- 
    --template|-t       path_to_file    :string      Path to template input file.                                 ./template.inp
-----------------------------------------------------------------------------------------------------------------------------------    
    --output|-o           directory     :string      Path to output directory.                                      ./outputs/
-----------------------------------------------------------------------------------------------------------------------------------      
    --coefficient|-c        value      :float(0:1]   Coefficient of variety.                                           0.01
----------------------------------------------------------------------------------------------------------------------------------- 
    --num_of_points|-n      value        :odd        Variation volume. (Only odd numbers)                               11
----------------------------------------------------------------------------------------------------------------------------------- 
    --prefix|-p             value       :string      Prefix to all files, including .inp and .out files.              
----------------------------------------------------------------------------------------------------------------------------------- 
    --pseudo_dir|-pd      directory     :string      Directory with pseudopotentials.                              ~/q-e/pseudo
===================================================================================================================================
