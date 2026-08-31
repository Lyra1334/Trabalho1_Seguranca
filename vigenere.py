from unicodedata import combining, normalize


def RemoverAcentos(texto: str):
    output = ""
    letra_latina = False
    for char in normalize("NFD", texto):
        if combining(char) and letra_latina:
            continue
        if not combining(char):
            letra_latina = char.isascii() and char.isalpha()
        output += char
    return normalize("NFC", output)


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
    mensagem = RemoverAcentos(mensagem)
    chave = RemoverAcentos(chave)
    if not chave:
        raise ValueError("Key must not be empty.")
    output = ""
    position = 0
    #position é a posição atual na chave


    for letra in mensagem:
        if letra.isascii() and letra.isalpha():
            output += LetterShift(letra, chave[position])
            # A chave só avança quando uma letra é cifrada.
            position = (position+1)%len(chave)
        else:
            output += letra
    return output

def Decodificar(mensagem:str, chave:str):
    mensagem = RemoverAcentos(mensagem)
    chave = RemoverAcentos(chave)
    if not chave:
        raise ValueError("Key must not be empty.")
    output = ""
    position = 0
    #position é a posição atual na chave
    
    
    for letra in mensagem:
        if letra.isascii() and letra.isalpha():
            output += LetterShift(letra, chave[position], False)
            # Mantém o mesmo alinhamento usado por Codificar.
            position = (position+1)%len(chave)
        else:
            output += letra
    return output


if __name__ == "__main__":
    from cli import main

    main()
