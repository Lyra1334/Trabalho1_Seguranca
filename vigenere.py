def LetterShift(char:str, shiftChar:str, sum:bool = True):
    #Char é o caractere original, shiftChar é o da chave
    #sum indica se vai "somar" ou "subtrair" o caractere
    code = ord(char)
    shift = ord(shiftChar)
    if char.isupper():
        code -= 65
    else:
        code -= 97

    if shiftChar.isupper():
        shift -= 65
    else:
        shift -= 97

    if sum:
        code = (code + shift)%26
    else:
        code = code - shift
        #corrigindo se der menor que 0
        if code < 0:
            code += 26

    #Mantém o caractere maiúsculo se o original era
    if char.isupper():
        return chr(code + 65)
    else:
        return chr(code + 97)

    
def Codificar(mensagem:str, chave:str):
    output = ""
    position = 0
    #position é a posição atual na chave


    for letra in mensagem:
        if letra.isalpha():
            output += LetterShift(letra, chave[position])
        else:
            output += letra
        #incrementa a posição pra próxima letra, e volta pro 0 se position = len(chave)
        position = (position+1)%len(chave)
    return output

def Decodificar(mensagem:str, chave:str):
    output = ""
    position = 0
    #position é a posição atual na chave
    
    
    for letra in mensagem:
        if letra.isalpha():
            output += LetterShift(letra, chave[position], False)
        else:
            output += letra
        #incrementa a posição pra próxima letra, e volta pro 0 se position = len(chave)
        position = (position+1)%len(chave)
    return output