# StrainKmer
StrainKmer- an efficient and user-friendly tool for extracting viral strains' k-mers from raw sequencing data

[Windows GUI version](https://strain.ee.cityu.edu.hk/strainkmer/StrainKmer_Windows.zip), [Mac GUI version](https://strain.ee.cityu.edu.hk/strainkmer/StrainKmer_Mac.zip) (Direct download), [Linux GUI version](https://strain.ee.cityu.edu.hk/strainkmer/StrainKmer_Linux.zip) (Direct download)<BR/>
[Windows GUI version](https://drive.google.com/file/d/1xg5Vd6KajFB9CG53JNl75e8Mb-iwmEcH/view?usp=sharing), [Mac GUI version](https://drive.google.com/file/d/1cAzu1wjGW2Z6qE7A8VbyJetdH4MUOdwp/view?usp=sharing) (Google drive), [Linux GUI version](https://drive.google.com/file/d/1qsj-PKNv1zVw4Onz3HIbExLmgJaaZ-9I/view) (Google drive)

## Install

Yon can install StrainKmer via [Anaconda](https://anaconda.org/) using the commands below:<BR/>

`git clone https://github.com/liaoherui/StrainKmer.git`<BR/>
`cd StrainKmer`<BR/>
`chmod 777 bin/*`<BR/>


`conda env create -f environment.yaml`<BR/>
`conda activate strainkmer`<BR/>

`python StrainKmer_for_cmd.py -h`<BR/>

If you have installed StrainKmer and downloaded the [Test_data_and_db](https://drive.google.com/file/d/1Da7bjEMrnvD8ewag5N1Fscl92MbtK2hR/view?usp=share_link). Then you can test StrainKmer with the example dataset using the command below.

`sh test.sh`<BR/>

## Usage

### Use StrainKmer to extract k-mers from your sequencing data.<BR/>
  
  `python StrainKmer_for_cmd.py -i <Input_train_dir> -d <Input_database_dir> -o <Output_dir>`<BR/>
  

### Full command-line options

 `python StrainKmer_for_cmd.py -h`<BR/>
 ```
  StrainKmer - extracting viral strains' k-mers from your sequencing data.
 
 optional arguments:
    -h,   --help                  Show help message and exit.
    -i,   SAMPLE_PATH             Sample files path.
    -d,   DATABASE_FILE_PATH      The path of pre-built database.
    -o,   OUT_PATH                The path of output files (default ./)
    -k,   K_VALUE                 K-mer length (k from 14 to 256; default: 25) 
    -ci,  CI_VALUE                Minimal K-mer occurring times (default: 2) 
    -cs,  CS_VALUE                Maximal K-mer occurring times (default: 65535)
 ```

