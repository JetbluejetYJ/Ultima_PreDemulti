
# 🚀 Ultima Genomics UG100 Pre-Demulti Script

A Python script for pre-demultiplexing analysis of Ultima Genomics UG100 sequencing runs.

---

## 📦 Usage

```bash
python Ultima_preDM.py [Run_Name] [Sample_Info]
# Example:
python Ultima_preDM.py 422022-20250613_1638 422022-20250613_1638.csv
```

### **Arguments**

| Argument      | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `Run_Name`    | The name of the UG100 sequencing run (e.g., `422022-20250613_1638`)         |
| `Sample_Info` | Path to the CSV file containing sample information (comma-delimited)         |

### **Options**

| Option        | Description                            |
|---------------|----------------------------------------|
| `-h, --help`  | Show help message and exit             |

---

## 📤 Output Files

The script generates **two CSV files** per run:

1. **Pre-demultiplexing results**  
   `[Run_Name]_sorted.csv`
2. **Top unknown barcodes results**  
   `Top_Unknown_Barcodes.csv`

---

## ❓ What is a Top Unknown barcode?

> A **Top Unknown barcode** refers to barcodes that are not registered in the sample information file (`Sample_Info.csv`)—that is, unknown barcodes—ranked in order of highest yield (output).  
> These barcodes are not assigned to any actual sample, so they are classified as **"unassigned (barcode unmatched)"** or **"Unknown barcode."**
>
> The file `Top_Unknown_Barcodes.csv` contains a list of barcodes that are not present in the sample information (PreDM), sorted by yield in descending order.  
> In other words, it is a list of the most frequently detected unassigned (Unknown) barcodes in this sequencing run.

---

## 📁 Directory Structure

```plaintext
/home/Ultima_PreDemulti/
├── 422022-20250613_1638/
│   ├── 422022-20250613_1638_sorted.csv
│   └── Reports/
│       └── Top_Unknown_Barcodes.csv
├── 422125-20250613_1930/
│   ├── 422125-20250613_1930_sorted.csv
│   └── Reports/
│       └── Top_Unknown_Barcodes.csv
├── csv/
│   ├── 422022-20250613_1638.csv
│   └── 422125-20250613_1930.csv
└── Ultima_preDM.py
```

---

## 📝 Notes

- Make sure your `Sample_Info.csv` is properly formatted (comma-delimited).
- For any issues or questions, please open an issue on this repository.

---
