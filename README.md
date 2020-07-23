# Function que registra os detalhes de logs do OCI Cloud via Events

Esta função em Python registra os eventos da Oracle Cloud em diversos buckets no próprio compartimento

## Requisitos
Antes de iniciar é necessário o seguinte:<br>
a. Configurar o Dynamic Group<br>
```
ALL {resource.type = 'fnfunc', resource.compartment.id = 'ocid1.compartment.oc1..aaaaaxxxxx'}
```

b. Criar o policy para o Dynamic Group
```
Allow dynamic-group exemplo to manage all-resources IN TENANCY
```

c. Configurar o ambiente local com o OCI CLI, Docker e Fn Function<br>
https://docs.docker.com/engine/install/ubuntu/<br>
https://docs.cloud.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm<br>
https://docs.cloud.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsinstallfncli.htm

c1. Configurar no ambiente local o contexto: nele será especificado o provider (Oracle), a api_url, o registry e o compartmentID.<br>
https://docs.cloud.oracle.com/en-us/iaas/Content/Functions/Tasks/functionscreatefncontext.htm

```
fn create context <context_name> --provider oracle
fn use context <context_name>
fn update context oracle.compartment-id <ocid>
fn update context api-url https://functions.<region>.oraclecloud.com
fn update context registry region/tenancy_name/repository_name
```

d. Criar Aplicação no Oracle Cloud
Executar do passo 1 ao 7 de "Criar Aplicação" <br>
https://docs.cloud.oracle.com/en-us/iaas/Content/Functions/Tasks/functionscreatingapps.htm
<br>

<table>
    <tbody>
        <tr>
        <th><img align="left" width="600" src="https://objectstorage.us-ashburn-1.oraclecloud.com/n/idsvh8rxij5e/b/imagens_git/o/appCaptura%20de%20tela%20de%202020-07-22%2019-23-06.png"/></th>
        </tr>
    </tbody>
</table>

## Estrutura do Projeto<br>
O projeto contempla 3 arquivos:<br><br>

func.py - função que será executada para obter dados ao log. Para execução altere somente o CompartmentID da linha 8<br>

```python
    signer = oci.auth.signers.get_resource_principals_signer()
    resp = json.dumps({
        "UTC": "{0}".format(ts),
        "Event Type": "{0}".format(event_type), 
        "body": "{0}".format(body), 
        "URL context": ctx.RequestURL(), 
        "Header context": ctx.Headers()},
        indent = 4)
    save_log(signer, resp, event_type)
```

requirements.txt - dependências do projeto<br>
func.yaml - configurações de execução e alocação de recursos<br>

## Deploy da Função para Oracle Functions
```
fn -v deploy --app <app-name>
```
<br>

Após o deploy, ao acessar a aplicação criada, poderemos verificar a função:<br>

<table>
    <tbody>
        <tr>
        <th><img width="600" align="left" src="https://objectstorage.us-ashburn-1.oraclecloud.com/n/idsvh8rxij5e/b/imagens_git/o/funcaoCaptura%20de%20tela%20de%202020-07-22%2020-15-22.png"/></th>
        </tr>
    </tbody>
</table>

<br>

## Invocar remotamente a Função do Oracle Functions
```
fn invoke <app-name> <function_name>
```
<table>
    <tbody>
        <tr>
        <th><img width="600" align="left" src="https://objectstorage.us-ashburn-1.oraclecloud.com/n/idsvh8rxij5e/b/imagens_git/o/localCaptura%20de%20tela%20de%202020-07-22%2020-26-27.png"></th>
        </tr>
    </tbody>
</table>
<br>

## Configurar o Oracle Events para invocar a função serverless
<br>

1. Acesse a console do Oracle Cloud
2. Menu lateral esquerdo encontre "Application Integration"
3. Clique em "Event Service"
4. Clique em "Create Rule"
5. Não configure nada em "Rule Condition"  
6. Configure "Action" para executar a função publicada a aplicação


<table>
    <tbody>
        <tr>
        <th><img width="600" align="left" src="https://objectstorage.us-ashburn-1.oraclecloud.com/n/idsvh8rxij5e/b/imagens_git/o/ruleCaptura%20de%20tela%20de%202020-07-22%2020-41-54.png"></th>
        </tr>
    </tbody>
</table>
