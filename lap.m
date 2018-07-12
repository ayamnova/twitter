%Asp = sparse(load("C:\Users\OSU user\Desktop\mat\userMatrix"));
A = sparse(load("/home/scratch1/karsdou/umataa"));
disp("Loaded");
mult_num = A(2, 1) / A(1, 1);
% get the first row
temp = A(0: end);

% multiply every element of temp by mult_num
s = temp.*mult_num;

% subtract s from row 2
A(1: end) - s;

%Asp = [Asp; zeros(
%At = transpose(Asp); 
%edges = Asp + At;
%[L, XY] = unmesh(edges);
% Asp = sparse(load("/home/karsdou/Desktop/userMatrix"));
D = diag(sum(Asp,1));
disp("Degree Matrix Done");
L = D - Asp;
disp("Laplacian Matrix Done");
e = eig(L);
disp("Eigen values done");
% dlmwrite("C:\Users\OSU user\Desktop\out\usermatrix.txt",e,'delimiter','\t');
dlmwrite("/home/scratch1/karsdou/usermatrix.txt",e,'delimiter','\t');
