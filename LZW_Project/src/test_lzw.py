from trie import Trie
from utils import read_file, write_file, file_size
from lzw import lzw_compress, lzw_decompress

def test_trie():
    trie = Trie()
    trie.insert("abc", 1)
    trie.insert("abcd", 2)
    trie.insert("ab", 3)

    assert trie.search("abc") == 1
    assert trie.search("abcd") == 2
    assert trie.search("ab") == 3
    assert trie.search("xyz") is None

    trie.delete("abcd")
    assert trie.search("abcd") is None
    assert trie.search("abc") == 1

    print("Teste da Trie: OK")

def test_compression_and_decompression():
    data = "Este é um teste simples para LZW."
    compressed_data, _ = lzw_compress(data)
    decompressed_data, _ = lzw_decompress(compressed_data)
    assert data == decompressed_data, "Erro: os dados descomprimidos não coincidem com os originais!"

    print("Compressão e descompressão de texto: OK")

    input_file = "../data/sample.txt"
    compressed_file = "../data/compressed.lzw"
    decompressed_file = "../data/decompressed.txt"

    data = read_file(input_file)
    compressed_data, _ = lzw_compress(data)
    write_file(compressed_file, compressed_data, binary=True)
    compressed_data = read_file(compressed_file, binary=True)
    decompressed_data, _ = lzw_decompress(compressed_data)
    write_file(decompressed_file, decompressed_data)

    assert data == decompressed_data, "Erro: os dados descomprimidos não coincidem com os originais!"
    print("Compressão e descompressão de arquivo: OK")

if __name__ == "__main__":
    test_trie()
    test_compression_and_decompression()
