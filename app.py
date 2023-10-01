import os
import pytesseract
import cv2
import re
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import scrolledtext
import shutil

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Define o diretório raiz do projeto na pasta "out"
diretorio_saida = os.path.join(os.getcwd(), 'out')
diretorio_trabalho = ''
pasta_selecionada = ''

# Função para extrair a data a partir do texto
def extrair_data(texto):
    # Usando uma expressão regular para encontrar datas no formato "X de Y de Z"
    padrao = r'(\d+) de (\w+)\. de (\d+)'
    correspondencias = re.search(padrao, texto)
    
    if correspondencias:
        dia, mes, ano = correspondencias.groups()
        # Mapeando nomes de meses para números (você pode expandir a lista de mapeamento conforme necessário)
        meses = {
            'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04', 'mai': '05', 'jun': '06',
            'jul': '07', 'ago': '08', 'set': '09', 'out': '10', 'nov': '11', 'dez': '12'
        }
        mes_numero = meses.get(mes[:3].lower())
        if mes_numero:
            return f"{ano}-{mes_numero}-{dia}"
    
    return None

# Função para converter todos os arquivos da pasta para PNG
def converter_para_png(caminho_pasta, text_widget):
    text_widget.insert(tk.END, f"Convertendo arquivos...\n")
    text_widget.update()
    for arquivo in os.listdir(caminho_pasta):
        if not arquivo.lower().endswith(('.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif')):  # Se não for um arquivo suportado
            continue  # Pule este arquivo

        caminho_arquivo = os.path.join(caminho_pasta, arquivo)

        try:
            imagem = cv2.imread(caminho_arquivo)

            if imagem is not None:
                novo_nome = os.path.splitext(arquivo)[0] + ".png"  # Nome do novo arquivo com extensão PNG
                caminho_novo_arquivo = os.path.join(caminho_pasta, novo_nome)
                cv2.imwrite(caminho_novo_arquivo, imagem)
                os.remove(caminho_arquivo)  # Remove o arquivo original
                print(f"Convertido: {arquivo} -> {novo_nome}")
            else:
                print(f"Erro ao ler imagem: {arquivo}")

        except Exception as e:
            print(f"Erro ao processar arquivo {arquivo}: {str(e)}")
    
    text_widget.insert(tk.END, f"Conversão finalizada! \n")
    text_widget.insert(tk.END, "_" * 50 + "\n")
    text_widget.update()

def recortar_roi(imagem, x, y, w, h):
    roi = imagem[y:y+h, x:x+w]
    return roi

def update_image(arquivo, data, caminho_arquivo, renomeados, caminho_pasta, text_widget):
    text_widget.insert(tk.END, f"Arquivo: {arquivo}\n")
    text_widget.insert(tk.END, f"Data extraída: {data}\n")
    text_widget.update()

    novo_nome = f"{data}.png"
    contador = 1
    while novo_nome in renomeados:
        novo_nome = f"{data} ({contador}).png"
        contador += 1
    
    renomeados.add(novo_nome)
    text_widget.insert(tk.END, f"Renomeado para: {novo_nome}\n")
    
    novo_nome = os.path.join(caminho_pasta, novo_nome)
    os.rename(caminho_arquivo, novo_nome)

