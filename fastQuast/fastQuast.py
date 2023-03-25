#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 25.03.2023
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import argparse
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

report_keys = ['Assembly', '# contigs (>= 0 bp)', '# contigs (>= 1000 bp)', '# contigs (>= 5000 bp)', '# contigs (>= 10000 bp)', '# contigs (>= 25000 bp)', '# contigs (>= 50000 bp)', 'Total length (>= 0 bp)', 'Total length (>= 1000 bp)', 'Total length (>= 5000 bp)', 'Total length (>= 10000 bp)', 'Total length (>= 25000 bp)', 'Total length (>= 50000 bp)', '# contigs', 'Largest contig', 'Total length', 'N50', 'L50', 'N75', 'L75', "# N's per 100 kbp"]

def iter_fasta_file(fasta_file_name, split_scaffolds):
    with open(fasta_file_name) as input_file:
        header = False
        seq_length = 0
        for line in input_file:
            line = line.strip()
            if split_scaffolds:
                lines = line.split("N")
                lines_len = len(lines)
                if lines_len > 1:
                    for subline in lines:
                        seq_length += len(subline)
                        yield seq_length, 1
                        seq_length = 0
            if not line:
                break
            if line.startswith(">"):
                if header:
                    yield seq_length, 0
                    seq_length = 0
                header = True
            else:
                seq_length += len(line)
        if header:
            yield seq_length, 0
            
def get_n50_and_l50(contig_lengths):
    total_length = sum(contig_lengths)
    target_length = total_length / 2
    sorted_lengths = sorted(contig_lengths, reverse=True)
    current_length = 0
    for i, length in enumerate(sorted_lengths):
        current_length += length
        if current_length >= target_length:
            return length, i + 1

def get_n_and_l_for_fraction(contig_lengths, fraction):
    total_length = sum(contig_lengths)
    target_length = total_length * fraction
    sorted_lengths = sorted(contig_lengths, reverse=True)
    current_length = 0
    for i, length in enumerate(sorted_lengths):
        current_length += length
        if current_length >= target_length:
            return length, i + 1

def calculate_n_per_100kbp(total_length, total_N):
    return (total_N / total_length) * 100000

def count_n_bases(length):
    return length.count('N') if isinstance(length, str) else 0

def generate_data_dict(contig_lengths, assembly_name, total_N):
    n_contigs = len(contig_lengths)
    total_length = sum(contig_lengths)
    n_1000 = sum(1 for x in contig_lengths if x >= 1000)
    n_5000 = sum(1 for x in contig_lengths if x >= 5000)
    n_10000 = sum(1 for x in contig_lengths if x >= 10000)
    n_25000 = sum(1 for x in contig_lengths if x >= 25000)
    n_50000 = sum(1 for x in contig_lengths if x >= 50000)
    total_length_1000 = sum(x for x in contig_lengths if x >= 1000)
    total_length_5000 = sum(x for x in contig_lengths if x >= 5000)
    total_length_10000 = sum(x for x in contig_lengths if x >= 10000)
    total_length_25000 = sum(x for x in contig_lengths if x >= 25000)
    total_length_50000 = sum(x for x in contig_lengths if x >= 50000)
    largest_contig = max(contig_lengths)
    n50, l50 = get_n50_and_l50(contig_lengths)
    n75, l75 = get_n_and_l_for_fraction(contig_lengths, 0.75)
    n_per_100kbp = calculate_n_per_100kbp(total_length, total_N)

    report_dict = {
        'Assembly': assembly_name,
        '# contigs (>= 0 bp)': n_contigs,
        '# contigs (>= 1000 bp)': n_1000,
        '# contigs (>= 5000 bp)': n_5000,
        '# contigs (>= 10000 bp)': n_10000,
        '# contigs (>= 25000 bp)': n_25000,
        '# contigs (>= 50000 bp)': n_50000,
        'Total length (>= 0 bp)': total_length,
        'Total length (>= 1000 bp)': total_length_1000,
        'Total length (>= 5000 bp)': total_length_5000,
        'Total length (>= 10000 bp)': total_length_10000,
        'Total length (>= 25000 bp)': total_length_25000,
        'Total length (>= 50000 bp)': total_length_50000,
        '# contigs': n_contigs,
        'Largest contig': largest_contig,
        'Total length': total_length,
        'N50': n50,
        'L50': l50,
        'N75': n75,
        'L75': l75,
        '# N\'s per 100 kbp': n_per_100kbp
    }

    return report_dict


