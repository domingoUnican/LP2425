Ejercicio 4: Comente como funciona la clase Token, porque tiene esa estructura 
y para que sirve el método post_init

En la clase token, cada palabra clave, símbolo, operador o identificador en el código fuente se convierte en un Token para que 
el compilador o intérprete lo procese. La clase token almacena el numero de linea (lineno), el valor del token (value) y su 
tipo (tipo) basado en la enumeracion de TokenType.

El metodo post_init se utiliza para ajustar y corregir el tipo de token basandose en su valor.
Los cambios realizados en esta clase sobre el código original son para modificar todos los tipo Float
a Number estándar (ejercicio 3)