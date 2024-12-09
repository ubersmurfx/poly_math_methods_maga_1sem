function route = GradientBasedPlanner (f, start_coords, end_coords, max_its)
% требуется найти путь на плоскости на основании градиента функции f 
% входные данные:
%     start_coords и end_coords -- координаты начальной и конечной точек
%     max_its -- максимальное число возможных итераций 
% выходные данные:
%     route -- массив из 2 столбцов и n строк
%     каждая строка соответствует координатам x, y робота (по мере прохождения пути)

[gx, gy] = gradient (-f);

% *******************************************************************
% ВАШ КОД ДОЛЖЕН НАХОДИТЬСЯ ЗДЕСЬ

gx_norm = gx/norm(gx);
gy_norm = gy/norm(gy);
route(1, :) = start_coords;
lambda = 1;
for its = 1 : max_its
    % проверка расстояния до конечной цели
    if norm(end_coords - route(its, :)) < 2
        break
    end
    check = true;
    while check
        % вычисление новой пары координат
        coord_x = route(its, 1) + lambda * gx_norm(int32(route(its, 2)), int32(route(its, 1)));
        coord_y = route(its, 2) + lambda * gy_norm(int32(route(its, 2)), int32(route(its, 1)));
        % коррекция лямбд
        if norm([coord_x, coord_y] - route(its, :)) > 1
            lambda = lambda / 1.1;
            check = true;
        else          
            lambda = lambda * 1.1;
            check = false;
        end
    end

%     
%     % коррекция лямбд
%     if norm([coord_x, coord_y] - route(its, :)) < 1
%         lambda = lambda * 1.5;
%     else
%         lambda = lambda / 1.5;
%     end
    
    % заполнение массива координат
    route = [route; coord_x coord_y];
    
end

% *******************************************************************

end
