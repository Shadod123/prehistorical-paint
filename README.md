## Instruções de uso:

Para utilizar os algoritmos de rasterização como DDA e Bresenham, certifique-se antes de que o modo Desenhar se encontra selecionado. 
Após isso, basta clicar em dois lugares da tela, de forma a definir dois pontos, e escolher um dos algoritmos citados clicando no botão correspondente.

Se o intuito é desenhar um polígono em vez de uma reta ou uma circunferência, basta ir colocando pontos no canvas e clicar no botão "Conectar Todos os Objetos". 
Tal funcionalidade desenhará um polígono regular criando linhas entre os pontos de A a Z.

Por fim, caso deseje utilizar a função de recorte, é necessário alterar o modo para "Selecionar Região". Feito isso, cada par de pontos colocados na tela através de 
cliques no mouse produzirá um retângulo que delimita a região de corte. Selecionando um dos algoritmos (Cohen-Sutherland ou Liang-Barsky), o recorte é feito e o canvas 
é atualizado para refletir tal mudança.

**OBS: para aplicar qualquer tipo de transformação em um objeto desenhado no canvas, utilize a linha de botões adequada, visto que tentar rotacionar um polígono com 
o botão de "Rotacionar" de retas não produzirá o resultado esperado.**