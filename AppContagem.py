import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import Listbox
import sqlite3
from datetime import datetime
resumo_window = None
setor_id = None
 

# Função para criar o ambiente (banco de dados e tabelas)
def criar_banco():
    try:
        # Criar banco de dados 'inventario.db'
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()

        # Criar tabela 'contagem'
        cursor.execute('''CREATE TABLE IF NOT EXISTS contagem (
                          id INTEGER PRIMARY KEY,
                          nome TEXT,
                          data_inicio TEXT,
                          data_fim TEXT,
                          status TEXT
                      )''')

        # Criar tabela 'setores'
        cursor.execute('''CREATE TABLE IF NOT EXISTS setores (
                          id INTEGER PRIMARY KEY,
                          contagem_id INTEGER,
                          nome TEXT,
                          data_hora_inicio TEXT,
                          data_hora_fim TEXT,
                          total_codigos INTEGER
                      )''')

        # Criar tabela 'codigos_bipados'
        cursor.execute('''CREATE TABLE IF NOT EXISTS codigos_bipados (
                          id INTEGER PRIMARY KEY,
                          setor_id INTEGER,
                          codigo TEXT
                      )''')

        # Criar tabela 'encontrados'
        cursor.execute('''CREATE TABLE IF NOT EXISTS encontrados (
                          id INTEGER PRIMARY KEY,
                          codigo TEXT,
                          desc_produto TEXT,
                          cor_produto TEXT,
                          tamanho TEXT,
                          setor_id INTEGER
                      )''')

        # Criar tabela 'nao_encontrados'
        cursor.execute('''CREATE TABLE IF NOT EXISTS nao_encontrados (
                          id INTEGER PRIMARY KEY,
                          codigo TEXT,
                          setor_id INTEGER
                      )''')

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Erro ao criar o banco de dados: {str(e)}")

# Chame a função para criar o banco de dados e tabelas
criar_banco()


# Função para criar uma nova contagem
def criar_contagem():
    try:
        nome_contagem = titulo_contagem.get()  # Obtenha o nome da contagem do campo de entrada
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
        
        # Obter a data e hora atual
        data_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Inserir a nova contagem no banco de dados com status 'Em Andamento'
        cursor.execute("INSERT INTO contagem (nome, data_inicio, status) VALUES (?, ?, ?)", (nome_contagem, data_inicio, 'Em Andamento'))
        conn.commit()
        
        conn.close()
        
        titulo_contagem.set("")  # Limpar o campo de título
        
        # Chamar a função para mostrar a próxima tela
        mostrar_setor_criar()
    except Exception as e:
        print(f"Erro ao criar uma nova contagem: {str(e)}")

# Para criar uma nova contagem e mostrar a próxima tela, chame a função apropriada no seu código.
# Exemplo de uso:
# criar_contagem()



# Função para mostrar a tela de criação de setor
def mostrar_setor_criar():
    tela_inicial.pack_forget()
    nova_contagem_button.pack_forget()
    encerrar_aplicativo_button.pack_forget()
    criar_setor_frame.pack(fill=tk.BOTH, expand=True)
    nome_setor_entry.pack()
    novo_setor_button.pack()
    novo_setor_button.pack(pady=(10, 10), padx=10)
    ultimos_codigos_bipados.pack()
    excluir_codigo_button.pack()

# Função para criar um novo setor
def criar_setor():
    try:
        nome_setor = nome_setor_entry.get()

        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM contagem")
        contagem_id = cursor.fetchone()[0]
        data_hora_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("INSERT INTO setores (contagem_id, nome, data_hora_inicio, data_hora_fim, total_codigos) VALUES (?, ?, ?, ?, ?)",
                       (contagem_id, nome_setor, data_hora_inicio, None, 0))
        conn.commit()
        
        # Defina a variável setor_id após a criação do setor
        cursor.execute("SELECT MAX(id) FROM setores")
        setor_id = cursor.fetchone()[0]
        # Agora a variável setor_id está definida para uso em outras funções

        
        conn.close()

        nome_setor_entry.delete(0, 'end')  # Limpar o campo de nome do setor
        
        # Chamar a função para mostrar a próxima tela
        mostrar_tela_bipar()
    except Exception as e:
        print(f"Erro ao criar um novo setor: {str(e)}")



 
