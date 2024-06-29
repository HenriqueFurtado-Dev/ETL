import requests
import pandas as pd

class DadosRepositorios:
    # inicia o construtor da classe
    def __init__(self, owner): # o self é usado para as variaveis de instância 
        self.owner = owner # variável de instância pode ser utilizada em qualquer método da classe
        self.api_base_url = 'https://api.github.com'
        self.access_token = ''
        self.headers = {'Authorization' : 'Bearer' + self.access_token, 
           'X-GitHub-Api-Version':'2022-11-28'}
        
    def lista_repos(self):
        self.repos_list = []

        user_url = f'{self.api_base_url}/users/{self.owner}'
        response_user = requests.get(user_url, headers = self.headers)
        user = response_user.json()
        pages_repos = user['public_repos']
        pages = round(pages_repos // 30) + 1

        for page in range(1, self.pages):
            try:
                self.url = f'{self.api_base_url}/users/{self.owner}/repos?page={page}'
                self.response = requests.get(self.url, headers=self.headers)
                self.repos_list.append(self.response.json())
            except:
                print('Página não encontrada')
                self.repos_list.append(None)

        return self.repos_list

    def nomes_repos(self):
        repos_name = []
        for page in self.repos_list:
            for repository in page:
                try:
                    repos_name.append(repository['name'])
                except:
                    pass
            
        return repos_name
    
    def nomes_linguagens(self):
        repos_language = []
        for page in self.repos_list:
            for repository in page:
                try:
                    repos_language.append(repository['language'])
                except:
                    pass

        return repos_language
    
    def cria_df_linguagens(self):
        
        repositorios = self.lista_repos() # chama a lista de repositorios
        nomes = self.nomes_repos() # varre o nome de todos os repositorios
        linguagens = self.nomes_linguagens() # busca a linguagem de todos os repositorios

        dados = pd.DataFrame() # cria um dataframe vazio
        dados['Repositorios'] = nomes # cria a coluna Repositorios com os nomes
        dados ['Linguagens'] = linguagens # cria a coluna Linguagens com as linguagens

        return dados # retorna o dataframe

amazon_rep = DadosRepositorios('amzn') # instancia um objeto
ling_mais_usadas_amzn = amazon_rep.cria_df_linguagens() # chama o método cria_df_linguagens



netflix_rep = DadosRepositorios('netflix') 
ling_mais_usadas_netflix = netflix_rep.cria_df_linguagens() 


spotify_rep = DadosRepositorios('spotify')
ling_mais_usada_spotify = spotify_rep.cria_df_linguagens()


# salvando os dados
ling_mais_usadas_amzn.to_csv('/dados/linguagens_amazon.csv')
print('AMAZON - Dados salvos com sucesso')

ling_mais_usadas_netflix.to_csv('/dados/linguagens_netflix.csv')
print('NETFLIX - Dados salvos com sucesso')

ling_mais_usada_spotify.to_csv('/dados/linguagens_spotify.csv')
print('SPOTIFY - Dados salvos com sucesso')
