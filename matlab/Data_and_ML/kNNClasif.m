function ClaseNuevaObs = kNNClasif(NuevaObs,Datos,Clase,k)

% Autor: Oscar Calvo, sobre una idea aparecida en el libro "100 Problemas Resueltos de Estadística Multivariable (implementados en Matlab)"
% de Baillo y Grané (2008)
% Fecha: Junio 16/2025
% % Licencia: Este archivo está bajo la licencia GPL-3.0. Ver LICENSE en el repositorio.
%

%kNNClasif(NuevaObs,Datos,Clase)

% Clasifica una nueva observacion NuevaObs utilizando la regla kNN (k vecinos más proximos).
% Variables de entrada:
%   NuevaObs = vector a clasificar con nº de componentes p
%   Datos = Matriz de datos nxp cuyas filas son individuos de clase (0 o 1) conocida.
%   Clase = Vector nx1 que contiene las etiquetas 0 o 1 de los individuos de la muestra.
%   k = Numero de vecinos mas proximos a NuevaObs que consideramos para su clasificacion.
% Variable de salida:
%   Clase = 0 si la mayoria de los k vecinos más próximos a NuevaObs son de
%   la clase 0. Clase = 1 si la mayoria de dichos kNN son de la clase 1. 
%   En caso de empate se sortea "una moneda" y se decide Clase aleatoriamente.
%
% Se provee como ejemplo, el archivo CORAZON2.txt, para comprbar su ejecucion.
% El archivo que contiene mediciones tomadas a pacientes que han sufrido ataques cardiacos
% tales como edad a la que sufrió el infarto (primera columna), contractilidad del corazon en las columnas
% segunda y tercera, la cuarta columna muestra la dimension ventricular izquierda al final de la diastole
% y la quinta columna es la medida de como se mueven los segmentos del ventriculo izquierdo.
% La ultima columna es la clase que es cero (O) para quienes vivieron menos de un año despues de ocurrido el infarto
% y es uno (1) para quienes vivieron más de un año.

% Ejemplo:
%   % Cargar datos de corazon2.txt
%   data = load('corazon2.txt');
%   Datos = data(:, 1:5); % Características
%   Clase = data(:, 6);   % Etiquetas
%   NuevaObs = [60, 0.25, 10, 4.5, 15]; % Nueva observación
%   k = 3;
%   ClaseNuevaObs = kNNClasif(NuevaObs, Datos, Clase, k);
%
% Notas:
%   - Los datos deben estar en la misma escala para evitar sesgos en las distancias.
%   - El archivo corazon2.txt contiene datos de pacientes con ataques cardíacos (ver descripción completa en el README).

% Control del numero de variables de entrada

if nargin < 4  
    error('Faltan variables de entrada') 
end

NuevaObs = NuevaObs(:) ; % "Obligamos" a NuevaObs a que sea vector columna
Clase = Clase(:) ;
    
% Control de la dimension de variables de entrada
[n,p] = size(Datos) ; p2 = length(NuevaObs) ; [nC,pC] = size(Clase) ;
if n ~= nC  
    error('El numero de filas de la muestra no coincide con el de la clase')
end
if p ~= p2 
    error('El numero de datos de la nueva observacion no es coherente con la dimension de la muestra')
end
if pC ~= 1 
    error('La clase tiene que ser un vector, no una matriz')
end
clear nC pC p2
    
% Calculamos la distancia euclídea de NuevaObs a la muestra
DistEuclid = sum((Datos - ones(n,1) * NuevaObs').^2,2) ; % Vector columna
[DistEOrd,IndEOrd] = sort(DistEuclid) ; % Ordenamos las distancias de menor a mayor.
ClasekNN = Clase(IndEOrd([1:k])) ; % Clases de los k-NN
NumkNN1 = sum(ClasekNN == 1) ; % Núm. de los kNN que pertenecen a Clase 1.
NumkNN0 = sum(ClasekNN == 0) ; % Núm. de los kNN que pertenecen a Clase 0.
if NumkNN1 > NumkNN0
    ClaseNuevaObs = 1 ;
elseif NumkNN1 < NumkNN0
    ClaseNuevaObs = 0 ;    
else % Se "tira una moneda al aire" y se decide la clase aleatoriamente    
    u = rand(1,1) ;
    ClaseNuevaObs = (u >= 0.5) ;
end    