# Função para mostrar a tela de bipar códigos
def mostrar_tela_bipar():
    criar_setor_frame.pack_forget()
    bipar_codigo_frame.pack(fill=tk.BOTH, expand=True)
    codigo_barras_entry.pack()
    codigo_barras_entry.focus_set()
    bipar_button.pack()
    bipar_button.pack(pady=(10, 10), padx=20)
    adicionar_avulso.pack()
    adicionar_avulso.pack(pady=(10, 10), padx=10)
    finalizar_setor_button.pack()

    
    
    
    
    
 
 

 
    
    

import sqlite3

# Função para bipar um código de barras
def bipar_codigo():
    global setor_id
    try:
        # Limpar o resultado_text antes de exibir uma nova mensagem
        resultado_text.config(state=tk.NORMAL)  # Habilitar a edição do Text widget
        resultado_text.delete(1.0, tk.END)  # Deletar todo o conteúdo
        resultado_text.config(state=tk.DISABLED)  # Desabilitar a edição do Text widget
        
        codigo_barras = codigo_barras_entry.get()

        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
        
        # Obter o ID do setor ativo (o setor mais recente em andamento)
        cursor.execute("SELECT id FROM setores WHERE data_hora_fim IS NULL ORDER BY id DESC LIMIT 1")
        setor_id = cursor.fetchone()[0]

        # Conectar ao banco de dados 'codigobarras.db'
        conn_codigobarras = sqlite3.connect("codigobarras.db")
        cursor_codigobarras = conn_codigobarras.cursor()

        # Verificar se o código de barras existe na tabela 'produtos' do banco 'codigobarras.db'
        cursor_codigobarras.execute("SELECT * FROM produtos WHERE codebar = ?", (codigo_barras,))
        produto_encontrado = cursor_codigobarras.fetchone()

        # insere em codigos bipados
        cursor.execute("INSERT INTO codigos_bipados  (setor_id,codigo) VALUES (?, ?)",(setor_id, codigo_barras)) 
           
      

        if produto_encontrado:
            resultado_text.config(state=tk.NORMAL)  # Habilitar a edição do Text widget
            resultado_text.insert(tk.END, "Código encontrado:\n")
            resultado_text.insert(tk.END, f"Codebar: {produto_encontrado[1]}\n")
            resultado_text.insert(tk.END, f"Descrição do Produto: {produto_encontrado[3]}\n")
            resultado_text.insert(tk.END, f"Cor do Produto: {produto_encontrado[4]}\n")
            resultado_text.insert(tk.END, f"Tamanho: {produto_encontrado[5]}\n")
            resultado_text.config(state=tk.DISABLED)  # Desabilitar a edição do Text widget

            # Registrar o código encontrado na tabela 'encontrados'
            cursor.execute("INSERT INTO encontrados (codigo, desc_produto, cor_produto, tamanho, setor_id) VALUES (?, ?, ?, ?,?)",
                           (codigo_barras, produto_encontrado[3], produto_encontrado[4], produto_encontrado[5], setor_id))
        else:
            resultado_text.config(state=tk.NORMAL)  # Habilitar a edição do Text widget
            resultado_text.insert(tk.END, "Código não encontrado\n")
            resultado_text.config(state=tk.DISABLED)  # Desabilitar a edição do Text widget

            # Registrar o código não encontrado na tabela 'nao_encontrados'
            cursor.execute("INSERT INTO nao_encontrados (codigo, setor_id) VALUES (?,?)", (codigo_barras,setor_id))
        
        # Atualizar o total de códigos no setor
        cursor.execute("UPDATE setores SET total_codigos = total_codigos + 1 WHERE id = ?", (setor_id,))
        conn.commit()
        
        # Atualizar a lista
        carregar_ultimos_codigos()

        
        conn.close()
        conn_codigobarras.close()

        codigo_barras_entry.delete(0, 'end')  # Limpar o campo de código de barras
    except Exception as e:
        print(f"Erro ao bipar um código de barras: {str(e)}")
 

