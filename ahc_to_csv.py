import os
import csv
import sys
import multiprocessing
def convert_ahc_to_csv(ahc_file, csv_file):
    """
        Função que tenta escrever/ler tanto em utf8 quanto em latin1
    """
    try:
        with open(ahc_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
    except UnicodeDecodeError as error:
        print(error, '-- tantando latin1')
        with open(ahc_file, 'r', encoding='latin1') as infile:
            lines = infile.readlines()

    lines = [line.replace('ø', 'O').replace('', 'C').replace('€', 'C') for line in lines]

    with open(csv_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=';')
        for line in lines:
            writer.writerow(line.strip().split('\t'))

def process_directory(directory):
    
    for filename in os.listdir(directory):
        v_filename = filename.strip()
        if v_filename.endswith('.ahc') or v_filename.endswith('.AHC'):
            ahc_path = os.path.join(directory, v_filename)
            csv_v_filename = f"{os.path.splitext(v_filename)[0]}.csv"
            csv_path = os.path.join(directory, csv_v_filename)
            
            #print(ahc_path)
            #print(csv_path)

            convert_ahc_to_csv(ahc_path, csv_path)
            print('Processado com Sucesso')
            
            if os.path.exists(f"{ahc_path}.process"):
                os.rename(ahc_path, f"{ahc_path}.already_exists")
            
            os.rename(ahc_path, f"{ahc_path}.process")
            print(f"Renomeado com sucesso: {ahc_path} - {ahc_path}.process")

def process_with_timeout(directory, timeout=60):
    process = multiprocessing.Process(target=process_directory, args=(directory,))
    process.start()
    process.join(timeout)
    if process.is_alive():
        print("Tempo limite excedido. Encerrando o processo.")
        process.terminate()
        process.join()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: ahc_to_csv precisa do diretório onde estão os arquivos .ahc")
    else:
        try:
            
            directory = sys.argv[1]
            
            process_with_timeout(directory, timeout=60)
        except Exception as e:
            print('Erro :', e)

