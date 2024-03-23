# Processo para Reverter Merge Requests (MRs)

Caso haja a necessidade de fazer um revert em um Merge Request que já foi mergeado. Seguir o passo a passo abaixo:

!!! caution Obs
	Caso o MR seja barrado em produção, realizar esse processo tanto na branch de **dev** quanto na de **homolog**

1. Acessar a página no GitLab do Merge Request que será revertido e clique no botão "revert":
	![[revert-1.png]](./imgs/revert-1.png)

2. Ao abrir a tela de opção de reversão, deve-se a mesma branch de **DESTINO** na qual o MR foi feito e **DESMARCAR** a opção de criar um novo merge request.
	![[revert-2.png]](./imgs/revert-2.png)

3. O histórico ficara da seguinte forma:
	![[revert-3.png]](./imgs/revert-3.png)