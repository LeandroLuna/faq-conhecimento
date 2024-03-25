# Conversão de imagens para WebP

<div style="height: 350px; overflow-x:scroll;">
    <img src="../conversao-imagens-para-webp.svg" style="max-width: initial;">
</div>

## Links
**Explicação sobre o WebP** [https://developers.google.com/speed/webp?hl=pt-br](https://developers.google.com/speed/webp?hl=pt-br)

**Links com os compiladores WebP** [https://developers.google.com/speed/webp/docs/precompiled?hl=pt-br](https://developers.google.com/speed/webp/docs/precompiled?hl=pt-br)

**Comandos do cwebp** [https://developers.google.com/speed/webp/docs/cwebp?hl=pt-br](https://developers.google.com/speed/webp/docs/cwebp?hl=pt-br)

## Principais comandos

```shell
# Comando básico
cwebp input_file -o output_file.webp

# Comando com ajuste de qualidade (imagem lossy)
cwebp -q 90 -o output_file.webp

# Comando para gerar imagem lossless
cwebp input_file -lossless -o output_file.webp
```

O comando básico tem como padrão o valor de qualidade 75. Se após a conversão a qualidade da imagem não estiver adequada, pode usar o segundo comando, alterando o valor do -q para o valor apropriado, sendo 100 o valor máximo.


Se, mesmo assim, a qualidade da imagem não estiver adequada, utilize o terceiro comando, que irá manter a qualidade original da imagem. 

Pode também adicionar alguma opção presente no link `Comandos do cwebp`, caso necessite de um ajuste mais fino na imagem.

## Aplicando a imagem WebP no HTML/CSS

Agora que temos a imagem original e a imagem .webp, vamos usá-la nos projetos. 

No HTML usaremos a tag [picture](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture). Essa tag usa outras duas tags: a `source`, que colocaremos o caminho da imagem .webp, e a `img`, que servirá como uma alternativa, caso a imagem .webp não carregue (por exemplo, caso o navegador não suporte a extensão .webp).

Segue um exemplo de aplicação da tag picture:

```html
<picture>
    <source srcset="imagem.webp" type="image/webp">
    <img src="imagem.png" alt="">
</picture>
```
No caso do CSS (quando a imagem está setada como um plano de fundo, por exemplo), podemos usar o [@supports](https://developer.mozilla.org/en-US/docs/Web/CSS/@supports).

```css
background-image: url("imagem.png");

@supports (background-image: url("imagem.webp")) {
    background-image: url("imagem.webp");
}
```

Outro método é verificar se, ao começar a carregar a página, o navegador tem suporte ao webp, e colocar uma classe no `html` ou no `body`, indicando o resultado (por exemplo, `webp` ou `no-webp`). E no arquivo css (ou scss), adicionar a classe gerada junto com a classe que tem o background-image, desse jeito:

```scss
body.webp {
    .imagem-de-fundo {
        background-image: url("imagem.webp");
    }
}
  
body.no-webp {
    .imagem-de-fundo {
        background-image: url("imagem.png");
    }
} 
```

## Quem conhece esse processo
- Gustavo Matias Cotta <gustavo.cotta@fiap.com.br> 
( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=gustavo.cotta@fiap.com.br) )
- João Henrique Damazio <joao.damazio@fiap.com.br> 
( [Chat do Teams](https://teams.microsoft.com/l/chat/0/?users=joao.damazio@fiap.com.br) )
