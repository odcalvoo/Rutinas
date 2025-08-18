%The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.
%Find the sum of all the primes below two million.
% https://projecteuler.net/problem=10
% Autor: Oscar Calvo
% Fecha: Agosto 28/2013
% Licencia: Este archivo está bajo la licencia GPL-3.0. Ver LICENSE en el repositorio.
%
clear all;close all;clc;
tic
p=primes(2000000);
s=sum(p);
toc
fprintf('La respuesta es %.0d\n',s)