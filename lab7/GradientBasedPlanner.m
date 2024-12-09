function route = GradientBasedPlanner (f, start_coords, end_coords, max_its)
% ��������� ����� ���� �� ��������� �� ��������� ��������� ������� f 
% ������� ������:
%     start_coords � end_coords -- ���������� ��������� � �������� �����
%     max_its -- ������������ ����� ��������� �������� 
% �������� ������:
%     route -- ������ �� 2 �������� � n �����
%     ������ ������ ������������� ����������� x, y ������ (�� ���� ����������� ����)

[gx, gy] = gradient (-f);

% *******************************************************************
% ��� ��� ������ ���������� �����

gx_norm = gx/norm(gx);
gy_norm = gy/norm(gy);
route(1, :) = start_coords;
lambda = 1;
for its = 1 : max_its
    % �������� ���������� �� �������� ����
    if norm(end_coords - route(its, :)) < 2
        break
    end
    check = true;
    while check
        % ���������� ����� ���� ���������
        coord_x = route(its, 1) + lambda * gx_norm(int32(route(its, 2)), int32(route(its, 1)));
        coord_y = route(its, 2) + lambda * gy_norm(int32(route(its, 2)), int32(route(its, 1)));
        % ��������� �����
        if norm([coord_x, coord_y] - route(its, :)) > 1
            lambda = lambda / 1.1;
            check = true;
        else          
            lambda = lambda * 1.1;
            check = false;
        end
    end

%     
%     % ��������� �����
%     if norm([coord_x, coord_y] - route(its, :)) < 1
%         lambda = lambda * 1.5;
%     else
%         lambda = lambda / 1.5;
%     end
    
    % ���������� ������� ���������
    route = [route; coord_x coord_y];
    
end

% *******************************************************************

end
