from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração de opções do Chrome
options = Options()
options.add_argument('--headless')  # Rodar sem interface gráfica
options.add_argument('--no-sandbox')  # Necessário para ambientes root
options.add_argument('--disable-dev-shm-usage')  # Resolve problemas de memória compartilhada

# Caminho do ChromeDriver
service = Service("/usr/local/bin/chromedriver")

# URL a ser acessada
url = "https://s3.amazonaws.com/1000g-ont/index.html?prefix=ALIGNMENT_AND_ASSEMBLY_DATA/100_PLUS/IN-HOUSE_MINIMAP2/"

# Inicializar o WebDriver
driver = webdriver.Chrome(service=service, options=options)

try:
    # Acessar a página
    driver.get(url)
    print(f"Título da página: {driver.title}")

    # Esperar até que todos os links estejam presentes
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

    # Coletar todos os links
    links = [a.get_attribute("href") for a in driver.find_elements(By.TAG_NAME, "a")]

    # Filtrar links que contêm "R10"
    links_r10 = [link for link in links if "R10" in link]

    # Exibir os links encontrados
    print(f"Links com 'R10': {links_r10}")
    
    # Padrão a ser removido
    padrao = "https://s3.amazonaws.com/1000g-ont/index.html?prefix=ALIGNMENT_AND_ASSEMBLY_DATA/100_PLUS/IN-HOUSE_MINIMAP2/"

    # Remover o padrão e criar uma nova lista
    Amostras_r10 = [link.replace(padrao, "") for link in links_r10]
    
    # Extrair apenas a primeira sequência até o primeiro "-"
    Amostras_r10_formatadas = [link.split("-")[0] for link in Amostras_r10]

    # Nome do arquivo de saída
    nome_arquivo = "amostras_disponiveis.txt"

    # Salvar os nomes extraídos em um arquivo txt
    with open(nome_arquivo, "w") as file:
        file.write("\n".join(Amostras_r10_formatadas))

    print(f"As amostras foram salvas no arquivo '{nome_arquivo}'.")

except Exception as e:
    print(f"Erro durante a execução: {e}")

finally:
    # Fechar o navegador
    driver.quit()
