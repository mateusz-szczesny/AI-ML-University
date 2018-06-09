# Created by Octave 4.2.2, Wed Mar 21 16:23:19 2018 GMT <matty.szczesny@gmail.com>
#
clear;
close all;
clc;
 
# INPUTS - START
pkg load communications;
x_range = [0, 127];
xn = 127;
# count of generations
gens = 100;
# count of chromosomes
N = 50;
# interbreeding ratio
PK = 0.8;
# mutation ratio
PM = 0.2;
# funtion to optimize
f = @(x) 2 * (x^2 + 1);
# INPUTS - END
 
#STEP: CREATION
tempValues = zeros(N, 1);
tempChromosomes = zeros(N, 7);
values = round( (x_range(end) - x_range(1)).*rand(N, 1) + x_range(1) );
chromosomes = de2bi( values );
 
# just for clean display
disp("1st generation:")
for i = 1:size(chromosomes, 1)
  fprintf('%d', chromosomes(i,:));
  fprintf('\n');
end
 
#REPEAT FOR EACH GENERATION
for g = 1:gens
  # STEP: SELECTION -> roulette selection
  for i = 1:N
     values(i, 2) = (values(i, 1) / sum(values(:, 1))) * 100;
  end
 
  for i = 1:N
    random = (rand()*100);
    for j = 1:N
      probability = sum(values(1:j, 2));
      if random < probability
        tempValues(i) = values(j, 1);
        break;
      end
    end
  end
  #update of values and it's binary representation
  values = tempValues;
  chromosomes = de2bi( values );
  #STEP: INTERBREEIDING
  pairs = randperm(N);
  #for each pair
  for i = 1:2:N
    if PK > rand()
      locus = round((size(chromosomes, 2) - 1).*rand() + 1);
      tempChromosomes(pairs(i), :) = [chromosomes(pairs(i), 1:locus), chromosomes(pairs(i+1), locus+1:end)];
      tempChromosomes(pairs(i+1), :) = [chromosomes(pairs(i+1), 1:locus), chromosomes(pairs(i), locus+1:end)];
    else
      tempChromosomes(pairs(i), :) = chromosomes(pairs(i), :);
      tempChromosomes(pairs(i+1), :) = chromosomes(pairs(i), :);
    end
  end
 
 
   
  #STEP: MUTATION
  random = randi([1 N], 1, 1);
  if PM > rand()
    locus = round((size(chromosomes, 2) - 1).*rand() + 1);
    chromosomes(random, locus) = ~(chromosomes(random, locus));
  end
  #update of values from it's binary representation
  values = bi2de( chromosomes );
end
#REPEAT
disp("");
disp("Newest generation:")
for i = 1:size(chromosomes, 1)
  fprintf('%d', chromosomes(i,:));
  fprintf('\n');
end