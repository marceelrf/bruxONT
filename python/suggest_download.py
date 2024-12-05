from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def contem_amostra(palavra,padrao) -> bool:
  return re.search(padrao, palavra) is not None

def gerar_comandos_wget(url_base, arquivo_faltantes, arquivo_saida):
    # Configuração de opções do Chrome
    options = Options()
    options.add_argument('--headless')  # Rodar sem interface gráfica
    options.add_argument('--no-sandbox')  # Necessário para ambientes root
    options.add_argument('--disable-dev-shm-usage')  # Resolve problemas de memória compartilhada

    # Caminho do ChromeDriver
    service = Service("/usr/local/bin/chromedriver")

    # Inicializar o WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    try:
        # Acessar a página
        driver.get(url_base)
        print(f"Título da página: {driver.title}")

        # Esperar até que todos os links estejam presentes
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

        # Coletar todos os links
        links = [a.get_attribute("href") for a in driver.find_elements(By.TAG_NAME, "a")]

        # Filtrar links que contêm "R10"
        links_r10 = [link for link in links if "R10" in link]
        
        # Ler a lista de amostras faltantes
        with open(arquivo_faltantes, "r") as file:
            amostras_faltantes = [linha.strip() for linha in file]
        
        # Filtrar links que contêm alguma amostra faltante e um padrão adicional
        links_filtrados = [link for link in links_r10 if any(re.search(rf"\b{amostra}\b", link) for amostra in amostras_faltantes)]
        
        
        wget_list = []
        # Acessar os links filtrados para pegar os links de BAMs
        for links in links_filtrados:
            driver.get(links)
            
            # Esperar até que todos os links estejam presentes
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

            # Coletar todos os links
            links = [a.get_attribute("href") for a in driver.find_elements(By.TAG_NAME, "a")]

            # Filtrar links que contêm "bam" ou ".bai"
            links_r10_bam = [link for link in links if ".bam" in link]
            # links_r10_bai = [link for link in links if ".bai" in link]
            
            for i in links_r10_bam:
                wget_list.append(i)
            
            
        comandos_wget = map(lambda x: f"wget {x} --continue", wget_list)
        # Exportar arquivo com comando WGET
        # Salvar os comandos wget em um arquivo
        with open(arquivo_saida, "w") as file:
            file.write("\n".join(comandos_wget))

    except Exception as e:
        print(f"Erro durante a execução: {e}")

    finally:
        # Fechar o navegador
        driver.quit()

# URL base do site (mantenha a barra no final para concatenar com os links)
url_base = "https://s3.amazonaws.com/1000g-ont/index.html?prefix=ALIGNMENT_AND_ASSEMBLY_DATA/100_PLUS/IN-HOUSE_MINIMAP2/"

# Caminho para o arquivo com as amostras faltantes
arquivo_faltantes = "amostras_faltantes.txt"

# Nome do arquivo de saída com os comandos wget
arquivo_saida = "comandos_wget.txt"

# Executar a função
gerar_comandos_wget(url_base, arquivo_faltantes, arquivo_saida)
