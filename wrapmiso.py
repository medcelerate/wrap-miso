import sys
import os
import subprocess
pickle = sys.argv[1]
bamDir = sys.argv[2]
readlength = sys.argv[3]
outputDir = sys.argv[4]
index = sys.argv[5]

def run_miso(bam, output, pickle, readlength, index):
    command = "/cm/shared/apps/slurm/15.08.13/bin/srun -p longq7 /home/groups/caputi-lab/fastmiso-latest/bin/exon_utils --get-const-exons " + index + " --min-exon-size 1000 --output-dir " + output + "ex/"
    print command
    #command = "'srun -p longq /home/groups/caputi-lab/fastmiso/bin/exon_utils --get-const-exons " + index + " --min-exon-size 1000 --output-dir " + output + "ex/'"
    command = str(command)
    #return_code = subprocess.call(command, shell=True)
    return_code = subprocess.call(command, shell=True)
    if return_code == 0:
        for files in os.listdir(bam):
            if files.endswith(".bam"):
		i = 0
                indexNew = output + "ex/" + str(os.path.basename(index).rsplit('.gff', 1)[0]) + '.min_1000.const_exons.gff'
                command = "/cm/shared/apps/slurm/15.08.13/bin/srun -p longq7 pe_utils --compute-insert-len " + files + " " + indexNew + " --min-exon-size 1000 --output-dir " + output + "pe/insert-dist_" + str(files.rsplit('.bam', 1)[0]) + "/"
                #print command
		#print command
		print command
                return_code = subprocess.call(command, shell=True)
		#return_code.wait()
                if return_code == 0:
                    location = output + "pe/insert-dist_" + str(files.rsplit('.bam', 1)[0]) + "/" + str(files) + ".insert_len"
                    insert_length = open(location, 'r').readline()
                    insert_length = insert_length.split(',')
                    mean = insert_length[0].rsplit('=')
                    mean = mean[1]
                    sdev = insert_length[1].rsplit('=')
                    sdev = sdev[1]
                    for subdir, dirs, filesw in os.walk(pickle):
                        for name in dirs:    
			    if i == 5:
			        break
			    else:
			        print name
			        print files
			        print output
			        print mean
			        print sdev
			        print readlength
			        print files.rsplit('.bam', 1)[0]
                                print command
			        command = "miso --run " + pickle + name + ' ' + files + " --output-dir " + output + "miso/" + str(files.rsplit('.bam', 1)[0]) + " --read-len " + str(readlength) + " --paired-end " + str(mean) + ' ' + str(sdev) + " --use-cluster"
                                #print command
                                miso_code = subprocess.call(command, shell=True)
			        i = i + 1
                                continue
                else:
                    sys.exit()


            else:
                sys.exit()
    else:
        print (return_code)




os.makedirs(outputDir)
os.makedirs(outputDir + '/miso')
os.makedirs(outputDir + '/ex')
os.makedirs(outputDir + '/pe')
os.makedirs(outputDir + '/compare')

if len(sys.argv) != 6:
    print ("The basic config should look like \n./miso.py pickle_directory bam_directory read_length output_directory gff_index_file")
    sys.exit()
else:
    run_miso(bam = bamDir, output = outputDir, pickle = pickle, readlength = readlength, index = index)
