% If we list all the natural numbers below 10 that are multiples of 3 or 5,
% we get 3, 5, 6 and 9. The sum of these multiples is 23.
% Find the sum of all the multiples of 3 or 5 below 1000
% https://projecteuler.net/problem=1
%
% Autor: Oscar Calvo
% Fecha: Agosto 28/2013
% % Licencia: Este archivo está bajo la licencia GPL-3.0. Ver LICENSE en el repositorio.
%
% Utilizo un ciclo FOR, pero creo que puede optimizare con vectorización
% k -> contador; a -> multiplos; s -> suma
%
clc, close all, clear all;
k=1;
tic
for i=1:999
    if rem(i,5)==0 || rem (i,3)==0
        a(k)=i;
        k=k+1;
    end
end
s=sum(a);
toc
fprintf('Suma de los múltiplos de 3 o 5 menores a 1000: %d\n', s);