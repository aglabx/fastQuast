# FastQuast: Fast and simple Quality Assessment Tool for Large Genomes

FastQuast is a tool for assessing the quality of genome assemblies. It is designed to be fast and simple, with usage patterns similar to the popular Quast tool. However, FastQuast has been rewritten from scratch to optimize for speed, providing results up to 5 times faster than Quast.

## Features

FastQuast provides the following features:

- Works with python 2.7 and 3.6+
- Fast and efficient quality assessment of genome assemblies similar to the classic Quast
- User-defined thresholds for contig length
- Ability to save reports in TSV format (if you want more post-processing friedly format, but I prefer classic Quast txt format)


## Installation

FastQuast can be installed via pip or conda. First, make sure you have either pip or conda installed on your system.

### Installation via pip

To install FastQuast via pip, run the following command:

```bash
pip install fastQuast
```

## Usage

You can use both variant:

```
fastQuast -h
```

and

```
fastquast -h
```

The simplest way to use:

```
fastquast you_genome.fasta
```

And it will create you_genome.quast file in the same place where you_genome.fasta located.


Full usage and options:

```
fastquast [-h] [-o OUTPUT_DIR] [-s] [-m MIN_CONTIG] [-l LABELS] [--tsv]
                 files_with_contigs [files_with_contigs ...]

Fast and simple Quality Assessment Tool for Genome Assemblies

positional arguments:
  files_with_contigs    List of files with contigs

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Directory to store all result files [default: replace file extension with quast
                        extension]
  -s, --split-scaffolds
                        Split assemblies by continuous fragments of N's and add such "contigs" to the
                        comparison [default: False]
  -m MIN_CONTIG, --min-contig MIN_CONTIG
                        Lower threshold for contig length [default: 1]
  -l LABELS, --labels LABELS
                        Names of assemblies to use in reports, comma-separated. If contain spaces, use
                        quotes
  --tsv                 Save report in TSV format to the specified file [default: false]
  ```
  
## Example


Here's an example of how to use FastQuast:

```
fastquast -o results/ -s --min-contig 500 --labels "Assembly A, Assembly B" --tsv contigs.fasta 
```

This will assess the quality of the contigs.fasta assembly, split scaffolds by continuous fragments of N's, set a minimum contig length of 500 bp, label the assembly as "Assembly A" and "Assembly B" in the report, save the report in both human-readable and TSV format, and store the results in the results/ directory.