def processar_pasta(caminho_pasta, text_widget, progresso):

    os.chdir(caminho_pasta)

    converter_para_png(caminho_pasta, text_widget)  # Converte todos os arquivos para PNG primeiro
    renomeados = set()  # Conjunto para rastrear nomes de arquivos já renomeados
    lista_arquivos = os.listdir(caminho_pasta)
    tamanho_do_laco = len(lista_arquivos)
    progresso['maximum'] = 100

    for indice, arquivo in enumerate(lista_arquivos):
        if arquivo.endswith(".png"):  # Agora todos os arquivos são PNG
            caminho_arquivo = os.path.join(caminho_pasta, arquivo)
            imagem = cv2.imread(caminho_arquivo)
            
            texto = pytesseract.image_to_string(imagem)
            data = extrair_data(texto)
            
            if data:
                update_image(arquivo, data, caminho_arquivo, renomeados, caminho_pasta, text_widget)
                
            else:
                text_widget.insert(tk.END, f"Data não encontrada: forçando análise... \n")
                # Criar imagem recortada no centro
                roi_centro = recortar_roi(imagem, 165, 780, 400, 100)
                texto = pytesseract.image_to_string(roi_centro)
                data = extrair_data(texto)

                if data:
                    update_image(arquivo, data, caminho_arquivo, renomeados, caminho_pasta, text_widget)
                else:
                    # Criar imagem recortada na parte superior
                    roi_superior = recortar_roi(imagem, 165, 270, 400, 100)
                    texto = pytesseract.image_to_string(roi_superior)
                    data = extrair_data(texto)

                    if data:
                        update_image(arquivo, data, caminho_arquivo, renomeados, caminho_pasta, text_widget)
                    else:
                        text_widget.insert(tk.END, f"Data não encontrada para arquivo [{arquivo}]\n")
            
            text_widget.insert(tk.END, "_" * 50 + "\n")
            text_widget.see(tk.END)
            text_widget.update()
            progresso['value'] = (indice + 1) / tamanho_do_laco * 100
    copy_results(text_widget)
    messagebox.showinfo("Processamento Concluído", "O processamento foi concluído com sucesso!")

def selecionar_pasta(text_widget):
    global pasta_selecionada
    global diretorio_trabalho
    global diretorio_saida
    delete_all_folders_in_directory(diretorio_saida)
    
    pasta_selecionada = filedialog.askdirectory(title="Selecione uma pasta")

    # Verifica se uma pasta foi selecionada
    if pasta_selecionada:
        # Obtém o nome da pasta selecionada
        nome_pasta = os.path.basename(pasta_selecionada)
        
        # Define o caminho completo da pasta de destino na pasta "out"
        pasta_destino = os.path.join(diretorio_saida, nome_pasta)
        diretorio_trabalho = pasta_destino

        try:
            text_widget.insert(tk.END, f"Copiando pasta. Aguarde. \n")
            text_widget.update()
            # Copia a pasta selecionada para a pasta de destino
            shutil.copytree(pasta_selecionada, pasta_destino)

            text_widget.insert(tk.END, f"A pasta selecionada está pronta!\n")
            text_widget.insert(tk.END, "_" * 50 + "\n")
            text_widget.insert(tk.END, f"INICIE O PRCESSAMENTO\n")
            text_widget.update()
            print("Pasta copiada para:", diretorio_trabalho)
        except Exception as e:
            messagebox.showerror("Erro ao copiar pasta", str(e))

def delete_all_folders_in_directory(directory):
    for root_folder, subfolders, files in os.walk(directory):
        for subfolder in subfolders:
            folder_to_delete = os.path.join(root_folder, subfolder)
            try:
                shutil.rmtree(folder_to_delete)
                print(f"Pasta apagada: {folder_to_delete}")
            except PermissionError:
                print(f"Erro ao apagar pasta: {folder_to_delete}. Aguardando e tentando novamente...")
                time.sleep(2)  # Espera por um curto período antes de tentar novamente
                try:
                    shutil.rmtree(folder_to_delete)
                    print(f"Pasta apagada na segunda tentativa: {folder_to_delete}")
                except Exception as e:
                    print(f"Erro ao apagar pasta na segunda tentativa: {folder_to_delete} - {str(e)}")

def copy_results(text_widget):
    global diretorio_trabalho
    global pasta_selecionada
    
    if not diretorio_trabalho or not pasta_selecionada:
        text_widget.insert(tk.END, "Erro: Pasta de trabalho ou pasta selecionada não definida.\n")
        return
    
    try:
        nome_pasta_selecionada = os.path.basename(pasta_selecionada)
        pasta_destino = os.path.join(os.path.dirname(pasta_selecionada), f"{nome_pasta_selecionada}-ordenada")
        
        text_widget.insert(tk.END, f"Salvando resultados em: {pasta_destino}\n")
        text_widget.update()
        text_widget.see(tk.END)
        
        # Copia a pasta de trabalho para a pasta de destino
        shutil.copytree(diretorio_trabalho, pasta_destino)
    
    except Exception as e:
        text_widget.insert(tk.END, f"Erro ao copiar resultados: {str(e)}\n")
        text_widget.update()
        text_widget.see(tk.END)
    
    # Agora, exclua a pasta de trabalho
    text_widget.insert(tk.END, f"Limpando arquivos temporários...\n")
    text_widget.update()
    text_widget.see(tk.END)
    delete_all_folders_in_directory(diretorio_saida)

