import os

def read_file(file_path, binary=False, max_bits=12):
    mode = 'rb' if binary else 'r'
    with open(file_path, mode) as file:
        if binary:
            byte_size = (max_bits + 7) // 8
            return [int.from_bytes(file.read(byte_size), byteorder='big') for _ in range(file_size(file_path) // byte_size)]
        else:
            return file.read()

def write_file(file_path, data, binary=False, max_bits=12):
    mode = 'wb' if binary else 'w'
    with open(file_path, mode) as file:
        if binary:
            for num in data:
                file.write(num.to_bytes((max_bits + 7) // 8, byteorder='big'))
        else:
            file.write(data)

def file_size(file_path):
    return os.path.getsize(file_path)
