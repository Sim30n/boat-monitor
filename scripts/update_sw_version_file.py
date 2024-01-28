from sys import argv

file_path = argv[1]
sw_version = argv[2]

with open(file_path, "w") as file1:
    file1.write("#ifndef SW_VERSION_H\n")
    file1.write("#define SW_VERSION_H\n")
    file1.write("\n")
    file1.write(f'const char sw_version[] = "{sw_version}";\n')
    file1.write("\n")
    file1.write("#endif\n")