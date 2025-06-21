%The sum of the squares of the first ten natural numbers is,
%(1^2) + (2^2) + ... + (10^2) = 385
%The square of the sum of the first ten natural numbers is,
%(1 + 2 + ... + 10)^2 = 55^2 = 3025
%Hence the difference between the sum of the squares of the first ten natural numbers 
%and the square of the sum is 3025 - 385 = 2640.
%Find the difference between the sum of the squares of the first one hundred natural numbers 
%and the square of the sum.
% https://projecteuler.net/problem=6
%
% Autor: Oscar Calvo
% Fecha: Agosto 28/2013
% % Licencia: Este archivo está bajo la licencia GPL-3.0. Ver LICENSE en el repositorio.
clc;clear all;close all
% Primero usando operaciones vectorizadas
tic
n = 1:100;
sum_square = sum((n.^2));
square_sum = (sum(n))^2;
differ = abs(sum_square-square_sum);
fprintf('La diferencia es  %.0d\n',differ)
toc
% Segundo, usando ciclos  %
tic
N = 100;
sum_square = 0;
square_sum = 0;
for i = 1:N
    sum_square = sum_square + i^2;
    square_sum = square_sum+i;
end
square_sum1 = square_sum^2;
difference = abs(sum_square-square_sum1);
fprintf('La diferencia es  %.0d\n',difference)
toc