from rpc.client import Client
import PySimpleGUI as sg
import platform

client_rpc = Client('127.0.0.1',8888)
def open_soma_window():
    # Definir o layout da janela de soma
    layout_soma = [
        [sg.Text('Número 1:'), sg.Input(key='num1')],
        [sg.Text('Número 2:'), sg.Input(key='num2')],
        [sg.Button('Somar'), sg.Button('Fechar')],
        [sg.Text('Resultado:'), sg.Input(key='resultado', disabled=True)]
    ]

    # Criar a janela de soma
    window_soma = sg.Window('Calculadora - Soma', layout_soma)

    # Loop de eventos para a janela de soma
    while True:
        event_soma, values_soma = window_soma.read()

        if event_soma == sg.WIN_CLOSED or event_soma == 'Fechar':
            break
        elif event_soma == 'Somar':
            try:
                # Obter os números dos inputs
                num1 = float(values_soma['num1'])
                num2 = float(values_soma['num2'])

                # Realizar a soma e atualizar o resultado
                resultado = client_rpc.sum((num1,num2))
                window_soma['resultado'].update(f'{resultado:.2f}')

            except ValueError:
                sg.popup_error('Por favor, insira números válidos.')

    # Fechar a janela de soma
    window_soma.close()
def open_sub_window():
    # Definir o layout da janela de soma
    layout_soma = [
        [sg.Text('Número 1:'), sg.Input(key='num1')],
        [sg.Text('Número 2:'), sg.Input(key='num2')],
        [sg.Button('Subtrair'), sg.Button('Fechar')],
        [sg.Text('Resultado:'), sg.Input(key='resultado', disabled=True)]
    ]

    # Criar a janela de soma
    window_soma = sg.Window('Calculadora - Subtrair', layout_soma)

    # Loop de eventos para a janela de soma
    while True:
        event_soma, values_soma = window_soma.read()

        if event_soma == sg.WIN_CLOSED or event_soma == 'Fechar':
            break
        elif event_soma == 'Subtrair':
            try:
                # Obter os números dos inputs
                num1 = float(values_soma['num1'])
                num2 = float(values_soma['num2'])

                # Realizar a soma e atualizar o resultado
                resultado = client_rpc.subtract((num1,num2))
                window_soma['resultado'].update(f'{resultado:.2f}')

            except ValueError:
                sg.popup_error('Por favor, insira números válidos.')

    # Fechar a janela de soma
    window_soma.close()
def open_mul_window():
    # Definir o layout da janela de soma
    layout_soma = [
        [sg.Text('Número 1:'), sg.Input(key='num1')],
        [sg.Text('Número 2:'), sg.Input(key='num2')],
        [sg.Button('Multiplicar'), sg.Button('Fechar')],
        [sg.Text('Resultado:'), sg.Input(key='resultado', disabled=True)]
    ]

    # Criar a janela de soma
    window_soma = sg.Window('Calculadora - MUltiplicação', layout_soma)

    # Loop de eventos para a janela de soma
    while True:
        event_soma, values_soma = window_soma.read()

        if event_soma == sg.WIN_CLOSED or event_soma == 'Fechar':
            break
        elif event_soma == 'Multiplicar':
            try:
                # Obter os números dos inputs
                num1 = float(values_soma['num1'])
                num2 = float(values_soma['num2'])

                # Realizar a soma e atualizar o resultado
                resultado = client_rpc.multiply((num1,num2))
                window_soma['resultado'].update(f'{resultado:.2f}')

            except ValueError:
                sg.popup_error('Por favor, insira números válidos.')

    # Fechar a janela de soma
    window_soma.close()
def open_div_window():
    # Definir o layout da janela de soma
    layout_soma = [
        [sg.Text('Número 1:'), sg.Input(key='num1')],
        [sg.Text('Número 2:'), sg.Input(key='num2')],
        [sg.Button('Dividir'), sg.Button('Fechar')],
        [sg.Text('Resultado:'), sg.Input(key='resultado', disabled=True)]
    ]

    # Criar a janela de soma
    window_soma = sg.Window('Calculadora - Dividir', layout_soma)

    # Loop de eventos para a janela de soma
    while True:
        event_soma, values_soma = window_soma.read()

        if event_soma == sg.WIN_CLOSED or event_soma == 'Fechar':
            break
        elif event_soma == 'Dividir':
            try:
                # Obter os números dos inputs
                num1 = float(values_soma['num1'])
                num2 = float(values_soma['num2'])

                # Realizar a soma e atualizar o resultado
                resultado = client_rpc.divide((num1,num2))
                window_soma['resultado'].update(f'{resultado}')

            except ValueError:
                sg.popup_error('Por favor, insira números válidos.')

    # Fechar a janela de soma
    window_soma.close()


