# coin-test

Se tienen N monedas y usuarios que realizan transacciones usando esas monedas(pesos, dolares, etc).
Para evitar el double spending use transacciones atómicas.
Se uso DRF para desarrollar la API(se configuraron permisos limitando las acciones posibles de cada usuario).

#### testing

Se crearon test de la api y la validacion de permisos de usuario de la misma. Estos se encuentran en el archivo
**coins/test/test_api.py**.
Para correr los tests:
```
python manage.py test coins.tests 
```
Y para correr los tests de las transacciones:
```
python manage.py test transactions.tests 
```
