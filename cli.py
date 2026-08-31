import argparse
from pathlib import Path

try:
    from .quebra import ENGLISH_FREQUENCIES, PT_BR_FREQUENCIES, decode_file
    from .vigenere import Codificar, Decodificar
except ImportError:
    from quebra import ENGLISH_FREQUENCIES, PT_BR_FREQUENCIES, decode_file
    from vigenere import Codificar, Decodificar


def ler_mensagem(args):
    if args.arquivo:
        return args.arquivo.read_text(encoding="utf-8")
    return args.mensagem


def executar_cifra(args):
    mensagem = ler_mensagem(args)
    resultado = args.funcao(mensagem, args.chave)
    if args.saida:
        args.saida.write_text(resultado, encoding="utf-8")
    else:
        print(resultado)


def executar_quebra(args):
    frequencies = PT_BR_FREQUENCIES if args.pt_br else ENGLISH_FREQUENCIES
    resultado = decode_file(str(args.arquivo), frequencies)
    print(resultado)


def adicionar_entrada(parser):
    parser.add_argument("chave", help="chave da cifra")
    parser.add_argument(
        "-o", "--output", dest="saida", type=Path, help="arquivo de saída"
    )
    entrada = parser.add_mutually_exclusive_group(required=True)
    entrada.add_argument("mensagem", nargs="?", help="texto a processar")
    entrada.add_argument(
        "-f", "--file", dest="arquivo", type=Path, help="arquivo de entrada"
    )


def criar_parser():
    parser = argparse.ArgumentParser(description="Cifra de Vigenere")
    comandos = parser.add_subparsers(dest="comando", required=True)

    encrypt = comandos.add_parser("encrypt", help="criptografa uma mensagem")
    adicionar_entrada(encrypt)
    encrypt.set_defaults(funcao=Codificar, executar=executar_cifra)

    decrypt = comandos.add_parser("decrypt", help="descriptografa uma mensagem")
    adicionar_entrada(decrypt)
    decrypt.set_defaults(funcao=Decodificar, executar=executar_cifra)

    break_parser = comandos.add_parser("break", help="tenta quebrar um arquivo")
    break_parser.add_argument("arquivo", type=Path, help="arquivo de entrada")
    break_parser.add_argument(
        "--pt-br",
        action="store_true",
        help="usa frequências de letras do português brasileiro",
    )
    break_parser.set_defaults(executar=executar_quebra)

    return parser


def main():
    parser = criar_parser()
    args = parser.parse_args()

    try:
        args.executar(args)
    except (OSError, ValueError) as erro:
        parser.error(str(erro))


if __name__ == "__main__":
    main()
