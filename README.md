# OrganizaPrints

## Visão Geral

No mundo atual, o armazenamento de históricos de localização pelo Google tornou-se uma prática comum. Embora inicialmente possa parecer invasivo, essa informação pode ser uma valiosa ferramenta para advogados na obtenção de provas. No entanto, a tarefa de organizar e ordenar os prints enviados pelo cliente pode ser desafiadora e demorada. É nesse contexto que surge o **OrganizaPrints**, uma aplicação desenvolvida para auxiliar os advogados na ordenação cronológica de prints do Google.

O **OrganizaPrints** é uma ferramenta projetada para automatizar o processo de organização de sequências de prints de histórico de localizações do Google, tornando-o mais eficiente e preciso.

## Download

Para baixar o **OrganizaPrints**, siga um dos métodos abaixo:

- **Download Direto**: Você pode baixar a última versão do OrganizaPrints clicando [aqui](https://docs.google.com/uc?export=download&id=1WECUwH45NeZpmnfBNIXOKhW9GS5z5P65).

- **Download a partir do Repositório**:
  - Acesse a pasta "dist" do repositório.
  - Faça o download do arquivo OrganizaPrints.zip.
 
Para utilizar, basta extrair a pasta e colocá-la em seu diretório de interesse.

## Como Funciona

O OrganizaPrints opera em alguns passos simples para facilitar a organização dos prints:

1. **Seleção da Pasta**: O usuário seleciona a pasta que contém os prints de histórico de localizações do Google por meio da interface gráfica fornecida pelo OrganizaPrints.

2. **Conversão para PNG**: Antes de processar as imagens, o sistema verifica e converte todos os arquivos de imagem na pasta selecionada para o formato PNG, garantindo uniformidade.

3. **Análise do Conteúdo**: Utilizando a biblioteca Tesseract OCR, o OrganizaPrints extrai o texto das imagens, buscando datas no formato "X de Y de Z".

4. **Renomeação das Imagens**: Quando uma data é encontrada em um print, o OrganizaPrints renomeia o arquivo da imagem com a data no formato "AAAA-MM-DD.png". Se uma data não for encontrada, o sistema tenta recortar áreas específicas da imagem para uma nova análise.

5. **Feedback ao Usuário**: Durante o processo de renomeação, o OrganizaPrints fornece feedback na interface gráfica, exibindo informações sobre cada imagem processada.

6. **Conclusão do Processamento**: Após processar todas as imagens na pasta selecionada, o OrganizaPrints exibe uma mensagem de conclusão bem-sucedida.

7. **Diretório de Saída**: Após o processamento, uma cópia da pasta original é criada ao lado da pasta selecionada, com o sufixo "-reordenada".

## Dados Importantes

- A taxa de acurácia das análises varia em torno de 94%. Esse valor representa o pior caso observado nos testes.
- A acurácia pode variar dependendo da imagem e da proporção do print.
- É aconselhável sempre verificar os resultados e fazer ajustes manuais nas imagens não renomeadas.
- Imagens com datas semelhantes recebem sufixos diferentes, por exemplo:
  - 2023-12-25
  - 2023-12-25(2)
  - 2023-12-25(3)
- A formatação da data é invertida em relação ao padrão brasileiro para que a ordenação seja feita de forma alfanumérica.

## Contato

Se você tiver dúvidas, sugestões ou quiser relatar problemas, não hesite em entrar em contato:

- **Alan Augusto**
- Email: augustoalan56@gmail.com
- Telefone: (31) 9 9997-8009
