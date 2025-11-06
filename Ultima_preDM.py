#-*- coding: utf-8 -*-
import os
import pandas as pd
import argparse

def get_args():
    boxed_desc = (
        "┌──────────────────────────────────────────────────────────────────────────┐\n"
        "│ Processing PreDM of Ultima Genomics UG100 sequencing platform run data   │\n"
        "│ The script outputs two CSV files:                                        │\n"
        "│ 1. Pre-demultiplexing results ([Run_Name]_sorted.csv)                    │\n"
        "│ 2. Top unknown barcodes results (Top_Unknown_Barcodes.csv)               │\n"
        "└──────────────────────────────────────────────────────────────────────────┘"
    )
    parser = argparse.ArgumentParser(
        description=boxed_desc,
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        'Run_Name',
        type=str,
        metavar='\033[31mRun_Name\033[0m',
        help='The name of the Ultima Genomics UG100 sequencing run (e.g., 422022-20250613_1638)'
    )
    parser.add_argument(
        'Sample_Info',
        type=str,
        metavar='\033[33mSample_Info\033[0m',
        help='The path to the CSV file containing sample information (comma delimiter)'
    )
    return parser.parse_args()

def generate_sample_mappings(sample_info_path):
    sample_info_df = pd.read_csv(sample_info_path)

    fcid_map, lane_map, samples = {}, {}, {}
    sample_ref_map, recipe_map, project_map = {}, {}, {}
    library_type_map, application_type_map = {}, {}
    plate_id_map, lib_id_map, cmpny_cd_map = {}, {}, {}

    for _, row in sample_info_df.iterrows():
        fcid = row['FCID']
        lane = row['Lane']
        sample_id = row['SampleID']
        sample_ref = row['SampleRef']
        index_sequence = row['Index Seq']
        recipe = row['Recipe']
        project = row['Project']
        library_type = row['LibraryType']
        application_type = row['ApplicationType']
        plate_id = row['PlateId']
        lib_id = row['LibId']
        cmpny_cd = row['CmpnyCd']

        fcid_map[sample_id] = fcid
        lane_map[sample_id] = lane
        samples[index_sequence] = sample_id
        sample_ref_map[sample_id] = sample_ref
        recipe_map[sample_id] = recipe
        project_map[sample_id] = project
        library_type_map[sample_id] = library_type
        application_type_map[sample_id] = application_type
        plate_id_map[sample_id] = plate_id
        lib_id_map[sample_id] = lib_id
        cmpny_cd_map[sample_id] = cmpny_cd

    return (samples, fcid_map, lane_map, sample_ref_map, recipe_map, project_map,library_type_map, application_type_map, plate_id_map, lib_id_map, cmpny_cd_map)


def extract_sample_metrics(run_dir_path, samples, fcid_map, lane_map, sample_ref_map, recipe_map, project_map,library_type_map, application_type_map, plate_id_map, lib_id_map, cmpny_cd_map):
    results = []

    for subdir, _, files in os.walk(run_dir_path):
        dir_name = os.path.basename(subdir)
        if 'TT-TT' in dir_name or 'UNKN' in dir_name:
            continue

        folder_parts = dir_name.split('-')
        barcode      = folder_parts[-1] if folder_parts else ""

        if barcode not in samples:
            fcid = lane = sample_id = sample_ref = "PreDM"
            recipe = project = library_type = application_type = "PreDM"
            plate_id = lib_id = cmpny_cd = "PreDM"

            if len(folder_parts) == 4:
                sample_ref = "%s-%s" % (folder_parts[1], folder_parts[2])
            elif len(folder_parts) == 3:
                sample_ref = folder_parts[1]

            index_sequence = ""
            if folder_parts and folder_parts[-1] and folder_parts[-1][0] in ['A','T','G','C']:
                index_sequence = folder_parts[-1]

        else:
            sample_id        = samples[barcode]
            fcid             = fcid_map[sample_id]
            lane             = lane_map[sample_id]
            sample_ref       = sample_ref_map[sample_id]
            recipe           = recipe_map[sample_id]
            project          = project_map[sample_id]
            library_type     = library_type_map[sample_id]
            application_type = application_type_map[sample_id]
            plate_id         = plate_id_map[sample_id]
            lib_id           = lib_id_map[sample_id]
            cmpny_cd         = cmpny_cd_map[sample_id]
            index_sequence   = ""

        for file in files:
            if file.startswith('merged'):
                continue

            if file.endswith('%s.csv' % barcode):
                print("Processing file: {}".format(file))
                csv_file_path = os.path.join(subdir, file)

                df = pd.read_csv(csv_file_path, header=None, names=['Metric', 'Value'])

                try:
                    pf_barcode_reads = int(df.loc[df['Metric']=='PF_Barcode_reads','Value'].values[0])
                except (KeyError, IndexError, ValueError):
                    pf_barcode_reads = 0
                try:
                    mean_read_length = float(df.loc[df['Metric']=='Mean_Read_Length', 'Value'].values[0])
                except (KeyError, IndexError, ValueError):
                    mean_read_length = 0

                yield_value = pf_barcode_reads * mean_read_length
                non_pass    = yield_value < 1000000000
                results.append((fcid, lane, sample_id, sample_ref, barcode,yield_value, pf_barcode_reads, mean_read_length, recipe, project, library_type, application_type,plate_id, lib_id, cmpny_cd, non_pass))

    return results