# Função para abrir a janela de adição de código avulso
def abrir_janela_adicao():
    global setor_id
    nova_janela = tk.Toplevel(root)
    nova_janela.title("Adicionar Código Avulso")

    # Rótulo e campo de entrada para código de barras avulso
    codigo_avulso_label = tk.Label(nova_janela, text="Código de Barras Avulso", font=("Arial", 16))
    codigo_avulso_label.pack(pady=20)
    codigo_avulso_entry = tk.Entry(nova_janela, font=("Arial", 14))
    codigo_avulso_entry.pack()

    # Rótulo e campo de entrada para quantidade
    quantidade_label = tk.Label(nova_janela, text="Quantidade", font=("Arial", 16))
    quantidade_label.pack()
    quantidade_entry = tk.Entry(nova_janela, font=("Arial", 14))
    quantidade_entry.pack()
 
    def adicionar_avulso():
        global setor_id
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
         # Obter o ID do setor ativo (o setor mais recente em andamento)
        cursor.execute("SELECT id FROM setores WHERE data_hora_fim IS NULL ORDER BY id DESC LIMIT 1")
        setor_id = cursor.fetchone()[0]
        
        codigo_avulso = codigo_avulso_entry.get()
        quantidade = quantidade_entry.get()

        if codigo_avulso and quantidade:
            try:
                quantidade = int(quantidade)
                if quantidade > 0:
                    for _ in range(quantidade):
                         
                        cursor.execute("INSERT INTO codigos_bipados (setor_id, codigo) VALUES (?, ?)", (setor_id, codigo_avulso))
                        conn.commit()
                    
                        # Atualizar o total de códigos no setor
                        cursor.execute("UPDATE setores SET total_codigos = total_codigos + 1 WHERE id = ?", (setor_id,))
                        conn.commit()
        
                    nova_janela.destroy()
                else:
                    messagebox.showerror("Erro", "A quantidade deve ser maior que zero.")
            except ValueError:
                messagebox.showerror("Erro", "A quantidade deve ser um número inteiro.")
        else:
            messagebox.showerror("Erro", "Preencha ambos os campos.")

    # Botão para adicionar o código avulso
    adicionar_avulso_button = tk.Button(nova_janela, text="Adicionar", command=adicionar_avulso)
    adicionar_avulso_button.pack(pady=(10, 10), padx=20)

# ...


# Função para finalizar um setor e limpar a tela
def finalizar_setor():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM setores")
    setor_id = cursor.fetchone()[0]
    data_hora_fim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("UPDATE setores SET data_hora_fim = ? WHERE id = ?", (data_hora_fim, setor_id))
    conn.commit()

    # Atualizar o total de códigos do setor após finalizar
    cursor.execute("SELECT COUNT(*) FROM codigos_bipados WHERE setor_id = ?", (setor_id,))
    total_codigos = cursor.fetchone()[0]
    cursor.execute("UPDATE setores SET total_codigos = ? WHERE id = ?", (total_codigos, setor_id))
    conn.commit()

    conn.close()

    limpar_tela_apos_finalizar()
    mostrar_setor_criar()  # Mostrar a tela de criação de setor novamente

# Função para limpar a tela após finalizar um setor
def limpar_tela_apos_finalizar():
    bipar_codigo_frame.pack_forget()
    codigo_barras_entry.delete(0, 'end')
    bipar_button.pack_forget()
    finalizar_setor_button.pack_forget()
    novo_setor_button.pack()
    adicionar_avulso.pack_forget()
    excluir_codigo_button.pack_forget()
    ultimos_codigos_bipados.pack_forget()
    

 
 


# Função para mostrar a tela de criação de novo setor
def mostrar_novo_setor():
    bipar_codigo_frame.pack_forget()
    novo_setor_button.pack()

 


