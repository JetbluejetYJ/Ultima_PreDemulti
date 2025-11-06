### Ultima Genemics UG100 Pre-Demulti Script
Usage : Ultima_preDM.py [-h] [Run_Name] [Sample_Info]


ex) 
python Ultima_preDM.py 422022-20250613_1638 422022-20250613_1638.csv

[positional arguments]
  Run_Name     The name of the Ultima Genomics UG100 sequencing run (e.g., 422022-20250613_1638)
  Sample_Info  The path to the CSV file containing sample information (comma delimiter)

[options]
  -h, --help            show this help message and exit

* The script outputs two CSV files:
 1. Pre-demultiplexing results ([Run_Name]_sorted.csv)
 2. Top unknown barcodes results (Top_Unknown_Barcodes.csv)


### Directory Structure
/home/Ultima_PreDemulti/
├── 422022-20250613_1638/
│   ├── 422022-20250613_1638_sorted.csv
│   └── Reports/
│       └── Top_Unknown_Barcodes.csv
├── 422125-20250613_1930/
│   ├── 422125-20250613_1930_sorted.csv
│   └── Reports/
│       └── Top_Unknown_Barcodes.csv
├── csv/
│   ├── 422022-20250613_1638.csv
│   └── 422125-20250613_1930.csv
└── Ultima_preDM.py
