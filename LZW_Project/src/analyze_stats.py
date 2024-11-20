import json
import matplotlib.pyplot as plt
import argparse
import os

def load_stats(stats_file):
    if not os.path.exists(stats_file):
        raise FileNotFoundError(f"O arquivo '{stats_file}' não foi encontrado.")
    
    with open(stats_file, "r") as file:
        stats = json.load(file)
    
    required_keys = ["dictionary_size", "memory_usage", "execution_time"]
    if "compression_ratio" in stats: 
        required_keys.append("compression_ratio")
    for key in required_keys:
        if key not in stats:
            raise KeyError(f"Campo '{key}' ausente no arquivo de estatísticas.")
    
    return stats

def plot_stats(stats, title="Estatísticas do Algoritmo LZW"):
    labels = ["Taxa de Compressão", "Tamanho do Dicionário", "Uso de Memória (KB)", "Tempo de Execução (s)"]
    values = [
        stats.get("compression_ratio", 0), 
        stats["dictionary_size"],
        stats["memory_usage"],
        stats["execution_time"]
    ]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color="skyblue")
    plt.title(title)
    plt.ylabel("Valores")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analisador de estatísticas de compressão/descompressão LZW.")
    parser.add_argument("stats_file", help="Arquivo JSON contendo as estatísticas.")
    parser.add_argument("--title", default="Estatísticas do Algoritmo LZW", help="Título do gráfico (opcional).")

    args = parser.parse_args()

    try:
        stats = load_stats(args.stats_file)
        plot_stats(stats, title=args.title)
    except (FileNotFoundError, KeyError) as e:
        print(f"Erro: {e}")
