# Created by Octave 4.2.2, Wed Mar 21 16:23:19 2018 GMT <unknown@unknown>
# 
clear;
close all;
clc;

# INPUTS - START
pkg load communications;
x_range = [0, 127];
xn = 127;
# count of generations
g = 100;
# count of chromosomes
N = 20;
# interbreeding ratio
PK = 0.8;
# mutation ratio
PM = 0.1;
# funtion to optimize
f = @(x) 2 * (x^2 + 1);
# INPUTS - END

values = round( (x_range(end) - x_range(1)).*rand(N, 1) + x_range(1) );
chromosomes = de2bi( values );

# just for clean display
for i = 1:size(chromosomes, 1)
  fprintf('%d', chromosomes(i,:));
  fprintf('\n');
end