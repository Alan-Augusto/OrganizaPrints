# OrganizaPrints

## Princípios

O OrganizaPrints é uma ferramenta desenvolvida para organizar sequências de prints de histórico de localizações do Google em ordem cronológica.
Quando a quantidade de imagens se torna grande, a tarefa de organizar manualmente esses prints pode se tornar árdua e demorada.
A ideia principal por trás deste projeto é automatizar esse processo, permitindo que o sistema analise o conteúdo de cada imagem, extraia a data relevante e renomeie a foto com base nessa data.

## Download

Basta selecionar acessar o link <a href="">clicando aqui.</a>

## Funcionamento

O OrganizaPrints opera de acordo com os seguintes passos:

1. **Seleção da Pasta**: O usuário seleciona uma pasta que contém os prints de histórico de localizações do Google. Isso é feito através da interface gráfica fornecida pelo OrganizaPrints.

2. **Conversão para PNG**: Antes de processar as imagens, o sistema verifica e converte todos os arquivos de imagem na pasta selecionada para o formato PNG. Isso garante que todas as imagens estejam em um formato uniforme para facilitar a análise.

3. **Análise do Conteúdo**: O OrganizaPrints utiliza a biblioteca Tesseract OCR para extrair o texto das imagens. Ele busca por datas nos prints no formato "X de Y de Z".

4. **Renomeação das Imagens**: Quando uma data é encontrada em um print, o OrganizaPrints renomeia o arquivo da imagem com a data encontrada, seguindo o formato "AAAA-MM-DD.png". Caso uma data não seja encontrada na imagem, o sistema tenta recortar áreas específicas da imagem e realizar uma nova análise para identificar a data.

5. **Feedback ao Usuário**: Durante o processo de renomeação, o OrganizaPrints fornece feedback ao usuário na interface gráfica, exibindo informações sobre cada imagem processada. Isso ajuda o usuário a acompanhar o progresso do processo.

6. **Conclusão do Processamento**: Após processar todas as imagens na pasta selecionada, o OrganizaPrints exibe uma mensagem informando que o processamento foi concluído com sucesso.