def prepare_report_tables(results):
    results_df = pd.DataFrame(results,columns=[
            'FCID','Lane','Sample ID','SampleRef','Index Sequence','Yield','PF_Barcode_reads','Mean_Read_Length','Recipe','Project','LibraryType','ApplicationType','PlateId','LibId','CmpnyCd','Non_Pass'])
    total_pf = results_df['PF_Barcode_reads'].sum()
    results_df['% of PF Barcode_reads'] = (results_df['PF_Barcode_reads']/total_pf*100).round(3)
    results_df = results_df[
        ['FCID','Lane','Sample ID','SampleRef','Index Sequence','Yield','PF_Barcode_reads','Mean_Read_Length','% of PF Barcode_reads','Non_Pass','Recipe','Project','LibraryType','ApplicationType','PlateId','LibId','CmpnyCd']]
    results_df = results_df.sort_values(by=['FCID'], key=lambda x: x == 'PreDM')
    sorted_predm_df   = results_df[results_df['Sample ID']=='PreDM'].sort_values(by='Yield', ascending=False)
    fail_sample_count = results_df.loc[results_df['Sample ID'] != 'PreDM', 'Non_Pass'].sum()

    if fail_sample_count > 0:
        top_n = fail_sample_count * 3
    else:
        top_n = 5

    sorted_predm_df = results_df[results_df['Sample ID'] == 'PreDM'].sort_values(by='Yield', ascending=False)
    report_in_predm_df = sorted_predm_df.head(top_n)
    remaining_predm_df= sorted_predm_df.iloc[top_n:]
    report_df = pd.concat([results_df[results_df['Sample ID']!='PreDM'], report_in_predm_df])
    return report_df, remaining_predm_df

def to_hq_lims_frame(results_df):
    results_df['SampleID'] = results_df['Project'].astype(str) + '_' + results_df['Sample ID'].astype(str)
    results_df['SampleName'] = results_df['Sample ID']
    results_df['index']      = results_df['Index Sequence']
    results_df['Result(Non Pass)'] = results_df['Non_Pass'].map({True:'Fail', False:'Pass'})
    results_df['Reads']      = results_df['PF_Barcode_reads']
    results_df['Throughput'] = results_df['Yield']
    results_df['Percentage'] = results_df['% of PF Barcode_reads']
    results_df.loc[results_df['SampleName'] == 'PreDM', 'SampleID'] = 'PreDM'
    results_df = results_df[
        ['Lane','SampleID','SampleName','SampleRef','index','Project','Result(Non Pass)','Reads','Throughput','Percentage','PlateId','LibId','CmpnyCd']]
    return results_df

def save_outputs(run_name, results_df, remaining_predm_df):
    output_dir  = '/garnet2/Users/yeongjae0420/10.WORK/10.Ultima_PreDemulti/{}'.format(run_name)
    output_dir2 = '{}/Reports'.format(output_dir)
    for d in (output_dir, output_dir2):
        if not os.path.exists(d):
            os.makedirs(d)
    output_csv_path          = os.path.join(output_dir , '%s_sorted.csv' % run_name)
    unknown_barcode_csv_path = os.path.join(output_dir2, 'Top_Unknown_Barcodes.csv')
    results_df.to_csv(output_csv_path, index=False)
    remaining_predm_df.to_csv(unknown_barcode_csv_path, index=False)
    print("Results saved :: {}".format(output_csv_path))
    print("Unknown barcodes saved :: {}".format(unknown_barcode_csv_path))

def main():
    print("")
    args = get_args()
    run_name = args.Run_Name
    sample_info_path = args.Sample_Info
    (samples, fcid_map, lane_map, sample_ref_map, recipe_map, project_map, library_type_map, application_type_map, plate_id_map, lib_id_map, cmpny_cd_map) = generate_sample_mappings(sample_info_path)
    run_dir_path = '/garnet/Ultima/UG100_01/{}/'.format(run_name)
    results = extract_sample_metrics(run_dir_path, samples, fcid_map, lane_map, sample_ref_map, recipe_map, project_map, library_type_map, application_type_map, plate_id_map, lib_id_map, cmpny_cd_map)
    report_df, remaining_predm_df = prepare_report_tables(results)
    hq_df = to_hq_lims_frame(report_df)
    save_outputs(run_name, hq_df, remaining_predm_df)

if __name__ == '__main__':
    main()
