import os

def verificar_amostras(pasta, arquivo_amostras):
    # Ler as amostras disponíveis do arquivo
    with open(arquivo_amostras, "r") as file:
        amostras_disponiveis = [linha.strip() for linha in file]

    # Obter os nomes de todos os arquivos .bam na pasta
    arquivos_bam = [f for f in os.listdir(pasta) if f.endswith(".bam")]

    # Verificar amostras que estão faltando
    amostras_faltantes = []
    for amostra in amostras_disponiveis:
        # Verifica se algum arquivo contém o padrão da amostra
        if not any(amostra in arquivo for arquivo in arquivos_bam):
            amostras_faltantes.append(amostra)

    # Salvar as amostras faltantes em um arquivo
    nome_arquivo_faltantes = "amostras_faltantes.txt"
    with open(nome_arquivo_faltantes, "w") as file:
        file.write("\n".join(amostras_faltantes))

    print(f"As amostras faltantes foram salvas no arquivo '{nome_arquivo_faltantes}'.")

# Exemplo de uso:
# Substitua 'minha_pasta' e 'amostras_disponiveis.txt' pelos caminhos corretos
pasta = "/media/lab/Data1/longReads/R10_1KG/"
arquivo_amostras = "amostras_disponiveis.txt"

verificar_amostras(pasta, arquivo_amostras)
