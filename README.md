
# Desigualdade Social e Pobreza vs Criminalidade

**Autores da pesquisa:** Leandro Filipe Pereira Silva, Daniel Henrique  
**Disciplina:** Modelagem e programação estatística  
**Tema:** Desigualdade Social e Pobreza vs Criminalidade  
**Amostra:** Municípios de São Paulo no ano de 2010  

### Comando para rodar a Dashboard:

    python -m streamlit run Dashboard1.py

> **Observação:** Confira se o terminal está no mesmo diretório/pasta que a dashboard antes de rodar, se não estiver digite `cd Dashboard` para entrar na mesma pasta, e assim rodar com sucesso.

---

## Introdução
Nessa pesquisa estudamos a relação entre a desigualdade social e pobreza, com a violência. Nossa hipótese é que quanto mais desigual e/ou pobre for um local - Município nesse caso -, maior será os índices de violência - Taxa de homicídio por 100k habitantes foi o índice observado.

### Mapa 1 (Distribuição da violência):
Nesse mapa é fácil observar que a violência está concentrada em alguns mumicípios de São Paulo. Não há uma distribuição uniforme aproximada entre os municípios, ou seja, todos os municípios não são muito violentos, da mesma forma que todos não são pacíficos de forma semelhante ou aproximada. O que acontece é que no geral, os municípios são bem menos violentos do que os que se destacam, isso faz concluir que o problema nesse ano, relacionado a violência, está, de forma notável, se concentrando em algumas regiões, que podem ser chamadas de “outliers” por ter esse índice - Taxa de homicídio por 100k habitantes - significativamente maior do que a maioria dos outros municípios.

**Conclusão desse mapa:** A distribuição de violencia por município em SP, ocorre de forma concentrada.

### Tabela 1 (Os 10 Municípios com Maiores Taxas):
Essa tabela filtra exatamente esses “outliers”, classificando os 10 municípios com as maiores taxas. Ou seja, esses foram os 10 municípios mais violêntos de SP no ano de 2010, usando como métrica a taxa de homicídios por 100k habitantes.

### Mapa 2 (Desigualdade Social)
Esse mapa, que também é de calor, ilustra a distribuição da desigualdade social das regiões, sob a métrica do Índice de Gini, que vai de 0 a 1, sendo 0 um lugar onde a distribuição da renda seja exatamente igual, e 1 é o máximo da desigualdade, traduzindo uma extrema diferença financeira entre a população. O gráfico nos mostra que o estado de SP é significativamente desigual, com regiões mais do que outras, mas nesse caso, não há uma notoriedade de tantos “outiliers” quanto o gráfico anterior. A nossa hipótese até esse ponto, era que ao comparar a violência com a desigualdade, seria notado a relação: os lugares mais desiguais coincidem com os mais violentos.

**Conclusão desse mapa:** O estado de São Paulo pode ser considerado desigual.

### Tabela 2 (Os 10 Municípios mais Desiguais)
Nessa tabela, a hipótese inicial começa a não ser comprovada. O município mais desigual, é a capital São Paulo, e Campinas, que foi o mais violento do ano, não assumiu a posição de destaque esperada, pelo menos entre os top 3, que fortaleceria a hipótese ao demonstrar que a região mais violenta está entre as 3 mais desiguais. Outros que apareceram na tabela descredibilisam ainda mais a hipótese, pois regiões como “Águad de Lindóia”, e “Amparo”, que são, respectivamente, o segundo e o terceiro município mais desigual de SP, nem aparecem entre os 10 mais violentos esse ano.

**Conclusão dessa tabela:** Os municípios começam a demonstrar não obedecer a relação diretamente proporcional entre desigualdade e violência.

### Gráfico 3 (Análise de Correlação da Renda)
Esses gráficos fortalecem ainda mais a não coerência dos dados com a hipótese inicial. Se a hipótese se provasse verdadeira, iriamos notar uma “linha” crescente, da esquerda para a direita, que demonstraria de fato, os municípios mais desiguais e mais pobres são os mais violentos. O que aconteceu, foi que os dados seguem uma distribuição “aleatória”, que não comprova a relação prevista.

### Matriz de Correlação: Resumo Estatístico
Aqui, a hipótese é falseada definitivamente, não existiu a relação prevista esse ano, ou não existiu de forma consistente o suficiente. O que demonstra a particularidade desse estado. Uma das possível causa para essa relação não ter sido observada, é a forte presença da facção PCC, onde literalmente o crime (incluindo a violência) ocorre de forma organizada, ou seja; não acontece de forma deliberada e espontânea como em outros lugares.

## Conclusão:
Ao contrário da literatura clássica, os dados de SP em 2010 refutam a hipótese de correlação linear direta. Isso sugere que, neste estado, dinâmicas locais de segurança pública ou crime organizado pesam mais do que a economia pura.