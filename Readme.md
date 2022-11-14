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
       **Entendimento de negócio:** Entender um pouco mais sobre o modelo de vendas cross-sell e como melhor aplicá-lo no modelo para aumentar o faturamento da empresa e melhorar a experiência dos clientes. Com os resultados em mãos iniciar as ofertas e discutir a possibilidade de mais orçamento para ampliar o número de ligações para cobrir toda a base possivelmente mais interessada no seguro. 
    </li>
    <li>
        
    </li>
    <li>
        
    </li>
    <li>
        
    </li>
    <li>
        
    </li>
    <li>
        
    </li>
    <li>
        
    </li>
    <li>
        
    </li>
    <li>
        
    </li>
</ol>
