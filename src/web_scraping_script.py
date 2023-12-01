# Exemplo de uso
if __name__ == "__main__":
    caminho_driver = 'caminho/para/seu/chromedriver.exe'
    automacao = AutomacaoSelenium(caminho_driver)
    
    try:
        automacao.abrir_pagina('https://www.exemplo.com')
        
        # Aguarde até que o elemento com ID 'elemento_id' esteja presente
        automacao.esperar_elemento_aparecer(10, 'elemento_id')

        # Encontre o elemento pelo ID
        meu_elemento = automacao.encontrar_elemento_por_id('elemento_id')

        # Clique no elemento
        automacao.clicar_elemento(meu_elemento)

        # Preencha um campo de texto
        automacao.preencher_campo(meu_elemento, 'Texto a ser inserido')

    finally:
        automacao.fechar_navegador()