# Função para mostrar o resumo da contagem
def mostrar_resumo_contagem():
    global resumo_window
 

    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contagem WHERE status = 'Concluída' ORDER BY id DESC LIMIT 1")
    contagem = cursor.fetchone()

    # Calcula o total de códigos bipados na contagem
    cursor.execute("SELECT SUM(total_codigos) FROM setores WHERE contagem_id = ?", (contagem[0],))
    total_contagem = cursor.fetchone()[0]

    # Calcula o total de códigos encontrados na contagem
    cursor.execute('''SELECT COUNT(*)  FROM encontrados

LEFT JOIN setores on encontrados.setor_id =  setores.id
left join contagem on contagem.id = setores.contagem_id  WHERE contagem_id = ?''', (contagem[0],))
    codigos_encontrados = cursor.fetchone()[0]

    # Calcula o total de códigos não encontrados na contagem
    cursor.execute('''SELECT COUNT(*) FROM nao_encontrados
    
LEFT JOIN setores on nao_encontrados.setor_id =  setores.id
left join contagem on contagem.id = setores.contagem_id  WHERE contagem_id = ?''', (contagem[0],))
    codigos_nao_encontrados = cursor.fetchone()[0]

    # Preparar o texto do resumo
    resumo_text = f"Nome da Contagem: {contagem[1]}\n"
    resumo_text += f"Data de Fim: {contagem[3]}\n"
    resumo_text += f"Qde Bipados: {total_contagem}\n"
    resumo_text += f"Encontrados: {codigos_encontrados}\n"
    resumo_text += f"Não Encontrados: {codigos_nao_encontrados}\n\n"

    # Obter quantidade de itens bipados por setores
    cursor.execute("SELECT nome, total_codigos FROM setores WHERE contagem_id = ?", (contagem[0],))
    setores = cursor.fetchall()

    for setor in setores:
        resumo_text += f"{setor[0]}"
        resumo_text += f": {setor[1]}\n"

    conn.close()

    # Criar uma nova janela para exibir o resumo
    resumo_window = tk.Tk()
    resumo_window.title("Resumo da Contagem")

    resumo_label = tk.Label(resumo_window, text=resumo_text, font=("Arial", 10), anchor="w")  # Defina o alinhamento para "w" (oeste)
    resumo_label.pack(padx=20, pady=20)
     
    def download_contagem():
        # Função para fazer o download da tabela de códigos_bipados da contagem em questão
        
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM contagem WHERE status = 'Concluída' ORDER BY id DESC LIMIT 1")
        contagem = cursor.fetchone()
    
        if contagem:
            contagem_id = contagem[0]
            
            cursor.execute('''SELECT codigo, contagem_id, setor_id, setores.nome  FROM codigos_bipados 
                              LEFT JOIN setores ON setores.id = codigos_bipados.setor_id
                              LEFT JOIN contagem ON contagem.id = setores.contagem_id
                              WHERE contagem_id = ?''', (contagem_id,))
            codigos = cursor.fetchall()
            conn.close()
    
            if codigos:
                # Configurar o texto do rótulo de mensagem
                mensagem_label.config(text="Download realizado com sucesso") 
                data_hora_atual = datetime.now().strftime("%Y%m%d%H%M%S")
                cabecalho = "codigobarras;contagem_id;setor_id;setor_nome\n"
                with open(f"contagem_{contagem_id}_codigos{data_hora_atual}.txt", "w") as file:
                    file.write(cabecalho)
                    for codigo in codigos:
                        file.write(f"{codigo[0]};{codigo[1]};{codigo[2]};{codigo[3]}\n")  # Remova o ponto e vírgula da escrita
                        root.after(6000, lambda: mensagem_label.config(text=""))

        else:
            print("Nenhuma contagem concluída encontrada.")

    # Rótulo para exibir a mensagem de download realizado com sucesso
    mensagem_label = tk.Label(resumo_window, text="", font=("Arial", 12), fg="green")
    mensagem_label.pack(pady=10)
    # Botão para download da contagem (desabilitado por padrão)
    download_button = tk.Button(resumo_window, text="Download Contagem", command=download_contagem)
    download_button.pack(side="right")
    download_button.pack(pady=(20, 20), padx=20)




    resumo_window.mainloop()

 
    


