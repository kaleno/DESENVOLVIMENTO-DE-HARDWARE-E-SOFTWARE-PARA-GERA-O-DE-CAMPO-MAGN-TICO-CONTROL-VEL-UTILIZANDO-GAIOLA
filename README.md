# DESENVOLVIMENTO DE HARDWARE E SOFTWARE PARA GERAÇÃO DE CAMPO MAGNÉTICO CONTROLÁVEL

Este repositório contém o trabalho de desenvolvimento de hardware e software realizado no âmbito do Laboratório de Controle e Simulação de Sistemas Aeroespaciais (LODESTAR) da Universidade de Brasília (UnB). O objetivo principal é criar uma plataforma com interface gráfica para a geração de campo magnético controlável, direcionada para aplicações no simulador de pequenos satélites do LODESTAR.

## Visão Geral

O sistema atual do laboratório inclui uma gaiola de Helmholtz com dois pares de bobinas por eixo, uma estação de trabalho e fontes de tensão controláveis. Este projeto propõe atualizações e o desenvolvimento de novas funcionalidades para a plataforma existente.

Algumas das aplicações planejadas são:

- Reprodução do campo magnético em malha fechada utilizando o modelo International Geomagnetic Reference Field (IGRF) em conjunto com o propagador de órbita Simplified General Perturbations (SGP4).
- Reprodução dos vetores de campo magnético coletados pelos sensores do satélite AlfaCrux, recentemente lançado.
- Realização de testes preliminares para validar o novo sistema no contexto dos projetos em andamento no LODESTAR.

## Estrutura do Repositório

O repositório está organizado da seguinte forma:

- `Firmware_Circuito_Inversor/`: Contém os arquivos relacionados ao firmware do circuito inversor.
- `Outros/`: Diretório para outros arquivos relevantes.
- `PonteH/`: Contém os arquivos relacionados à ponte H.
- `PonteH2.0/`: Contém os arquivos relacionados à versão 2.0 da ponte H.
- `Software_Gaiola/`: Contém os arquivos relacionados ao software da gaiola de Helmholtz.
- `Manual_Gaiola_de_Helmholtz_(1).pdf`: Documento PDF contendo o manual da gaiola de Helmholtz.
- `README.md`: Este arquivo README com informações sobre o projeto.
- `TCC_ThiagoHenriqueFerreiradaSilva_biblioteca.pdf`: Documento PDF contendo o TCC (Trabalho de Conclusão de Curso) intitulado "DESENVOLVIMENTO DE HARDWARE E SOFTWARE PARA GERAÇÃO DE CAMPO MAGNÉTICO CONTROLÁVEL".

Certifique-se de ajustar os nomes dos diretórios e arquivos de acordo com a estrutura do seu repositório.

## Pré-requisitos e Instalação

1. Certifique-se de ter os seguintes componentes presentes no arquivo requirements.bat

2. Clone este repositório em sua máquina local usando o seguinte comando:

**git clone https://github.com/seu-usuario/nome-do-repositorio.git**

3. Navegue até o diretório clonado.

4. Siga as instruções específicas contidas em `Manual_Gaiola_de_Helmholtz_(1).pdf` para configurar e instalar as respectivas partes do sistema.

## Utilização

1. Certifique-se de que o hardware está corretamente configurado e conectado à sua estação de trabalho.

2. Inicie o software e abra a interface gráfica do sistema.

3. Utilize as funcionalidades disponíveis para gerar o campo magnético controlável de acordo com suas necessidades.

4. Consulte a documentação disponível em `docs/` para obter informações adicionais sobre a utilização do sistema.

## Contribuição

Se você deseja contribuir para este projeto, sinta-se à vontade para enviar um pull request com suas melhorias. Toda contribuição é bem-vinda!

## Licença

Este projeto é licenciado sob a MIT. Consulte o arquivo LICENSE para obter mais informações.

## Contato

Para mais informações sobre este projeto, entre em contato conosco:

- Nome: Thiago Henrique Ferreira da Silva
- E-mail: thiago.henriquef@hotmail.com


