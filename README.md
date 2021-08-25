# Controle de robôs por tags

Esse projeto tinha o objetivo de fazer o controle da movimentação de um robô (4 rodas ou esteiras) através de Visão Computacional

https://drive.google.com/open?id=1o5wWD6clXiKC6qeON1uYP24FKBFMXq9i

como pode ser visto no vídeo, existem marcadores posicionados nos meus dedos e as informações de ângulo e tamanho da reta traçada pelo programa seriam os definidores 
da movimentação do robô (sendo ângulo para direcional e tamanho para velocidade)

![image](https://user-images.githubusercontent.com/56319681/130544921-cfd2c287-2680-4f1d-b995-66da18b0bca3.png)

Projeto não finalizado.

## Como Rodar o Projeto

 - Primeiro, instale as libs `cv2` e `numpy`
 
```
~$ pip3 install opencv-python

...

~$ pip3 instal numpy
```

- Segundo, rode o programa `trackbar.py`. Nele, você vai filtrar as cores que quer que seu programa reconheça. Ainda está manual, então anote os valores que
aparecerem na tela, tanto para o primeiro quanto para o segundo marcador.

- Terceiro, rode o programa `main.py`
