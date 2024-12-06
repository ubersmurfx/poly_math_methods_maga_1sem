function [route,numExpanded] = AStarGrid(input_map, start_coords, dest_coords, drawMap)
% ������ ��������� A* �� �����

% ������� ������: 
%     input_map: ���������� ������, � ������� ��������� ������ = 0 (false), ����������� = 1 (true)
%     start_coords and dest_coords: ���������� (������, �������) ��������� � �������� ������

% �������� ������:
%      route : ���������� ������ �������� �������� ���� ������, ��������������� ����������� ���� (����, ���� ���� �� ����������)
%      numExpanded: ����� ����� ������, ��������������� � ������ (�������� ����� �� ������ � ��� �����)

% ��������� �������� ����� ��� ������ �����
% 1 - white -- ��������� ������
% 2 - black -- �����������
% 3 - red -- ���������� ������
% 4 - blue  -- ������ �� ������ ���������������
% 5 - green -- ��������� ������
% 6 - yellow -- �������� ������

cmap = [1 1 1; ...
    0 0 0; ...
    1 0 0; ...
    0 0 1; ...
    0 1 0; ...
    1 1 0; ...
    0.5 0.5 0.5];

colormap(cmap);

% ���������� ��� ����������� ����� �� ������ ��������
drawMapEveryTime = drawMap;

[nrows, ncols] = size(input_map);

% map -- ������� ������� ��������� ������
map = zeros(nrows, ncols);

map(~input_map) = 1;     % ��������� ��������� ������
map(input_map)  = 2;     % ��������� �����������

% �������� ������ ��������� � �������� ������
start_node = sub2ind(size(map), start_coords(1), start_coords(2));
dest_node  = sub2ind(size(map), dest_coords(1),  dest_coords(2));

map(start_node) = 5;
map(dest_node)  = 6;

parent = zeros(nrows, ncols);

% meshgrid ���������� ������� ���������, ��������� -- ��. help meshgrid
[X, Y] = meshgrid (1: ncols, 1: nrows);

xd = dest_coords(1);
yd = dest_coords(2);

% ������� ��������� (������������� ����������)
H = abs(X - xd) + abs(Y - yd);
H = H';
% ������������� �������� "���������" (����������)
f = Inf(nrows, ncols);
g = Inf(nrows, ncols);

g(start_node) = 0;
f(start_node) = H(start_node);

% ������� ��������������� � ������ ������
numExpanded = 0;

% ������� ����

while true
    
    % ��������� ������� �����
    map(start_node) = 5;
    map(dest_node) = 6;
    
    % ����� ������ ��������� �����: drawMapEveryTime = true 
    if (drawMapEveryTime)
        image(1.5, 1.5, map);
        grid on;
        axis image;
        drawnow;
    end
    
    % ���������� ������ � ����������� ��������� f
    [min_f, current] = min(f(:));
    
    if ((current == dest_node) || isinf(min_f))
        break
    end
    
    % ���������� �����
    map(current) = 3;     % ��������� ������� ������ ��� ����������
    f(current) = Inf;     % �������� ���� ������ �� ������ ���������������
    
    % ���������� (������, �������) ������� ������
    [i, j] = ind2sub(size(f), current);
    
   % ********************************************************************* 
   % ��� ��� ������ ���������� �����
   % ���������� �������� ������� ������ ��������������� ������ � �������� �������� �������� map, f, g � parent
    
    
   %*********************************************************************
    
end

%% ���������� ���� � ������� ����������������� ����������� �� ���������
if (isinf(f(dest_node)))
    route = [];
else
    route = dest_node;
    
    while (parent(route(1)) ~= 0)
        route = [parent(route(1)), route];
    end

    % ������������ ����� � ����
    for k = 2:length(route) - 1        
        map(route(k)) = 7;
        pause(0.1);
        image(1.5, 1.5, map);
        grid on;
        axis image;
    end
end

end
