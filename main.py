import os
import subprocess
num_of_prog=3
def zip_files():
    zip_file=[]
    all_files=os.listdir()
    for file in all_files:
        if file.endswith(".zip"):
            zip_file.append(file)
    return zip_file
def list_cpp_files():
    cpp_files=[]
    all_files=os.listdir()
    for file in all_files:
        if file.endswith(".cpp"):
            cpp_files.append(file)
    return cpp_files
def list_py_files():
    py_files=[]
    all_files=os.listdir()
    for file in all_files:
        if file.endswith(".py"):
            py_files.append(file)
    return py_files 
def list_c_files():
    c_files=[]
    all_files=os.listdir()
    for file in all_files:
        if file.endswith(".c"):
            c_files.append(file)
    return c_files
def c_compile(file):
   # subprocess.run(["gcc",file,"-o",file[]".out"],stdin=input_file , stderr=error_file)
    error=open("error_file","r") 
    if len(error)==0:
        print("C program Compiled Succesfully")
    #error.close()
   #subprocess.run([],stdout=outfile)
    else :
        print("Error Found in C program")
def cpp_compile(file):
    with open("error.txt","w") as error_file:
        subprocess.run(["g++",file,"-o",f"{file[0:-4]}.out"] , stderr=error_file)
    err_f=open("error.txt","r")
    error=err_f.read()
    err_f.close()
    if len(error)==0: 
        print("C++ program Compiled Succesfully")
        with open("output.txt","w") as output_file:
            subprocess.run([f"./{file[0:-4]}.out"],stdout=output_file)
        subprocess.run(["cat","output.txt"])
        subprocess.run(["rm","output.txt"])
    else :
        print("Error Found in C++ program")
    subprocess.run(["rm","error.txt"])
def py_compile(file):
   # subprocess.run(["python3,file],stdin=input_file , stderr=error_file,stdout=output_file)
    error=open("error_file","r") 
    if len(error)==0:
        print("Python program Compiled Succesfully")
    #error.close()
  # subprocess.run([],stdout=outfile)
    else :
        print("Error Found in Python program")

zip_files=zip_files()
for file in zip_files:
    with open("log.txt","w") as log:
        subprocess.run(["unzip",file],stdout=log)
    subprocess.run(["rm","log.txt"])
for file in zip_files:
    if len(zip_files) < num_of_prog:
        print("Incomplete Assignment")
        break
    folder_name = file[:-4]
    os.chdir(folder_name)
    subprocess.run(["pwd"])
    cpp_files = list_cpp_files()
    for file in cpp_files:
        cpp_compile(file)
  
    os.chdir("../")