# Função para finalizar a contagem
def finalizar_contagem():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM contagem")
    contagem_id = cursor.fetchone()[0]
    data_hora_fim = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Atualizar o status para 'Concluída' no banco de dados
    cursor.execute("UPDATE contagem SET status = 'Concluída', data_fim = ? WHERE id = ?", (data_hora_fim, contagem_id))
    conn.commit()
    conn.close()

    mostrar_resumo_contagem()  # Após atualizar o status, mostra o resumo em uma nova janela




# Função para iniciar uma nova contagem
def iniciar_nova_contagem():
    criar_banco()
    criar_setor_frame.pack_forget()
    bipar_codigo_frame.pack_forget()
    mostrar_tela_inicial()

# Função para encerrar o aplicativo
def encerrar_aplicativo():
    root.destroy()


#################################################################################################
# Configuração da janela principal
root = tk.Tk()
root.title("Aplicativo de Contagem de Códigos de Barras")
root.geometry("400x700")


# Carregar a imagem
photo = tk.PhotoImage(file="topo_inventario.png")

# Criar um label para exibir a imagem no topo
imagem_label = tk.Label(root, image=photo)
imagem_label.pack(padx=0)

# Rótulo para exibir a mensagem de download realizado com sucesso
mensagem_label = tk.Label(root, text="", font=("Arial", 12), fg="green")
mensagem_label.pack(pady=10)

# Variáveis de controle
titulo_contagem = tk.StringVar()
nome_setor_entry = tk.StringVar()
codigo_barras_entry = tk.StringVar()

# Criar um frame para o rodapé
rodape_frame = tk.Frame(root)
rodape_frame.pack(side="bottom", fill="x")

# Botão para finalizar a contagem
finalizar_contagem_button = tk.Button(rodape_frame, text="Finalizar Contagem", command=finalizar_contagem)
finalizar_contagem_button.pack(side="right")
finalizar_contagem_button.pack(pady=(20, 20), padx=20)



resultado_text2 = tk.Text(root, height=5, width=40, bg='light gray')
resultado_text2.insert(tk.END, '''Contagem de Invenatário OFFLINE.\n
Problema ou dúvida, envie um\ne-mail para leandrotobita@gmail.com.
'''
                      )
resultado_text2.pack(pady=10)
resultado_text2.config(state=tk.DISABLED)  # Desabilitar a edição do Text widget



# Criação do Text widget para exibir o resultado com cor de fundo e margem superior
resultado_text = tk.Text(root, height=5, width=40, bg='light gray')
resultado_text.pack(pady=10)  # Adicione pady=10 para uma margem superior de 10 pixels
resultado_text.config(state=tk.DISABLED)  # Inicialmente, desabilitado para evitar edição


# Tela inicial
tela_inicial = tk.Frame(root)
titulo_label = tk.Label(tela_inicial, text="Nova Contagem", font=("Arial", 16))
titulo_label.pack(pady=20)
titulo_entry = tk.Entry(tela_inicial, textvariable=titulo_contagem, font=("Arial", 14))
titulo_entry.pack()
criar_contagem_button = tk.Button(tela_inicial, text="Criar Contagem", command=criar_contagem)
criar_contagem_button.pack()
criar_contagem_button.pack(pady=(10, 0))

# Tela de criação de setor
criar_setor_frame = tk.Frame(root)
nome_setor_label = tk.Label(criar_setor_frame, text="Nome do Setor", font=("Arial", 16))
nome_setor_label.pack(pady=20)
nome_setor_entry = tk.Entry(criar_setor_frame, textvariable=nome_setor_entry, font=("Arial", 14))
novo_setor_button = tk.Button(criar_setor_frame, text="Novo Setor", command=criar_setor)

# Tela de bipar códigos
bipar_codigo_frame = tk.Frame(root)
codigo_barras_label = tk.Label(bipar_codigo_frame, text="Código de Barras", font=("Arial", 16))
codigo_barras_label.pack(pady=20)
codigo_barras_entry = tk.Entry(bipar_codigo_frame, font=("Arial", 14))
codigo_barras_entry.pack()  # Não vincule textvariable a este campo
 

