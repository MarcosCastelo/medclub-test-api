# **API Teste MedClub**

#  Configuração
Para testar a API é necessário a instalação do `docker` e do `docker-compose` para instalar esses recursos acesse: https://docs.docker.com/compose/install/

### Criando arquivo .env
Copie renomeei ou copie o arquivo .env.example para .env

### Execução do projeto
Para executar o projeto basta executar o comando `docker-compose up --build`

- Criando superuser: `docker-compose run web poetry run python manage.py createsuperuser
`

### Acessando o Swagger
A rota para o swagger é http://localhost:8000/api/schema/swagger-ui/

Utilize a rota `/auth/login/` para obter o token de autenticação 

No Swagger UI, clique no botão `Authorize` e insira o token

### Acessando o admin
A rota para o admin é http://localhost:8000/admin

# Endpoints e recursos:
## Autenticação e Autorização

### Registro de usuário 
```
POST /auth/register/

{
  "username": "testuser",
  "first_name": "Test",
  "last_name": "User",
  "email": "testuser@example.com",
  "phone_number": "123456789",
  "password": "password"
}
```
### Login de Usuário
```
POST /auth/login/

{
  "username": "testuser",
  "password": "password"
}
```

### Detalhes do Usuário
```
GET /auth/me/
Authorization: Bearer <access_token>
```

### Listagem de Usuários (Admin)
```
GET /auth/users/
Authorization: Bearer <admin_access_token>
```

## Gestão de Itens
### Criar Item (grupo editors)
```
POST /items/
Authorization: Bearer <access_token>

{  
	"name":  "Item 1",  
	"price":  10.0
}
```
### Listar Itens
```
GET /items/
Authorization: Bearer <access_token>
```
**Query Params:**

-   `page`: Número da página
-   `name`: Filtrar por nome
-   `price`: Filtrar por preço
-   `ordering`: Ordenar por campos (ex: `?ordering=price`)

### Detalhes do Item
```
GET /items/{id}/
Authorization: Bearer <access_token>
```

### Atualizar Item (grupo editors)
```
PUT/items/{id}/
Authorization: Bearer <access_token>

{  
	"name":  "Updated Item",  
	"price":  15.0
}
```

### Deletar Item (grupo editors)
```
DELETE/items/{id}/
Authorization: Bearer <access_token>
```

## Gestão de Pedidos
### Criar Pedido
```
POST /orders/
Authorization: Bearer <access_token>
{  
	"order_items":  [  
		{"item_id":  "item-uuid",  "quantity":  2}  
	]  
}
```
### Listar Pedidos
```
GET /orders/
Authorization: Bearer <access_token>
```
Obs: Usuários normais veem apenas seus próprios pedidos; usuários do grupo `manager` e administradores veem todos os pedidos.

**Query Params:**

-   `page`: Número da página
-   `user__username`: Filtrar por nome de usuário
-   `created_at`: Filtrar por data de criação
-   `ordering`: Ordenar por campos (ex: `?ordering=created_at`)

### Detalhes do Pedido
```
GET /orders/{id}/
Authorization: Bearer <access_token>
```
### Atualizar Pedido (grupo manager)
```
PUT /orders/{id}/
Authorization: Bearer <access_token>
{  
	"order_items":  [  
		{"item_id":  "item-uuid",  "quantity":  3}  
	]  
}
```
### Excluir Pedido (admin)
```
DELETE /orders/{id}/
Authorization: Bearer <admin_access_token>
```

## Grupos (admin)
A associação de grupos a usuários só é possível através do dashboard de admin `/admin`
### Listar Grupos
```
GET  /groups/
Authorization: Bearer <admin_access_token>
```

### Criar Grupo
```
POST /groups/
Authorization: Bearer <admin_access_token>
{  
	"name":  "new_group"  
}
```
### Atualizar Grupo
```
PUT /groups/{id}/
Authorization: Bearer <admin_access_token>
{  
	"name":  "updated_group"  
}
```

### Excluir Grupo
```
DELETE /groups/{id}/
Authorization: Bearer <admin_access_token>
```

## Paginação, Filtros e Throttling

### Paginação

Todos os endpoints que retornam listas de itens suportam paginação usando o parâmetro `page`.

**Exemplo:**

`GET /items/?page=1` 

### Filtros

Filtros podem ser aplicados usando parâmetros de consulta específicos.

**Exemplos:**

`GET /items/?name=Item+1
GET /orders/?user__username=normal_user` 

### Throttling

Para evitar sobrecarga de requisições, a API implementa throttling global e específico.
