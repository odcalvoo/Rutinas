%A palindromic number reads the same both ways.
%The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.
%Find the largest palindrome made from the product of two 3-digit numbers.
% https://projecteuler.net/problem=4
%
% Autor: Oscar Calvo
% Fecha: Agosto 28/2013
% % Licencia: Este archivo está bajo la licencia GPL-3.0. Ver LICENSE en el repositorio.
%
clc;clear all;close all;
i = 90;
j = 1;
tic
for g = 900:999
for k = 900:999
    p = g*k;
    b=num2str(p);
    if b==fliplr(b);
    a(j) = p;
    j = j+1;
    end
end
end
m=max(a);
toc
fprintf('La respuesta es %.0d\n',m)