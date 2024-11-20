import argparse
import time
import tracemalloc
import json
import os
from utils import read_file, write_file

def lzw_compress(data, max_bits=12):
    """Realiza a compressão usando o algoritmo LZW e coleta estatísticas."""
    max_table_size = 2 ** max_bits
    dictionary = {chr(i): i for i in range(256)}

    current_string = ""
    compressed_data = []
    next_code = 256 

    start_time = time.time()
    tracemalloc.start()

    for symbol in data:
        combined = current_string + symbol
        if combined in dictionary:
            current_string = combined
        else:
            compressed_data.append(dictionary[current_string])
            if next_code < max_table_size:
                dictionary[combined] = next_code
                next_code += 1
            current_string = symbol

    if current_string:
        compressed_data.append(dictionary[current_string])

    memory_usage, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.time()

    print(f"Tabela final de compressão: {len(dictionary)} entradas (limite: {max_table_size})")

    stats = {
        "compression_ratio": len(data) / len(compressed_data),
        "dictionary_size": next_code,
        "memory_usage": memory_usage / 1024,  # em KB
        "execution_time": end_time - start_time,
    }

    return compressed_data, stats

def lzw_decompress(compressed_data, max_bits=12):
    """Realiza a descompressão usando o algoritmo LZW e coleta estatísticas."""
    max_table_size = 2 ** max_bits
    dictionary = {i: chr(i) for i in range(256)} 
    current_code = compressed_data.pop(0)
    current_string = dictionary[current_code]
    result = [current_string]

    start_time = time.time()
    tracemalloc.start()

    next_code = 256  

    for code in compressed_data:
        print(f"Processando código: {code}, Limite: {max_table_size}")

        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:  
            entry = current_string + current_string[0]
        else:
            raise ValueError(f"Erro na descompressão. Código inválido: {code}")

        result.append(entry)

        
        if next_code < max_table_size:
            dictionary[next_code] = current_string + entry[0]
            next_code += 1

        current_string = entry

    memory_usage, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.time()

    stats = {
        "dictionary_size": len(dictionary),
        "memory_usage": memory_usage / 1024,  # em KB
        "execution_time": end_time - start_time,
    }

    return "".join(result), stats

def main():
    """Interface de linha de comando para compressão e descompressão."""
    parser = argparse.ArgumentParser(description="Algoritmo LZW para compressão e descompressão de arquivos.")
    parser.add_argument("mode", choices=["compress", "decompress"], help="Modo de operação: compress ou decompress")
    parser.add_argument("input_file", help="Arquivo de entrada")
    parser.add_argument("output_file", help="Arquivo de saída")
    parser.add_argument("--stats_file", default="stats.json", help="Arquivo para salvar estatísticas (padrão: stats.json)")
    parser.add_argument("--max_bits", type=int, default=12, help="Número máximo de bits (padrão: 12)")

    args = parser.parse_args()

    # Ler o arquivo de entrada
    if args.mode == "compress":
        data = read_file(args.input_file)
        compressed_data, stats = lzw_compress(data, max_bits=args.max_bits)
        write_file(args.output_file, compressed_data, binary=True, max_bits=args.max_bits)

        # Certifique-se de que o diretório do arquivo de estatísticas existe
        stats_dir = os.path.dirname(args.stats_file)
        if stats_dir and not os.path.exists(stats_dir):
            os.makedirs(stats_dir)

        with open(args.stats_file, "w") as stats_file:
            json.dump(stats, stats_file, indent=4)

        print(f"Arquivo {args.input_file} comprimido com sucesso em {args.output_file}!")
        print(f"Estatísticas salvas em {args.stats_file}")

    elif args.mode == "decompress":
        compressed_data = read_file(args.input_file, binary=True, max_bits=args.max_bits)
        decompressed_data, stats = lzw_decompress(compressed_data, max_bits=args.max_bits)
        write_file(args.output_file, decompressed_data)

        # Certifique-se de que o diretório do arquivo de estatísticas existe
        stats_dir = os.path.dirname(args.stats_file)
        if stats_dir and not os.path.exists(stats_dir):
            os.makedirs(stats_dir)

        with open(args.stats_file, "w") as stats_file:
            json.dump(stats, stats_file, indent=4)

        print(f"Arquivo {args.input_file} descomprimido com sucesso em {args.output_file}!")
        print(f"Estatísticas salvas em {args.stats_file}")

if __name__ == "__main__":
    main()
