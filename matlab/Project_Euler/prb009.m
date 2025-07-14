%A Pythagorean triplet is a set of three natural numbers, a < b < c, for which,
%a^2 + b^2 = c^2
%For example, 3^2 + 4^2 = 9 + 16 = 25 = 5^2.
%There exists exactly one Pythagorean triplet for which a + b + c = 1000.
%Find the product abc.
%https://projecteuler.net/problem=9
%
% Autor: Oscar Calvo
% Fecha: Agosto 28/2013
% Licencia: Este archivo está bajo la licencia GPL-3.0. Ver LICENSE en el repositorio.
clc; clear all; close all;
tic
% Definir el límite de la suma
sum_limit = 1000;
% Bucle optimizado para a y b, con c = sum_limit - a - b
for a = 1:sum_limit/3  % a < b < c, así que a no puede exceder 1/3 de 1000
    for b = a+1:sum_limit/2  % b debe ser mayor que a y menor que 500
        c = sum_limit - a - b;
        if c > b && a^2 + b^2 == c^2  % Verificar triplete pitagórico y a < b < c
            product = a * b * c;
            break;
        end
    end
    if exist('product', 'var')
        break;
    end
end
fprintf('El producto abc para el triplete pitagórico con suma 1000 es %.0f\n', product);
toc