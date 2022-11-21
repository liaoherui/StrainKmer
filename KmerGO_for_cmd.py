# coding = utf-8
# author: QiChen
# version: v1.5.0
# modification date: 2020/7/22

import sys, os, shutil, argparse, csv
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from collections import Counter
import warnings
warnings.filterwarnings('ignore')
import time
import platform
import multiprocessing
from lib import kmc_read, kmer_matrix, kmer_features, sequence_assembly
from lib import projectlist_file as plf

system_platform = platform.system()

def get_parameters():
    usage_info = "KmerGO [optional options] -i <input_files_folder> -t <input_trait_information>"
    parser = argparse.ArgumentParser(prog='KmerGO', usage=usage_info)
    parser.add_argument('-i', dest='sample_path', required=True, type=str, help='sample files path')
    parser.add_argument('-d', dest='database_file_path', required=True, type=str, help='the path of pre-built database')
    parser.add_argument('-o', dest='out_path', type=str,default="./", help='the path of output files (default ./)')
    parser.add_argument('-k', '--kmerlength', dest='k_value', type=int, default=25, help='k-mer length (k from 14 to 256; default: 25)')
    parser.add_argument('-ci', dest='ci_value', type=int, default=2, help='minimal K-mer occurring times (default: 2)')
    parser.add_argument('-cs', dest='cs_value', type=int, default=65535, help='maximal K-mer occurring times (default: 65535)')

    return parser.parse_args()



def KMC_GO(param):

    kmc_thread = kmc_read.KMC_Thread((param.k_value, param.ci_value,
                                      param.cs_value, param.sample_path,
                                      param.out_path,param.database_file_path))
    kmc_thread.start()
    last_info = ''
    print('StrainKmer: start k-mer counting...', flush=True)
    while True:
        if kmc_thread.status <= 0:
            if kmc_thread.status == 0:
                print("Complete!")
                return 0
            else:
                if kmc_thread.loginfo != last_info:
                    print(kmc_thread.loginfo, flush=True)
                return -1
        else:
            if kmc_thread.loginfo != last_info:
                last_info = kmc_thread.loginfo
                print(last_info, flush=True)





if __name__ == "__main__":
    multiprocessing.freeze_support()
    param = get_parameters()
    KMC_GO(param)
 
    