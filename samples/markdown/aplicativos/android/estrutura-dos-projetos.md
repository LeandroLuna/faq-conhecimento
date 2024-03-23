# Estrutura do projeto

Documentação abaixo:

## FiapOn
	
### Camada logica

    1. api - endpoints
	2. base - classes base (baseActivitity)...
	3. data - ?
	
### Camada telas
	
    1. login - loginActivity and fragments of login 
	2. main - mainActivity and internal fragments
	3. model - modelos do projeto, classe pojo
	4. player - ?
	5. service - ?
	6. ui - animacoes etc... delegacao de animacao
	7. util - classes para maior reutilizacao de codigo

## Uso do MVP nas activitys

	1. Contract - garante quais acoes a tela tem 
	2. View - usa a logica
	3. Presenter - mantem a logica das acoes

### Uso do MVP das activitys para os fragments
	
	Alguns fragments tem como atributo tem o presenter com o presenter da *Activity*, por exemplo o SignInPresenter (Presenter de um Fragment) tem o LoginPresenter que é o presenter da activity que o tem, no metodo login do SignInPresenter por exemplo, ele usa o login da presenter da activity

## Next

## Fiapp