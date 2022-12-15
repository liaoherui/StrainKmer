# coding = utf-8
# author: QiChen
# version: v3.0
# modification date: 2020/4/21

import os, sys, re
import subprocess
import threading
import platform
from collections import defaultdict
#import pickle
#import gzip
import numpy as np
import scipy.sparse as sp


FASTA_suffix = ['.fa', '.fna', '.fasta', '.fa.gz', '.fna.gz', '.fasta.gz']
FASTQ_suffix = ['.fq', '.fastq', '.fq.gz', '.fastq.gz']

class KMC_Thread(threading.Thread):
    def __init__(self, KMC_Param):
        threading.Thread.__init__(self)
        self.Parameters = KMC_Param
        self.loginfo = ''
        self.status = 1

    def run(self):
        try:
            self.status = self.KMC_GO()
        except:
            self.status = -999
        if self.status == -1:
            self.loginfo = 'The system is not supported.'
        elif self.status == -2:
            self.loginfo = 'There are no FASTA/Q files under the selected folder.'
        elif self.status == -999:
            self.loginfo = 'There are some errors when KMC is running.'

    def KMC_GO(self):
        self.loginfo = 'KMC working is ready...'

        system_platform = platform.system()
        #print(self.Parameters)
        #exit()
        k_value = self.Parameters[0]
        ci_value = self.Parameters[1]
        cs_value = self.Parameters[2]
        work_dir = self.Parameters[3]
        output_dir = self.Parameters[4]
        db_dir=self.Parameters[5]
        flist = []
        typelist = []

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)



        if system_platform == 'Windows':
            kmc_command = r'.\bin\kmc.exe'
            kmc_tools_command = r'.\bin\kmc_tools.exe'
            kmc_dump_command = r'.\bin\kmc_dump.exe'
        elif system_platform == 'Linux':
            file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
            kmc_command = file_path + '/bin/./kmc'
            kmc_tools_command = file_path + '/bin/./kmc_tools'
            kmc_dump_command = file_path + '/bin/./kmc_dump'
        else:
            return -1   # the system is not supported

        for dir, folder, file in os.walk(work_dir):
            if dir == work_dir:
                flist = file
        flist.sort()
        for i in list(flist):
            suffix = i[i.find('.'):]
            if suffix.lower() in FASTA_suffix:
                typelist.append(' -fm ')
                flist[flist.index(i)] = [i[:i.find('.')], os.path.join(work_dir, i)]
            elif suffix.lower() in FASTQ_suffix:
                typelist.append(' -fq ')
                flist[flist.index(i)] = [i[:i.find('.')], os.path.join(work_dir, i)]
            else:
                flist.remove(i)
            if len(flist) == 0:
                return -2  # no files in this directory



        #DB_name=os.path.splitext(os.path.basename(db_dir))[0]
        countings = 0
        self.loginfo = 'Number 0/' + str(len(flist))
        for i in range(len(flist)):
            countings += 1
            #out[flist[i][0]]=icount.copy()
            #name.append(flist[i][0])
            #out=icount.copy()
            # Run KMC on the input sequnece datasets

            cmd = kmc_command + ' -k' + str(k_value) + ' -ci' + str(ci_value) + ' -cs' + str(cs_value)+' -b '\
                  + typelist[i] + flist[i][1] + ' ' + os.path.join(work_dir, flist[i][0])\
                  + ' ' + work_dir
            #print(cmd)

            r = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
            if r != 0:
                return 0 / 0


            # Intersection of these two databases
            cmd1 = kmc_tools_command+' simple ' + os.path.join(work_dir, flist[i][0])+ ' '+db_dir+'  intersect '+os.path.join(work_dir, flist[i][0]+'_res -ocleft')
            cmd2 = kmc_tools_command + ' simple ' + os.path.join(work_dir, flist[i][0]) + ' ' + db_dir+'_sub  intersect ' + os.path.join(work_dir, flist[i][0] + '_sub_res -ocleft')
            r = subprocess.call(cmd1, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
            if r != 0:
                return 0 / 0

            r = subprocess.call(cmd2, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
            if r != 0:
                return 0 / 0
            # Get all kmer count of the data
            # cmd = kmc_tools_command + ' simple '+db_dir+' '+os.path.join(work_dir, flist[i][0]+'_res')+' union '+os.path.join(work_dir, flist[i][0]+'_final_res -ocmax')
            # r = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            # if r != 0:
            #     return 0 / 0
            #
            # cmd = kmc_tools_command + ' simple ' + db_dir + '_sub ' + os.path.join(work_dir, flist[i][0] + '_sub_res') + ' union ' + os.path.join(work_dir, flist[i][0] + '_final_res_sub -ocmax')
            # r = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # if r != 0:
            #     return 0 / 0
            # Dump the result
            cmd = kmc_dump_command + ' -cs' + str(cs_value) + ' '\
                  + os.path.join(work_dir, flist[i][0] + '_res') + ' '\
                  + os.path.join(output_dir, flist[i][0] + '.txt') + ' '\
                  + os.path.join(output_dir, flist[i][0] + '_beacon.txt')
            #print(cmd)
            r = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
            if r != 0:
                return 0 / 0
            cmd = kmc_dump_command + ' -cs' + str(cs_value) + ' '\
                  + os.path.join(work_dir, flist[i][0] + '_sub_res') + ' '\
                  + os.path.join(output_dir, flist[i][0] + '_sub.txt') + ' '\
                  + os.path.join(output_dir, flist[i][0] + '_beacon_sub.txt')
            r = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
            if r != 0:
                return 0 / 0

            cmd = kmc_dump_command + ' ' \
                  + db_dir + ' ' \
                  + db_dir + '.txt'
            r = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
            # print(cmd)
            if r != 0:
                return 0 / 0

            cmd = kmc_dump_command + ' ' \
                  + db_dir + '_sub ' \
                  + db_dir + '_sub.txt'
            r = subprocess.call(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
            # print(cmd)
            if r != 0:
                return 0 / 0

            fd1 = open(db_dir + '.txt', 'r')
            kmr_arr = []
            while True:
                line = fd1.readline().strip()
                if not line: break
                ele = line.split()
                kmr_arr.append(ele[0])
            fd1.close()
            # print(kmr_arr)
            fd2 = open(db_dir + '_sub.txt', 'r')
            kmr_sub_arr = []
            while True:
                line = fd2.readline().strip()
                if not line: break
                ele = line.split()
                kmr_sub_arr.append(ele[0])
            fd2.close()

            os.remove(os.path.join(work_dir, flist[i][0] + '.kmc_pre'))
            os.remove(os.path.join(work_dir, flist[i][0] + '.kmc_suf'))

            os.remove(os.path.join(work_dir, flist[i][0] + '_res.kmc_pre'))
            os.remove(os.path.join(work_dir, flist[i][0] + '_res.kmc_suf'))
            os.remove(os.path.join(work_dir, flist[i][0] + '_sub_res.kmc_pre'))
            os.remove(os.path.join(work_dir, flist[i][0] + '_sub_res.kmc_suf'))
            #print('finished')
            #exit()
            os.remove(db_dir + '.txt')
            os.remove(db_dir + '_sub.txt')

            #print(os.path.join(output_dir, flist[i][0] + '.txt'))

            out = []
            kcd = {}
            f2 = open(os.path.join(output_dir, flist[i][0] + '.txt'), 'r')
            while True:
                line = f2.readline().strip()
                if not line: break
                ele = line.split()
                kcd[ele[0]] = int(ele[1])
                # print(ele)
                # out.append(int(ele[1]))
            f2.close()
            o4 = open(os.path.join(output_dir, flist[i][0] + '_sort.txt'), 'w+')
            for a in kmr_arr:
                if a not in kcd:
                    out.append(0)
                    o4.write(a + '\t0\n')
                else:
                    out.append(kcd[a])
                    o4.write(a + '\t' + str(kcd[a]) + '\n')
            o4.close()
            out = np.array(out)
            spa = sp.csr_matrix(out)
            sp.save_npz(os.path.join(output_dir, flist[i][0] + '.npz'), spa)

            out2 = []
            kcd2 = {}
            f3 = open(os.path.join(output_dir, flist[i][0] + '_sub.txt'), 'r')

            while True:
                line = f3.readline().strip()
                if not line: break
                ele = line.split()
                # print(ele)
                kcd2[ele[0]] = int(ele[1])

            f3.close()
            o5 = open(os.path.join(output_dir, flist[i][0] + '_sub_sort.txt'), 'w+')
            for a in kmr_sub_arr:
                if a not in kcd2:
                    out2.append(0)
                    o5.write(a + '\t0\n')
                else:
                    out2.append(kcd2[a])
                    o5.write(a + '\t' + str(kcd2[a]) + '\n')
            o5.close()

            # print('plan to remove tem files')
            os.remove(os.path.join(output_dir, flist[i][0] + '.txt'))
            os.remove(os.path.join(output_dir, flist[i][0] + '_sub.txt'))
            # print('remove done')

            out2 = np.array(out2)
            spa = sp.csr_matrix(out2)
            sp.save_npz(os.path.join(output_dir, flist[i][0] + '_sub.npz'), spa)

            #os.remove(os.path.join(output_dir, flist[i][0] + '.txt'))

            self.loginfo = 'Number ' + str(countings) + '/' +  str(len(flist))

        return 0
