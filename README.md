# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<img width="200" height="50" alt="Image" src="https://github.com/user-attachments/assets/5746c27f-0276-4eb3-b7da-6f249578a58d" /></a>
</p>

<br>

# 🎓 Graduação ON em Inteligência Artificial  
## 📚 Global Solution 1º Semestre 2026

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/paulo-pereira-de-souza-junior-mba-msc-0b497825/">Paulo Pereira de Souza Junior</a>

## 👨‍🎓 Apresentacao: 
- <a href="https://youtu.be/VY23rVfZaIM">Video Apresentação - YOUTUBE</a>

## 👩🏻‍💻 Como a Inteligência Artificial e as tecnologias digitais podem transformar a nova economia espacial e gerar impacto positivo na Terra?

## 👩🏻‍💻 Linha de Pesquisa: Sistemas inteligentes de monitoramento climático utilizando dados espaciais
 
## 👩🏻‍💻 Uso dos dados do *Oceanic Niño Index (ONI)*, fornecidos pelo  <a href="https://www.cpc.ncep.noaa.gov/">NOAA Climate Prediction Center</a>  , para a previsão volume de chuvas e o mapeamento preventivo de áreas sujeitas a eventos climáticos extremos.

## 👩🏻‍💻 Contexto de Pesquisa.
A ONU alertou, segundo a BBC (Jun, 2026), que um novo evento do fenômeno climático natural El Niño pode iniciar em breve, elevando as temperaturas em um mundo já pressionado pelas mudanças climáticas. Outras fontes também indicam condições favoráveis para a ocorrência do fenômeno El Niño; segundo Conexaosafra (Jun, 2026), o status atual é de “El Niño Watch”, utilizado quando existem condições propícias para o desenvolvimento desse fenômeno. A possibilidade de formação do El Niño entre maio e julho de 2026 é de 82%. Para o intervalo de dezembro de 2026 a fevereiro de 2027, essa chance de persistência sobe para 96%. 

O fenômeno El Niño se caracteriza pelo aquecimento das águas do oceano Pacífico, enquanto o resfriamento das águas desse mesmo oceano caracteriza o fenômeno La Niña, conforme informações do INPE - Instituto Nacional de Pesquisas Espaciais (Out, 2024). Tanto o El Niño quanto a La Niña fazem parte de um fenômeno interligado (atmosférico-oceânico) que ocorre no oceano Pacífico Equatorial (e na atmosfera ao seu redor), denominado Oscilação Sul do El Niño (ENOS). A fase El Niño desse fenômeno acoplado ENOS se refere a situações em que o oceano Pacífico Equatorial está mais aquecido do que a média histórica (climatológica), enquanto a fase La Niña se refere à situação oposta, ou seja, quando o oceano Pacífico Equatorial está mais frio do que a média histórica. A variação na temperatura do oceano Pacífico Equatorial provoca efeitos globais nos padrões de circulação atmosférica, transporte de umidade, temperatura e precipitação.

As variações de temperatura do oceano Pacífico influenciam diretamente o clima brasileiro, especialmente os ciclos de El Niño e La Niña, de acordo com Globo Rural (Out, 2028). No Brasil, os efeitos são razoavelmente conhecidos e variam dependendo da região. Os impactos não são exatamente os mesmos a cada ano devido aos fatores que causam a variabilidade climática. Em anos em que o El Niño está ativo, as temperaturas tendem a aumentar no inverno, e o clima pode até se assemelhar ao do verão em algumas ocasiões. As maiores mudanças nas chuvas ocorrem no Rio Grande do Sul (Região Sul), onde as precipitações aumentam: "O inverno gaúcho já é normalmente úmido. Com o El Niño, isso se intensifica". No Nordeste, a situação é diferente. "Durante o verão, o El Niño provoca seca. No inverno, a falta de chuvas já é comum, mas, se não chover no verão, as colheitas de grãos são prejudicadas".

Por outro lado, a La Niña torna o clima no Rio Grande do Sul mais seco, o que é favorável para o cultivo de trigo. De acordo com o meteorologista, as condições para o cultivo desse cereal podem ser até melhores do que em anos neutros, já que, além de haver um pouco menos de chuva, as ondas de frio ocorrem com mais frequência. A diminuição da temperatura não costuma ser drástica a ponto de causar geadas. Na região Sul, assim como no litoral de São Paulo e do Rio de Janeiro, as temperaturas geralmente caem sob a influência da La Niña. "Tanto as mínimas quanto as máximas ficam mais baixas", explica Celso. No entanto, em muitas regiões produtoras do interior do Sudeste e do Centro-Oeste, os anos de La Niña apresentam uma maior amplitude térmica: tardes quentes, mas noites e madrugadas mais frias do que a média. "Isso ocorre porque a La Niña torna o clima de outono e inverno ainda mais seco no interior do país. Inclusive, a seca que experimentamos no primeiro semestre foi um resquício de sua última atuação".
- ...
<p align="center">
<img width="785" height="480" alt="Image" src="https://github.com/user-attachments/assets/2b081288-cead-489a-8ddc-b60f85c65ff5" /></a>
</p>
---

