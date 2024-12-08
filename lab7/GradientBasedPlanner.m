function route = GradientBasedPlanner (f, start_coords, end_coords, max_its)
% ��������� ����� ���� �� ��������� �� ��������� ��������� ������� f 
% ������� ������:
%     start_coords � end_coords -- ���������� ��������� � �������� �����
%     max_its -- ������������ ����� ��������� �������� 
% �������� ������:
%     route -- ������ �� 2 �������� � n �����
%     ������ ������ ������������� ����������� x, y ������ (�� ���� ����������� ����)

[gx, gy] = gradient (-f);

% [nrows, ncols] = size(f);

% gx = normalize(gx);
% gy = normalize(gy);

route = start_coords;

current_coords = start_coords;

% *******************************************************************
% ��� ��� ������ ���������� �����

    function distance = DistanceBetweenPoints(point_1, point_2)
        distance = sqrt((point_1(1)-point_2(1))^2+(point_1(2)-point_2(2))^2); 
        
    end


for k = 1:(max_its-1)
    
%     current_index = sub2ind(size(f), round(current_coords(1)), round(current_coords(2)));
    
%     x = gx(current_index);
%     y = gy(current_index);
    current_coords(1) = current_coords(1) + gx(round(current_coords(2)), round(current_coords(1)));
    current_coords(2) = current_coords(2) + gy(round(current_coords(2)), round(current_coords(1)));
    
    route(end+1,:) = current_coords;
    
    distance = DistanceBetweenPoints(current_coords, end_coords)
    if  distance <= 2
        break
    end
    
end
route(end+1, :) = end_coords 
% *******************************************************************

end
