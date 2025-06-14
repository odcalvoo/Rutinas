%The prime factors of 13195 are 5, 7, 13 and 29.
%What is the largest prime factor of the number 600851475143 ?
% https://projecteuler.net/problem=3
%
% Autor: Oscar Calvo
% Fecha: Agosto 28/2013
% % Licencia: Este archivo está bajo la licencia GPL-3.0. Ver LICENSE en el repositorio.
%
clc;
clear all;
close all;
z = input('Entre su número positivo: '); 
tic
% Ciclo para testear todo los enteros (2 a z) como FP
for i = 2 : z
    s = 0;
    % Es z/i un entero? Es el residuo 0?
    while z/i == floor(z/i)
        z = z/i;
        s = s + 1;
    end

    % Un FP se encontro y se muestra
    if s > 0
        str = [num2str(i) '^' num2str(s)];
        disp(str)        

        % Si z = 1, no se necesitan mas divisiones, 
        % salimos del ciclo
        if z == 1
            break
        end
    end
end
toc