bipar_button = tk.Button(bipar_codigo_frame, text="Bipar Código", command=bipar_codigo)
finalizar_setor_button = tk.Button(bipar_codigo_frame, text="Finalizar Setor", command=finalizar_setor, bg="red", fg="white")
adicionar_avulso = tk.Button(bipar_codigo_frame, text="Adiconar código manualmente", command=abrir_janela_adicao)

# Crie a Listbox para exibir os últimos códigos
ultimos_codigos_bipados = Listbox(bipar_codigo_frame, height=5, width=35, selectbackground='blue')
ultimos_codigos_bipados.pack()


# Conecte-se ao banco de dados
conn = sqlite3.connect("inventario.db")
cursor = conn.cursor()

# ...

# Dicionário para mapear IDs a códigos na Listbox
codigo_id_map = {}

# Função para carregar os últimos 5 códigos do banco de dados
def carregar_ultimos_codigos():
    cursor.execute("SELECT MAX(id) FROM contagem")
    contagem_idx = cursor.fetchone()[0]
        
    # Substitua este SQL pela consulta apropriada no seu banco de dados
    cursor.execute('''SELECT codigos_bipados.id, codigos_bipados.codigo FROM codigos_bipados 
                LEFT JOIN setores on codigos_bipados.setor_id = setores.id
                WHERE contagem_id = ? 
                ORDER BY codigos_bipados.id DESC LIMIT 5''', (contagem_idx,))

    codigos = cursor.fetchall()
    
  
        

    # Limpe a lista antes de adicionar novos códigos
    ultimos_codigos_bipados.delete(0, tk.END)

    for codigo_id, codigo in codigos:
        ultimos_codigos_bipados.insert(tk.END, codigo)  # Adicione o código à Listbox
        codigo_id_map[ultimos_codigos_bipados.get(tk.END)] = codigo_id  # Mapeie o código ao ID


# Chame a função para carregar os últimos códigos ao inicializar a tela
carregar_ultimos_codigos()

# ...

# Botão para excluir o código selecionado
def excluir_codigo():
    selecao = ultimos_codigos_bipados.curselection()
    if selecao:
        codigo_selecionado = ultimos_codigos_bipados.get(selecao)
        codigo_id = codigo_id_map.get(codigo_selecionado)
        if codigo_id:
            # Exclua o código do banco de dados
            cursor.execute("DELETE FROM codigos_bipados WHERE id=?", (codigo_id,))
            conn.commit()
            
            # Exclua o código do banco de dados encontrados
            cursor.execute("DELETE FROM encontrados WHERE codigo=? and setor_id=?", (codigo_selecionado,setor_id))
            conn.commit()
            
             # Exclua o código do banco de dados encontrados
            cursor.execute("DELETE FROM nao_encontrados WHERE codigo=? and setor_id=?", (codigo_selecionado,setor_id))
            conn.commit()
            
            
            
            # Atualizar o total de códigos no setor
            cursor.execute("UPDATE setores SET total_codigos = total_codigos - 1 WHERE id = ?", (setor_id,))
            conn.commit()
            
            
            
            
            # Exclua o código da Listbox
            ultimos_codigos_bipados.delete(selecao)

# Botão para excluir o código selecionado
excluir_codigo_button = tk.Button(bipar_codigo_frame, text="Excluir Código", command=excluir_codigo)
excluir_codigo_button.pack()



# Adicionar evento Enter para o campo1 de entrada
codigo_barras_entry.bind('<Return>', lambda event=None: bipar_codigo())

# Para usar a tecla Enter para bipar o código, você pode pressionar Enter no campo de entrada.

# Botão para finalizar a contagem
finalizar_contagem_button = tk.Button(root, text="Finalizar Contagem", command=finalizar_contagem)

# Label para mostrar o resultado
resultado_label = tk.Label(root, text="", font=("Arial", 8))

# Botão para iniciar uma nova 1contagem
nova_contagem_button = tk.Button(root, text="Iniciar Nova Contagem", command=iniciar_nova_contagem)

# Botão para encerrar o aplicativo
encerrar_aplicativo_button = tk.Button(root, text="Encerrar Aplicativo", command=encerrar_aplicativo)

# Mostrar a tela inicial
tela_inicial.pack(fill=tk.BOTH, expand=True)

root.mainloop()
