# StrainKmer
StrainKmer- an efficient and user-friendly tool for extracting viral strains' k-mers from raw sequencing data

## Install

Yon can install StrainKmer via [Anaconda](https://anaconda.org/) using the commands below:<BR/>

`git clone https://github.com/liaoherui/StrainKmer.git`<BR/>
`cd StrainKmer`<BR/>
`chmod 777 bin/*`<BR/>


`conda env create -f environment.yaml`<BR/>
`conda activate strainkmer`<BR/>

`python StrainKmer_for_cmd.py -h`<BR/>

If you have installed StrainKmer and downloaded the [Test_datasets](). Then you can test StrainKmer with the example dataset using the command below.

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

