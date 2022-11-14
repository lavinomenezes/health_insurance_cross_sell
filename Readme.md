# Health Insurance Cross Sell

## Problema de negócio

A Insurance all é uma empresa fictícia de seguros de saúde cujo time de produtos está analisando o aumento do portfólio de serviços da empresa com a criação de um seguro automotivo. A partir disso, realizou uma pesquisa com cerca de 380 mil clientes que já possuem seguro de saúde sobre o interesse em contratar esse novo produto.

Para iniciar a oferta do novo seguro, a equipe de produtos selecionou 114090 mil novos clientes para receber a oferta pelo time de vendas através de ligações telefônicas. Entretanto, a equipe de vendas só tem capacidade para efetuar 20 mil ligações no período da campanha.

Assim foi solicitado à equipe de dados para construir um modelo que priorizasse os clientes que estariam mais interessados em contratar o seguro. Assim, ordenando essa lista de 114090 mil clientes de forma que aqueles com maior chance de contratar o seguro estejam no início dela.

**Dataset overview**


| **Variable** | **Meaning** |



## Questões do negócio.
<ol>
    
<li>
Principais Insights sobre os atributos mais relevantes de clientes interessados em adquirir um seguro de automóvel.
</li>
<li>Qual a porcentagem de clientes interessados em adquirir um seguro de automóvel, o time de vendas conseguirá contatar fazendo 20.000 ligações?
</li>
<li>
 E se a capacidade do time de vendas aumentar para 40.000 ligações, qual a porcentagem de clientes interessados em adquirir um seguro de automóvel o time de vendas conseguirá contatar?
</li>
<li>
 Quantas ligações o time de vendas precisa fazer para contatar 80% dos clientes interessados em adquirir um seguro de automóvel?
</li>
</ol>

## Premissas de negócio
<ul>
    <li>
    A variável “response”, que representa a resposta a pesquisa, está desbalanceada com 87,13 % de respostas negativas (response = 0) e 12,87% com respostas positivas (response=1), mas no primeiro ciclo não houve nenhum processo de balanceamento dos dados;
    </li>
    <li>
    A varíavel “driving_license” em sua grande maioria (99,79%) possui respostas positivas (1), sendo que apenas 41 clientes que não possuem licença (0) estão interessados no seguro. Assim, a coluna foi excluída por não trazer informações ao modelo;
    </li>
    <li>
    Apenas 0.04% dos veículos dos clientes na pesquisa tem mais de 2 anos de uso, isso num momento inicial pode mascarar o comportamento da resposta quando comparado aos outros períodos de uso;
    </li>
    <li>
    O “policysaleschannel” possui 155 formas de contato, mas não foi informado que método é referente a cada número.
A variável “annual_premium” está cotada em rúpias indianas, ao final nos resultados financeiros será convertida em dólares para melhor entendimento. A cotação utilizada será do dia 08/11/2022.
    </li>
</ul>

## Planejamento de solução

Neste projeto foi aplicado o método CRISP-DM (Cross-Industry Standard Process for Data Mining) adaptado para os processos de ciência de dados que se tornaram CRIS-DS.

A divisão dos passos utilizados no projeto foi:
<ol>
    <li>
       <strong>Entendimento de negócio:</strong> Entender um pouco mais sobre o modelo de vendas cross-sell e como melhor aplicá-lo no modelo para aumentar o faturamento da empresa e melhorar a experiência dos clientes. Com os resultados em mãos iniciar as ofertas e discutir a possibilidade de mais orçamento para ampliar o número de ligações para cobrir toda a base possivelmente mais interessada no seguro. 
    </li>
    <li>
        <strong>Coleta de dados:</strong> Os dados foram coletados de um banco de dados através de uma query  SQL, antes distribuídos em 3 datasets diferentes foram unidos com base no id de cada cliente para iniciar a análise.
    </li>
    <li>
        <strong>Análise descritiva:</strong> uma breve análise dos dados para adquirir familiaridade com os mesmo, os dados foram divididos em numéricos e categóricos, para aplicar os métodos de análise corretos para cada tipo.
    </li>
    <li>
        <strong>Dados faltantes:</strong> Não foram encontrados dados faltantes no dataframe.
    </li>
    <li>
       <strong>Feature engineering:</strong> No primeiro ciclo do projeto foi decidido não criar nenhuma nova variável, apenas algumas das variáveis categóricas tiveram seus valores transformados para melhor performance do algoritmo. Sendo elas: 
       <ul>
           <li>
               gender: Male = 0, Female = 1;
           </li>
           <li>
               vehicle_damage: Yes = 1, No = 0.
           </li>
       </ul>
    </li>
    <li>
       <strong>Filtragem de dados:</strong> Remoção de colunas que não tem impacto no modelo. Remoção de linhas que não contribuem com o modelo. Sendo eles:
        <ul>
            <li>
               Colunas removidas: 'driving_license’; 
            </li>
            <li>
               Linhas removidas: as que na coluna 'driving_license’ tinha resposta negativa (0).
            </li>
        </ul>
    </li>
    <li>
        <strong>Análise exploratória de dados:</strong> Criar e validar hipóteses de negócio para melhor entendimento do comportamento dos dados em relação a variável alvo e como elas se influenciam, e definir quais atributos são importantes para o modelo. Junto com uma análise de correlação entre variáveis aplicado e método correto para que variáveis numéricas e categóricas sejam corretamente comparadas. Sendo elas:
        <ul>
            <li>
               cramer v: categórica vs categórica; 
            </li>
            <li>
               Point-biserial: numérica vs categórica.
            </li>
        </ul>
    </li>
    <li>
        <strong>Preparação dos dados:</strong> Manipular os dados para se adequarem melhor num modelo de machine learning.
        <ul>
            <li>
                Re-escala dos atributos numéricos para não força o modelo a trabalhar com valores muito altos: 
                <ul>
                    <li>
                        MinMaxscaler: ‘age’ e ‘vintage’;
                    </li>
                    <li>
                        StandardScale: ‘annual_premium’.
                    </li>
                </ul>
            </li>
            <li>
                Encoding das variáveis categóricas:
                <ul>
                    <li>
                        Ordinal encoding:  ‘vehicle_age’. 
                    </li>
                </ul>
            </li>
        </ul>
        Ao final as escalas foram salvas no formato pickle para serem aplicadas no dataset de treino.
    </li>
    <li>
        <strong>Feature selection:</strong> Neste primeiro ciclo do CRISP foi utilizado o algoritmo boruta para definir os atributos que iremos utilizar no treinamento, só que o algoritmo estava apenas retornando uma variável, logo não seria possível montar um modelo com apenas uma variável. Então, foi aplicado o método de feature importance para definir o peso que os atributos tem no modelo.

        <img title="a title" alt="Alt text" src="https://github.com/lavinomenezes/health_insurance_cross_sell/blob/main/image/feature_importance.png">
       
        Após os resultados foi decidido que a variável gênero fosse excluída do treinamento do modelo final. 
    </li>
</ol>
