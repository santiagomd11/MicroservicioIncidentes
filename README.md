# Servicio de Manejo de Incidentes

Este microservicio permite la gestión de incidentes, desde su creación, consulta, búsqueda y actualización de respuestas, y es el encargado de manejar las transacciones relacionadas con los incidentes.

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Pruebas](#pruebas)
5. [Autor](#autor)

## Estructura

```plaintext
.
├── Dockerfile
├── Pipfile
├── Pipfile.lock
├── README.md
├── local
│   └── docker-compose.yaml
├── piptest.ini
├── postman
│   └── incidents.postman_collection.json
├── src
│   ├── __init__.py
│   ├── blueprints
│   │   ├── __init__.py
│   │   └── services.py
│   ├── commands
│   │   ├── __init__.py
│   │   ├── base_command.py
│   │   ├── clear_database.py
│   │   ├── create_incident.py
│   │   ├── create_user.py
│   │   ├── get_incident.py
│   │   ├── get_incidents.py
│   │   ├── get_user.py
│   │   ├── ping.py
│   │   ├── search_incident.py
│   │   └── update_incident_response.py
│   ├── errors
│   │   ├── __init__.py
│   │   └── errors.py
│   ├── main.py
│   └── models
│       ├── __init__.py
│       ├── incident.py
│       └── user.py
└── tests
    ├── __init__.py
    ├── blueprints
    │   ├── test_clear_db.py
    │   ├── test_incidents.py
    │   ├── test_ping.py
    │   └── test_users.py
    ├── commands
    │   ├── test_clear_database.py
    │   ├── test_create_incident.py
    │   ├── test_create_user.py
    │   ├── test_get_incident.py
    │   ├── test_get_incidents.py
    │   ├── test_get_user.py
    │   ├── test_ping_command.py
    │   └── test_search_incident.py
    └── conftest.py
```

## Uso

### 1. Creación de usuarios

Permite la creación de un usuario con los datos proporcionados.

<table>
<tr>
<td> Método </td>
<td> POST </td>
</tr>
<tr>
<td> Ruta </td>
<td> <strong>/incidents/create_user</strong> </td>
</tr>
<tr>
<td> Parámetros </td>
<td> N/A </td>
</tr>
<tr>
<td> Encabezados </td>
<td> N/A </td>
</tr>
<tr>
<td> Cuerpo </td>
<td>

```json
{
    "id": "12345",
    "name": "John Doe",
    "phone": "1234567890",
    "email": "john.doe@example.com",
    "company": "example_company"
}
```
</td>
</tr>
<td> Respuesta </td>
<td>

```json
{
    "id": "12345",
    "name": "John Doe",
    "phone": "1234567890",
    "email": "john.doe@example.com",
    "company": "example_company"
}
```
</td>
<tr>

</table>

### 2. Creación de incidentes

Crea un incidente con los datos proporcionados.

<table>
<tr>
<td> Método </td>
<td> POST </td>
</tr>
<tr>
<td> Ruta </td>
<td> <strong>/incidents/create_incident</strong> </td>
</tr>
<tr>
<td> Parámetros </td>
<td> N/A </td>
</tr>
<tr>
<td> Encabezados </td>
<td> N/A </td>
</tr>
<tr>
<td> Cuerpo </td>
<td>

```json
{
    "type": "PETICION",
    "description": "Test incident",
    "date": "2024-10-01T00:00:00Z",
    "userId": "12345",
    "channel": "WEB",
    "agentId": "agent123",
    "company": "example_company"
}
```
</td>
</tr>
</td>
<td> Respuesta </td>
<td>

```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "description": "Test incident",
    "userEmail": "user@example.com"
}
```
</td>
<tr>

</table>

### 3. Obtener información de un incidente

Obtiene los detalles de un incidente a partir de su ID.

<table>
<tr>
<td> Método </td>
<td> GET </td>
</tr>
<tr>
<td> Ruta </td>
<td> <strong>/incidents/get_incident/&lt;incident_id&gt;/&lt;company&gt;</strong> </td>
</tr>
<tr>
<td> Parámetros </td>
<td> <strong>incident_id, company</strong> </td>
</tr>
<tr>
<td> Encabezados </td>
<td> N/A </td>
</tr>
<tr>
<td> Cuerpo </td>
<td> N/A </td>
</tr>
</td>
<td> Respuesta </td>
<td>

```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "type": "PETICION",
    "description": "Test incident",
    "date": "2024-10-01T00:00:00Z",
    "userId": "12345",
    "channel": "WEB",
    "agentId": "agent123",
    "company": "example_company",
    "solved": false,
    "response": null
}
```
</td>
<tr>

</table>

### 4. Búsqueda de incidentes

Permite buscar incidentes con base en los criterios proporcionados.

<table>
<tr>
<td> Método </td>
<td> POST </td>
</tr>
<tr>
<td> Ruta </td>
<td> <strong>/incidents/search_incident</strong> </td>
</tr>
<tr>
<td> Parámetros </td>
<td> N/A </td>
</tr>
<tr>
<td> Encabezados </td>
<td> N/A </td>
</tr>
<tr>
<td> Cuerpo </td>
<td>

```json
{
    "userId": "12345",
    "incidentId": "123e4567-e89b-12d3-a456-426614174000"
}
```
</td>
</tr>
<td> Respuesta </td>
<td>

```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "type": "PETICION",
    "description": "Test incident",
    "date": "2024-10-01T00:00:00Z",
    "userId": "12345",
    "channel": "WEB",
    "agentId": "agent123",
    "company": "example_company",
    "solved": false,
    "response": null
}
```
</td>
<tr>

</table>

### 5. Actualización de respuesta de incidente

Permite actualizar la respuesta de un incidente existente.

<table>
<tr>
<td> Método </td>
<td> PUT </td>
</tr>
<tr>
<td> Ruta </td>
<td> <strong>/incidents/update_incident_response</strong> </td>
</tr>
<tr>
<td> Parámetros </td>
<td> N/A </td>
</tr>
<tr>
<td> Encabezados </td>
<td> N/A </td>
</tr>
<tr>
<td> Cuerpo </td>
<td>

```json
{
    "incidentId": "123e4567-e89b-12d3-a456-426614174000",
    "company": "example_company",
    "response": "Incident has been resolved."
}
```
</td>
</tr>
</table>

### 6. Consulta de salud del servicio

Verifica el estado de salud del servicio.

<table>
<tr>
<td> Método </td>
<td> GET </td>
</tr>
<tr>
<td> Ruta </td>
<td> <strong>/incidents/ping</strong> </td>
</tr>
<tr>
<td> Parámetros </td>
<td> N/A </td>
</tr>
<tr>
<td> Encabezados </td>
<td> N/A </td>
</tr>
<tr>

## Pruebas

Para correr las pruebas del proyecto ejecutar los siguientes comandos: 

```bash
pipenv shell
```
```bash
pipenv run pytest --cov=src -v -s --cov-fail-under=80 --log-cli-level=INFO
```

## Autor

Victor Santiago Montaño Diaz