def open_is_prime_window():
    # Definir o layout da janela de is_prime
    layout_is_prime = [
        [sg.Text('Número Inicial:'), sg.Input(key='inicio')],
        [sg.Text('Número Final:'), sg.Input(key='fim')],
        [sg.Text('Passo:'), sg.Input(key='passo')],
        [sg.Button('Verificar'), sg.Button('Fechar')],
        [sg.Text('Resultados:')],
        [sg.Multiline('', key='resultados', size=(30, 10), disabled=True)]
    ]

    # Criar a janela de is_prime
    window_is_prime = sg.Window('Verificar Números Primos', layout_is_prime)

    # Loop de eventos para a janela de is_prime
    while True:
        event_is_prime, values_is_prime = window_is_prime.read()

        if event_is_prime == sg.WIN_CLOSED or event_is_prime == 'Fechar':
            break
        elif event_is_prime == 'Verificar':
            try:
                # Obter os números dos inputs
                inicio = int(values_is_prime['inicio'])
                fim = int(values_is_prime['fim'])
                passo = int(values_is_prime['passo'])

                # Verificar os números primos no intervalo especificado
                prime_numbers = client_rpc.is_prime(inicio,fim,passo)
                print(prime_numbers) 
                resultados = resultados = [str(num) for num in prime_numbers]

                # Atualizar a lista de resultados
                window_is_prime['resultados'].update('\n'.join(resultados))

            except ValueError:
                sg.popup_error('Por favor, insira números inteiros válidos.')

    # Fechar a janela de is_prime
    window_is_prime.close()

def open_last_news_window():
    # Definir o layout da janela de last_news
    layout_last_news = [
        [sg.Text('Número de Notícias:'), sg.Input(key='num_noticias')],
        [sg.Button('Buscar')],
        [sg.Table(values=[], headings=['Título', 'Link'], auto_size_columns=False, display_row_numbers=True,vertical_scroll_only=False,justification='right', key='tabela',size=(400,20))],
        [sg.Button('Fechar')]
    ]

    # Criar a janela de last_news
    window_last_news = sg.Window('Últimas Notícias', layout_last_news,size=(500,500))

    # Loop de eventos para a janela de last_news
    while True:
        event_last_news, values_last_news = window_last_news.read()

        if event_last_news == sg.WIN_CLOSED or event_last_news == 'Fechar':
            break
        elif event_last_news == 'Buscar':
            try:
                # Obter o número de notícias
                num_noticias = int(values_last_news['num_noticias'])

                # Obter as notícias usando a função fictícia
                noticias = client_rpc.last_news_ifbarbacena(num_noticias)

                # Atualizar a tabela com os resultados
                window_last_news['tabela'].update(values=noticias)

            except ValueError:
                sg.popup_error('Por favor, insira um número válido de notícias.')

    # Fechar a janela de last_news
    window_last_news.close()

def open_validar_cpf_window():
    # Definir o layout da janela de validar_cpf
    layout_validar_cpf = [
        [sg.Text('CPF:'), sg.Input(key='cpf')],
        [sg.Button('Validar')],
        [sg.Text('Resultado:'), sg.Input(key='resultado', disabled=True)]
    ]

    # Criar a janela de validar_cpf
    window_validar_cpf = sg.Window('Validar CPF', layout_validar_cpf)

    # Loop de eventos para a janela de validar_cpf
    while True:
        event_validar_cpf, values_validar_cpf = window_validar_cpf.read()

        if event_validar_cpf == sg.WIN_CLOSED:
            break
        elif event_validar_cpf == 'Validar':
            # Obter o CPF do input
            cpf = values_validar_cpf['cpf']

            # Validar o CPF usando a função fictícia
            resultado = 'Válido' if client_rpc.validate_cpf(cpf) else 'Inválido'

            # Atualizar o resultado na janela
            window_validar_cpf['resultado'].update(resultado)

    # Fechar a janela de validar_cpf
    window_validar_cpf.close()


# Verificar se o sistema operacional suporta GUI
if platform.system() not in ('Windows', 'Darwin', 'Linux'):
    sg.popup_error("Este script requer um ambiente gráfico.")
    exit()

def open_operation_window(operation):
    sg.popup(f'Você clicou no botão {operation}')

# Definir o layout da janela principal
layout = [
    [sg.Button('Soma', key='soma')],
    [sg.Button('Subtração', key='subtracao')],
    [sg.Button('Divisão', key='divisao')],
    [sg.Button('Multiplicação', key='multiplicacao')],
    [sg.Button('Is_prime', key='is_prime')],
    [sg.Button('Ultimas Noticias', key='ultimas_noticias')],
    [sg.Button('Validar CPF', key='validar_cpf')],
    [sg.Button('Sair')]
]

# Criar a janela principal
window = sg.Window('Calculadora e Outras Funções', layout)

# Loop de eventos
while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Sair'):
        break
    elif event == 'soma':
        open_soma_window()
    elif event == 'subtracao':
        open_sub_window()
    elif event == 'divisao':
        open_div_window()
    elif event == 'multiplicacao':
        open_mul_window()
    elif event == 'is_prime':
        open_is_prime_window()
    elif event == 'ultimas_noticias':
        open_last_news_window()
    elif event == 'validar_cpf':
        open_validar_cpf_window()


# Fechar a janela principal
window.close()