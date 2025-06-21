%2520 is the smallest number that can be divided by each of the numbers from 1 to 10
%without any remainder.
%What is the smallest positive number that is evenly divisible by all of the numbers
%from 1 to 20?
% https://projecteuler.net/problem=5
%
% Autor: Oscar Calvo
% Fecha: Agosto 28/2013
% % Licencia: Este archivo est� bajo la licencia GPL-3.0. Ver LICENSE en el repositorio.
% Originalmente se hab�a implementado un m�todo de fuerza bruta, pero se presenta a continuaci�n un metodo m�s eficiente, basado en el MCM y MCD
%
clc; clear all; close all;
tic

% Funci�n para calcular el m�ximo com�n divisor (MCD) usando el algoritmo de Euclides
function mcd = calculate_mcd(a, b)
    while b ~= 0
        temp = b;
        b = mod(a, b);
        a = temp;
    end
    mcd = a;
end

% Calcular el m�nimo com�n m�ltiplo (MCM) de los n�meros del 1 al 20
N = 20;
result = 1;
for i = 2:N
    result = (result * i) / calculate_mcd(result, i);
end

fprintf('El n�mero m�s peque�o divisible por todos los enteros del 1 al 20 es %.0f\n', result);
toc