def fechar_janela():
    root.destroy()
    exit()  # Destruir a janela principal (encerrar o programa)

# Função principal que inicia a interface gráfica e o processamento
def main():
    # Cria uma janela tkinter
    root = tk.Tk()
    root.title("Organizador de Prints")

    # Cria um frame para conter os widgets
    frame = ttk.Frame(root)
    frame.pack(padx=20, pady=20)

    # Adiciona um rótulo com o texto centralizado
    label = ttk.Label(frame, text="Organizador de Prints", font=("Helvetica", 16))
    label.grid(row=0, column=0, columnspan=2, pady=10)

    # Cria um widget de texto rolável para exibir mensagens
    text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=40, height=20)
    text_widget.grid(row=1, column=0, columnspan=2, pady=10)

    progress_bar = ttk.Progressbar(frame, length=300, mode='determinate')
    progress_bar.grid(row=2, column=0, pady=10)

    # Botão para selecionar o caminho da pasta
    global pasta_selecionada
    button_select_folder = ttk.Button(frame, text="Selecionar Pasta", command=selecionar_pasta)
    button_select_folder.grid(row=3, column=0, pady=10)

    # Botão para iniciar o processamento
    button_start = ttk.Button(frame, text="Iniciar Processamento", command=lambda: processar_pasta(pasta_selecionada, text_widget))
    button_start.grid(row=3, column=1, pady=10)
    
    root.protocol("WM_DELETE_WINDOW", fechar_janela)

    # Executa a janela tkinter
    root.mainloop()


class APP:
    def __init__(self, root):
        self.root = root
        self.root.title("OrganizaPrints")
        # Associa a função 'self.fechar_janela' ao evento de fechar a janela
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_janela)

        # Adicione widgets, como botões e rótulos, aqui

         # Cria um frame para conter os widgets
        frame = ttk.Frame(root)
        frame.pack(padx=20, pady=20)

        # Adiciona um rótulo com o texto centralizado
        label = ttk.Label(frame, text="Seja bem vindo ao OrganizaPrints!", font=("Helvetica", 16))
        label.grid(row=0, column=0, columnspan=2, pady=10)
        # Descrição
        label = ttk.Label(frame, text="Selecione uma pasta que contenha prints de histórico de localizações do google.", font=("Helvetica", 12))
        label.grid(row=1, column=0, columnspan=2, pady=10)

        # Cria um widget de texto rolável para exibir mensagens
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=70, height=7)
        text_widget.grid(row=2, column=0, columnspan=2, pady=10)
        
        progresso = ttk.Progressbar(frame, orient='horizontal', length=550, mode='determinate')
        progresso.grid(row=3, column=0, columnspan=2, pady=10)

        # Botão para selecionar o caminho da pasta
        global pasta_selecionada
        button_select_folder = ttk.Button(frame, text="Selecionar Pasta", command=lambda:selecionar_pasta(text_widget))
        button_select_folder.grid(row=4, column=0, pady=10)

        # Botão para iniciar o processamento
        button_start = ttk.Button(frame, text="Iniciar Processamento", command=lambda:processar_pasta(diretorio_trabalho, text_widget, progresso))
        button_start.grid(row=4, column=1, pady=10)

    def fechar_janela(self):
        self.root.destroy()  # Destruir a janela principal (encerrar o programa)

if __name__ == "__main__":
    # Cria uma janela tkinter
    root = tk.Tk()

    # Crie uma instância da classe MinhaAplicacao
    app = APP(root)

    # Inicie a interface gráfica
    root.mainloop()