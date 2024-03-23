# Geração de Contratos

## Realizando Requisição Postman

Para gerar **qualquer tipo de contrato** em PDF que utilize os conteúdos, 
cabeçalhos e rodapés do 
[modelos-contratos](https://gitlab.fiap.com.br/html/modelos-contratos), 
basta realizar a seguinte requisição no 
[Postman](https://www.postman.com/downloads/):

- Verbo HTTP: **POST**;
- Rota: https://apis.fiap.com.br/contrato/v1/Gerar/GerarPdf?sistema=<NOME_SISTEMA>&rm=<RM_ALUNO>
- Conteúdo da requisição (**Body** > **Raw** > **JSON**):

```json
{
    "Header": {
        "Modelo": "Modulo"
    },
    "Conteudo": {
        "Modelo": "ModuloIntegral-2023",
        "Dados": {
            "NomeFantasia": "Colégio Módulo",
            "RazaoSocial": "MD Educacional LTDA",
            "CNPJ": "11.316.763/0001-62",
            "Endereco": "Rua Tito, 1.175, Vila Romana, São Paulo ? SP",
            "CEP": "05051-001",
            "Curso": "Ensino Médio Regular",
            "Serie": 1,
            "ValorAnuidadeCheio": "R$28.925,00",
            "ValorAnuidadeCheioExtenso": "vinte e oito mil, novecentos e vinte e cinco reais",
            "ValorCheio": "R$2.225,00",
            "ValorCheioExtenso": "dois mil, duzentos e vinte e cinco reais",
            "ValorAnuidadeIntegral": "",
            "ValorAnuidadeIntegralExtenso": "",
            "ValorIntegral": "",
            "ValorIntegralExtenso": "",
            "ValorIntegralDesconto": "",
            "ValorIntegralDescontoExtenso": "",
            "ValorDesconto": "R$2.117,00",
            "ValorDescontoExtenso": "dois mil, cento e dezessete reais",
            "SufixoLogo": "",
            "Telefone": "11 3670.7070",
            "Site": "www.colegiomodulo.com.br",
            "NomeLegal": "FRANCISCO ESTEVES",
            "CelularLegal": "11 981700053",
            "TelefoneResidencialLegal": "",
            "TelefoneComercialLegal": "11 38726949",
            "DataNascimentoLegal": "15/04/1981",
            "CPFLegal": "28222561871",
            "RGLegal": "19647785-2",
            "EstadoCivilLegal": "Casado",
            "LogradouroLegal": ", 298 Casa 2",
            "NumeroLegal": "",
            "CepLegal": "00000000",
            "CidadeLegal": "",
            "BairroLegal": "",
            "EstadoLegal": "SP",
            "EmailLegal": "francisco.esteves@gmail.com",
            "NomeFinanceiro": "FRANCISCO ESTEVES",
            "CelularFinanceiro": "11 981700053",
            "TelefoneResidencialFinanceiro": "11 36754021",
            "TelefoneComercialFinanceiro": "11 38726949",
            "DataNascimentoFinanceiro": "15/04/1981",
            "CPFFinanceiro": "28222561871",
            "RGFinanceiro": "19647785-2",
            "EstadoCivilFinanceiro": "Casado",
            "LogradouroFinanceiro": ", 298 Casa 2",
            "NumeroFinanceiro": "",
            "CepFinanceiro": "00000000",
            "BairroFinanceiro": "",
            "CidadeFinanceiro": "",
            "EstadoFinanceiro": "SP",
            "EmailFinanceiro": "francisco.esteves@gmail.com",
            "Nome": "Murilo Otávio Teodoro Esteves",
            "RM": "24015",
            "Periodo": "Manhã",
            "DataAtual": "24 de Março de 2023",
            "Ano": "2023",
            "PeriodoIntegralExtenso": "Matutino",
            "PeriodoRegularExtenso": "Vespertino",
            "NomeSolidario": "",
            "CelularSolidario": "",
            "TelefoneResidencialSolidario": "",
            "TelefoneComercialSolidario": "",
            "DataNascimentoSolidario": "",
            "CPFSolidario": "",
            "RGSolidario": "",
            "EstadoCivilSolidario": "",
            "LogradouroSolidario": "",
            "NumeroSolidario": "",
            "CepSolidario": "00000000",
            "BairroSolidario": "",
            "CidadeSolidario": "",
            "EstadoSolidario": "SP",
            "EmailSolidario": "",
            "Sigla": "EMR",
            "ExibeMaterialDidatico": "true",
            "AutorizacaoImagem": "true"
        }
    },
    "Footer": {
        "Modelo": "Modulo"
    }
}
```

## Acessando Contrato PDF

Caso tudo funcione corretamente, será retornado um objeto JSON neste formato:

```json
{
    "NomeContrato": "/updown/Contratos/<CAMINHO_CONTRATO_PDF>"
}
```

O url completo para acesso do contrato ficará:

```
https://intranet.fiap.com.br/updown/Contratos/<CAMINHO_CONTRATO_PDF>
```