## 🎯 Objetivo

Este trabalho tem como objetivo:

- 📌 Criar estrutura de dados armazenamento de informações climaticas históricas
- 📌 Processar informações de clima e condições climaticas
- 📌 Aplicar conceitos de machine learning para previsão de chuvas e identificação de áreas criticas expostas a eventos climaticos
- 📌 Análise de Dados
- 📌 Apresentações Graficas e Mapas

---

## 🧠 Fontes Históricas de Dados Climatológicos

Neste trabalho utilizamos duas fontes principais de dados, sendo

<a href="https://bdmep.inmet.gov.br/">Banco de Dados Meteorológicos do INMET </a>:  Cadastro de estações meteorológicas com localização geográfica e histórico de dados climatológicos desde o ano 2000.

<a href="https://www.cpc.ncep.noaa.gov/">NOAA Climate Prediction Center</a>: Monitoramento e medições mensais da temperatura do oceano Pacífico.
```bash
📂 Global Solution 1º Semestre 2026
│
├── 📂 Dados INMET
│   ├── 📂 DADOS CONSOLIDADOS BRUTOS (Informações de estações metereologicas do Brasil, dados desde 2000, aproximadamente 170 mil registros armazenados)
│   │   ├── 📂 tab: DADOS_CLIMA_GS_2026_S1 
│   ├── 📂 DADOS TRABALHADOS (limpeza de registros duplicados, valores nulos ou outliers)
│   |   ├── 📂 tab: HISTORICO_CHUVA
│   |   ├── 📂 tab: HISTORICO_TEMPERATURA
│   |   ├── 📂 tab: HISTORICO_UMIDADE
│   |   ├── 📂 tab: HISTORICO_VENTO
│   └── 📂 CADASTRO DE ESTAÇÕES METEREOLOGICAS (Informações de todas as estações metereologicas ativas, posição geografica, altitude e distancia para a faixa do Equador)
│   |   ├── 📂 tab: DF_CADASTRO_ESTACOES
├── 📂 Dados NOAA (Monitoramento e medições mensais da temperatura do oceano Pacífico)
│   ├── 📂 tab: DADOS_NOAA
```
## 🧠 Tabelas e Banco de Dados
---

Imagem abaixo demonstra a estrutura do banco de dados, neste projeto, utilizamos 6 tabelas
<p align="center">
<img width="318" height="266" alt="Image" src="https://github.com/user-attachments/assets/50838172-38b4-49d8-b5fb-3282a252fb33" /></a>
</p>

*DADOS_CLIMA_GS_206_S1:* Estrutura contendo dados climáticos brutos extraídos diretamente das bases do INMET. Serve como fonte primária para as análises de monitoramento.

<p align="center">
<img width="753" height="510" alt="Image" src="https://github.com/user-attachments/assets/6dd46d1a-4be1-40d5-b001-818982be1484" /></a>
</p>

*DF_CADASTRO_ESTACOES:* Catálogo estruturado de 597 estações meteorológicas de medição. Inclui metadados como posição geográfica, altitude e distância em relação à Linha do Equador.

<p align="center">
<img width="722" height="292" alt="Image" src="https://github.com/user-attachments/assets/fdf7b7a3-376b-4462-8c0a-487f97f38b3c" /></a>
</p>

<p align="center">
<img width="1295" height="555" alt="Image" src="https://github.com/user-attachments/assets/d7df3923-8161-48aa-be53-6944dc8a4525" /></a>
</p>

*DADOS_NOAA:* Consolidação das temperaturas da superfície do oceano Pacífico, utilizada para a identificação e classificação de períodos e ciclos climáticos (El Niño, La Niña e Neutro).

<p align="center">
<img width="769" height="263" alt="Image" src="https://github.com/user-attachments/assets/87ea4157-f3cf-4a95-b726-9c8b2bac5177" /></a>
</p>

*HISTORICO_CHUVA:* Série histórica de precipitação climática (em milímetros), com agregação mensal e estruturada pela coluna ANO_MES.

*HISTORICO_TEMPERATURA:* Série histórica de temperaturas, apresentada em médias mensais, categorizada e identificada pela coluna ANO_MES.

*HISTORICO_UMIDADE:* Série histórica de Umidade Relativa do Ar, apresentada em médias mensais e estruturada pela coluna ANO_MES.

*HISTORICO_VENTOS:* Série histórica de medições de vento, com visão de média mensal e estruturada pela coluna ANO_MES.

<p align="center">
<img width="254" height="428" alt="Image" src="https://github.com/user-attachments/assets/24ddeb23-cb5c-47f3-8906-9227ecda07e8" /></a>
</p>

```bash
```
## 🧠 Processamento de Informações
---

## 📋 Licença


https://conexaosafra.com/

https://www.bbc.com/portuguese/resources/idt-54f4e985-a7fb-48b2-8246-f3be0d699402

http://enos.cptec.inpe.br/

https://globorural.globo.com/Noticias/Tempo/noticia/2018/10/el-nino-e-la-nina-efeitos-no-clima-e-na-agricultura.html
