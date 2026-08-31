# Cifra de Vigenere

Programa de linha de comando para criptografar e descriptografar mensagens
com a cifra de Vigenère.

## Uso

```bash
python -m vigenere encrypt CHAVE "mensagem"
python -m vigenere decrypt CHAVE "mensagem criptografada"
python -m vigenere encrypt CHAVE -f mensagem.txt
python -m vigenere decrypt CHAVE -f mensagem.txt
python -m vigenere encrypt CHAVE -f mensagem.txt -o criptografada.txt
python -m vigenere decrypt CHAVE -f criptografada.txt -o mensagem.txt
python -m vigenere break mensagem.txt
python -m vigenere break mensagem.txt --pt-br
```

Os comandos leem e escrevem arquivos em UTF-8. A cifra remove os acentos de
letras latinas antes de aplicar o deslocamento de `A` a `Z`. A chave avança
somente quando uma letra ASCII é processada. Outros alfabetos, emoji e símbolos
são preservados. A opção `-o` (ou `--output`) grava o resultado no arquivo
indicado; sem ela, o resultado é exibido no terminal.
O comando `break` usa frequências de letras do inglês por padrão. Use `--pt-br`
para analisar um texto em português brasileiro.
