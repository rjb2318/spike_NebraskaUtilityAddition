import os
from spike.File.Solarix import Import_2D

file_count = 0

# This is the batch directory. It must be entered to tell the location of all subsequent files.
# The master file should be located within the batch directory.
directory_text = input('What is the file path for the path directory?')

directory = directory_text
master = (directory + os.sep + 'param_controller_master.mscf')
batch = open(directory + os.sep + 'batch_runner.ps1', 'w')

# Iterator for writing new param file based on master_param file to be used as a template.
# Loop will cover each line and modify values based on file details and locations.
# Enter to loop. Calls for each line in the master param file.
for folder in os.listdir(directory):
    if folder == 'param_controller_master.mscf':
        pass
    elif folder == 'batch_runner.ps1':
        pass
    else:
        file_count = file_count + 1
        instruct_location = (directory + os.sep + folder + os.sep + 'param_controller.mscf')
        instruct = open(str(instruct_location), 'w+')
        batch.write('mpiexec -np 60 python -m spike.processing ' + instruct_location + '\n')
        for file in os.listdir(directory + os.sep + folder):
            print('new file at ' + directory + os.sep + folder + os.sep + 'param_controller.mscf')
            if file.endswith('.d'):
                print(file)
                master_open = open(master)
                data_file_location = str(directory + os.sep + folder + os.sep + file)
                outport = (directory + os.sep + folder + os.sep + file[:-2] + '_binary.msh5')
                d = Import_2D(directory + os.sep + folder + os.sep + file, outfile=outport)

                #This will go through and collect the frequency and high mass for each file
                for sub_file in os.listdir(data_file_location):
                    if sub_file.endswith('.m'):
                        method_file = open(data_file_location + os.sep + sub_file +os.sep + 'apexAcquisition.method')
                        for line_2 in method_file:
                            if line_2.startswith('<param name="EXC_hi">'):
                                highmass = []
                                for character in line_2:
                                    if character.isdigit() or character == '.':
                                        highmass.append(character)
                                    else:
                                        pass
                                highmass = ''.join(highmass)
                                print(highmass)
                            if line_2.startswith('<param name="EXC_Freq_Low"><value>'):
                                frequency = []
                                for character in line_2:
                                    if character.isdigit() or character == '.':
                                        frequency.append(character)
                                    else:
                                        pass
                                frequency = ''.join(frequency)
                                print(frequency)
                            else:
                                pass
                    else:
                        pass
                method_file.close()
                # Creating instruction file. Fills in blanks for file locations, frequency, and high mass
                for line in master_open:
                    stripped_line = line.strip()
                    # Conditional for writing frequency of demodulation and high mass from Apex file.
                    if stripped_line == 'highmass =':
                        instruct.write('highmass = ' + highmass + '\n')

                    elif stripped_line == 'freq_f1demodu=':
                        instruct.write('freq_f1demodu= ' + frequency + '\n')

                    # Conditionals for denoting appropriate file locations
                    elif stripped_line == 'apex =':
                        instruct.write('apex = ' + data_file_location + '\n')
                        print('apex = ' + data_file_location + '\n')
                    elif stripped_line == 'infile =':
                        instruct.write('infile = ' + outport + '\n')
                    elif stripped_line == 'interfile =':
                        instruct.write('interfile = ' + directory + os.sep + folder + os.sep + 'interfile.msh5\n')
                    elif stripped_line == 'outfile =':
                       instruct.write('outfile = ' + directory + os.sep + folder + os.sep + file[:-2] + '_outfile.msh5\n')
                       print('outfile = ' + directory + os.sep + folder + os.sep + file[:-2] + '_outfile.msh5\n')
                    else:
                        instruct.write(stripped_line +'\n')





print('Number of files for processing: ' + str(file_count))
print(data_file_location)