import base64
import subprocess
import tempfile
import os
import time
import filecmp


def createTempFile(value,ext=".py"):
     input_file_path=""
     with tempfile.NamedTemporaryFile(mode='w', suffix=ext, delete=False) as temp_file:
            temp_file.write(value)
            input_file_path = temp_file.name
     return input_file_path 

def prepareFiles(code,inp,out):
    code = (base64.b64decode(code)).decode('utf-8')
    inp = (base64.b64decode(inp)).decode('utf-8')
    out = (base64.b64decode(out)).decode('utf-8')
    code_path = createTempFile(code)
    inp_path = createTempFile(inp,".txt")
    out_path = createTempFile(out,".txt")
    return [code_path,inp_path,out_path]

def cleanFiles(fileList):
     for fpath in fileList:
          os.remove(fpath)
          
def execute(code,inp,out):
    #Convert the code from base64 to meaning full code
    [code_path,inp_path,out_path]=prepareFiles(code,inp,out)

    batch_script_content = f"""@echo off
    python {code_path} < {inp_path}
    """
    bat_file_path = createTempFile(batch_script_content,".bat")


    start_time = time.time()
    completed_process = subprocess.run(
        bat_file_path,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,  # Set to True if you want text output (Python 3.5+)
    )
    end_time = time.time()


    execution_time = (end_time - start_time)/1000

    result_path = createTempFile(completed_process.stdout,".txt")
    
    result = {}
    if len(completed_process.stderr) > 0 :
       result = {
            "status" : "CompileError",
            "output" : completed_process.stderr,
            "execution_time" :execution_time
       }
    else:
           status = "Pass" if filecmp.cmp(result_path, out_path) else "Fail"
           result = {
            "status" : status,
            "output" : completed_process.stdout,
            "execution_time" :execution_time
       }

    cleanFiles([code_path,inp_path,out_path,bat_file_path])
    return result

# code ="""
# def sum(a,c,b):
#     return f'{a}{c}{b}'
# a=input()
# c=input()
# b=input()
# print(sum(a,c,b))
# """
# #encode the code
# inp="""1
# s
# 2
# """
# out="""1s2
# """

# encoded_code = base64.b64encode(code.encode('utf-8'))
# encoded_inp = base64.b64encode(inp.encode('utf-8'))
# encoded_out = base64.b64encode(out.encode('utf-8'))
# print(execute(encoded_code,encoded_inp,encoded_out))

