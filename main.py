import json
import os
import subprocess
num_of_prog=3
result={}
f=open('detail.json')
data=json.load(f)
f.close()
directory=data['directory']
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
    filename = file[0:-2]
    with open("error.txt","w") as error_file:
        subprocess.run(["gcc",file,"-o",f"{filename}.out"], stderr=error_file)
    err_f=open("error.txt","r")
    error=err_f.read()
    err_f.close()
    ans=0 
    if len(error)==0:
        print("C program Compiled Succesfully")
        with open("output.txt","w") as output_file:
            with open(directory+data[filename][0],"r") as input_file:
                subprocess.run([f"./{filename}.out"],stdout=output_file,stdin=input_file)
        output=open("output.txt","r").read().strip()
        actual_output=open(directory+data[filename][1],"r").read().strip()
        if(output==actual_output):
            print("Output Matched for",file)
            ans=1
        else:
            print("Ouput mismatched for",file)
        subprocess.run(["rm","output.txt"])
    else :
        print("Error Found in C program")
    subprocess.run(["rm","error.txt"])
    return ans
def cpp_compile(file):
    filename=file[0:-4]
    with open("error.txt","w") as error_file:
        subprocess.run(["g++",file,"-o",f"{file[0:-4]}.out"] , stderr=error_file)
    err_f=open("error.txt","r")
    error=err_f.read()
    err_f.close()
    ans=0
    if len(error)==0: 
        print("C++ program Compiled Succesfully")
        with open("output.txt","w") as output_file:
            with open(directory+data[filename][0],"r") as input_file:
                subprocess.run([f"./{file[0:-4]}.out"],stdout=output_file,stdin=input_file)
        output=open("output.txt","r").read().strip()
        actual_output=open(directory+data[filename][1],"r").read().strip()
        if(output==actual_output):
            print("Output Matched for",file)
            ans=1
        else:
            print("Ouput mismatched for",file)
            

        subprocess.run(["rm","output.txt"])
    else :
        print("Error Found in C++ program")
    subprocess.run(["rm","error.txt"])
    return ans
       
def py_compile(file):
    filename=file[0:-3]
    with open("error.txt","w") as error_file:
        with open("output.txt","w") as output_file:
            with open(directory+data[filename][0],"r") as input_file:
                subprocess.run(["python3",file],stderr=error_file,stdout=output_file,stdin=input_file)
    err_f=open("error.txt","r")
    error=err_f.read()
    err_f.close()
    ans=0 
    if len(error)==0:
        print("Python program Compiled Succesfully")
        output=open("output.txt","r").read().strip()
        actual_output=open(directory+data[filename][1],"r").read().strip()
        if(output==actual_output):
            print("Output Matched for",file)
            ans=1            
        else:
            print("Ouput mismatched for",file)

        subprocess.run(["rm","output.txt"])  
    else :
        print("Error Found in Python program")
    subprocess.run(["rm","error.txt"])
    return ans
zip_files=zip_files()
for file in zip_files:
    with open("log.txt","w") as log:
        subprocess.run(["unzip",file],stdout=log)
    subprocess.run(["rm","log.txt"])
for file in zip_files:
    folder_name = file[:-4]
    result[folder_name]=0
    os.chdir(folder_name)
    all_files=os.listdir()
    if len(all_files) < num_of_prog:
        print("Incomplete Assignment")
        continue
    subprocess.run(["pwd"])
    count=0
    cpp_files = list_cpp_files()
    for file in cpp_files:
        count+=cpp_compile(file)
    py_files=list_py_files()
    for file in py_files:
        count+=py_compile(file)
    c_files=list_c_files()
    for file in c_files:
        count+=c_compile(file)
    result[folder_name]=count
    os.chdir("../")
print(result)
    
