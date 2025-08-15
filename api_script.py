
import requests
import csv
import os

# Substitua com sua chave de API da Alpha Vantage
# Você pode obter uma chave gratuita em https://www.alphavantage.co/support/#api-key
ALPHA_VANTAGE_API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"

def get_stock_data_from_api(ticker):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API para {ticker}: {e}")
        return None
    except ValueError:
        print(f"Erro ao decodificar JSON da API para {ticker}. Resposta: {response.text}")
        return None

    if "Global Quote" in data and data["Global Quote"]:
        quote = data["Global Quote"]
        formatted_data = {
            "Ticker": quote.get("01. symbol"),
            "Preco_Atual": quote.get("05. price"),
            "Variacao": quote.get("10. change percent"),
            "Volume": quote.get("06. volume"),
            "Ultima_Atualizacao": quote.get("07. latest trading day")
        }
        return formatted_data
    else:
        print(f"Nenhum dado encontrado para o ticker {ticker} na API. Resposta: {data}")
        return None

def save_to_csv(data, filename='dados_acoes_api.csv'):
    if not data:
        print("Nenhum dado para salvar.")
        return

    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["Ticker", "Preco_Atual", "Variacao", "Volume", "Ultima_Atualizacao"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists or os.stat(filename).st_size == 0:
            writer.writeheader()  # Escreve o cabeçalho apenas se o arquivo não existir ou estiver vazio
        
        writer.writerow(data)
    print(f"Dados salvos em {filename}")

if __name__ == "__main__":
    tickers = ["IBM", "TSLA", "AMZN"] # Exemplos de tickers
    all_api_data = []

    for ticker in tickers:
        print(f"Coletando dados da API para {ticker}...")
        api_data = get_stock_data_from_api(ticker)
        if api_data:
            all_api_data.append(api_data)
    
    # Salvar todos os dados coletados em um único arquivo CSV
    if all_api_data:
        filename = 'dados_acoes_api.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["Ticker", "Preco_Atual", "Variacao", "Volume", "Ultima_Atualizacao"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_api_data)
        print(f"Todos os dados da API foram salvos em {filename}")
    else:
        print("Nenhum dado da API foi coletado para salvar.")