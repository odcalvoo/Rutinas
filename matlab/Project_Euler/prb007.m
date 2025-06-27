%By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, 
%we can see that the 6th prime is 13.
%What is the 10001st prime number?
% https://projecteuler.net/problem=7
%
% Autor: Oscar Calvo
% Fecha: Agosto 28/2013
% % Licencia: Este archivo está bajo la licencia GPL-3.0. Ver LICENSE en el repositorio.
clc;clear all;close all
m = input('Posicion del numero primo: ');
tic
i = 1;
n = 2;
while(i<m) % No importa si empezamos con el primer primo, index = 1 prime (n) = 2,
               % Vamos hasta que encontremos el primo 10,001!
    n = n+1;   % n representa el numero que estamos chequeando, asi, sabemos quw 2 es primo, chequeamos el siguiente!
    x = 2;     % x va a ser el numero que nosotros dividimos por n. empezamos en 2 (es par) y lo incrementamos
    while x <= sqrt(n)  % trampita de optmizacion. Chequeamos solo hasta la raiz cuadrada de N, en vez de todo N
                        % Si no encontramos un divisor menor o igual a sqrt(n), entonces no hay un numero mayor 
                        % correspondiente
        if mod(n,x) == 0  % Si al dividir el numero actual por x no tiene residuo
            break         % salimos
        end
        x = x+1;          % Pero si SI hay residuo, (i.e. no es un divisor), chequeamos el siguiente numero
    end
    if x > sqrt(n)  % Esto solo puede ser cierto si nunca salimos del ciclo anterior (es decirm tenemos un primo!)
        i = i+1;    % No nos interesa almacenos nuestros numeros primos, solo incrementamos el contador,
                    % es como el contador para VERDADEROS primos.
    end
end
toc
fprintf('La respuesta es %.0d\n',n)