def generate_combined_report(results_data, tsv_report=False):
    
    lines = []
    for key in report_keys:
        lines.append([key.ljust(28)])
    
    max_length_of_name = max([len(x) for x in results_data])
    max_adjusted_length = max_length_of_name + 18

    for report in results_data:
        max_adjusted_length = max([len(str(x)) for x in report.values()]) + 4
        for i, key in enumerate(report_keys):
            lines[i].append(str(report[key]).ljust(max_adjusted_length))

    if tsv_report:
        return "\n".join(["\t".join([y.strip() for y in x]) for x in lines])
    else:
        return "\n".join(["".join(x) for x in lines])
    
def inter_assembly_summary(assembly_list):
    for i, assembly in enumerate(assembly_list, start=1):
        N = assembly["# N's per 100 kbp"]
        assembly_name = assembly['Assembly']
        n50 = assembly['N50']
        l50 = assembly['L50']
        total_length = assembly['Total length']
        output = "    %s  %s, N50 = %s, L50 = %s, Total length = %s, # N's per 100 kbp = %s" % (i, assembly_name, n50, l50, total_length, N)
        yield output
 

def main():
    parser = argparse.ArgumentParser(description='Fast and simple Quality Assessment Tool for Genome Assemblies')

    parser.add_argument('files_with_contigs', nargs='+', help='List of files with contigs')
    parser.add_argument('-o', '--output-dir', default=None, help='Directory to store all result files [default: replace file extension with quast extension]')
    parser.add_argument('-s', '--split-scaffolds', action='store_true', help='Split assemblies by continuous fragments of N\'s and add such "contigs" to the comparison [default: False]', default=False)
    parser.add_argument('-m', '--min-contig', type=int, default=1, help='Lower threshold for contig length [default: 1]')
    parser.add_argument('-l', '--labels', default=None, help='Names of assemblies to use in reports, comma-separated. If contain spaces, use quotes')
    parser.add_argument('--tsv', default=False, help='Save report in TSV format to the specified file [default: false]', action='store_true')

    args = parser.parse_args()
    files_to_process = args.files_with_contigs
    split_scaffolds = args.split_scaffolds
    labels = args.labels
    min_contig = int(args.min_contig)
    output_dir = args.output_dir
    tsv_report = args.tsv

    if labels:
        labels = [label.strip() for label in labels.split(",")]
        if len(labels) != len(files_to_process):
            logging.error("Error: number of labels should be equal to number of files")
            exit(1)
    else:
        labels = [
            os.path.splitext(os.path.basename(file_path))[0] for file_path in files_to_process]
    
    output_files = []
    for file_name in files_to_process:
        logging.info("Processing file %s" % file_name)
        output_file = os.path.splitext(file_name)[0] + ".quast"
        if output_dir:
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)
            output_file = os.path.join(output_dir, os.path.basename(output_file))
        output_files.append(output_file)
        
    results_data = []
    for i, file_name in enumerate(files_to_process):
        sizes = []
        total_N = 0
        for seq_length, N in iter_fasta_file(file_name, split_scaffolds):
            if seq_length >= min_contig:
                sizes.append(seq_length)
                total_N += N
        results_data.append(generate_data_dict(sizes, labels[i], total_N))

    report_table = generate_combined_report(results_data, tsv_report=tsv_report)

    for output_file in output_files:
        with open(output_file, "w") as f:
            f.write(report_table)

    for summary in inter_assembly_summary(results_data):
        print(summary)

if __name__ == "__main__":
    main()
