"""Extract string constants and method names from secure_database.cpython-310.pyc"""
import marshal
import types

with open('__pycache__/secure_database.cpython-310.pyc', 'rb') as f:
    f.read(16)
    code = marshal.load(f)

out = open('decompile_out.txt', 'w', encoding='utf-8')

def extract_info(code_obj, indent=0):
    prefix = "  " * indent
    out.write(f"{prefix}=== {code_obj.co_name} ===\n")
    out.write(f"{prefix}  varnames: {code_obj.co_varnames}\n")
    out.write(f"{prefix}  names: {code_obj.co_names}\n")
    
    for c in code_obj.co_consts:
        if isinstance(c, str):
            out.write(f"{prefix}  STR: {repr(c[:500])}\n")
        elif isinstance(c, bytes):
            out.write(f"{prefix}  BYTES: {repr(c[:500])}\n")
        elif isinstance(c, (int, float)):
            out.write(f"{prefix}  NUM: {c}\n")
    
    for c in code_obj.co_consts:
        if isinstance(c, types.CodeType):
            extract_info(c, indent + 1)

extract_info(code)
out.close()
print("Done - output written to decompile_out.txt")
