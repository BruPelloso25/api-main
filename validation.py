import re 

def validar_email(email): 
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None 

def validar_cpf(cpf): 
    return re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf) is not None