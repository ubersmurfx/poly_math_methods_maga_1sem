function [route,numExpanded] = DijkstraGrid(input_map, start_coords, dest_coords, drawMap)

cmap = [1 1 1; ...
        0 0 0; ...
        1 0 0; ...
        0 0 1; ...
        0 1 0; ...
        1 1 0; ...
	0.5 0.5 0.5];

colormap(cmap);
drawMapEveryTime = drawMap;

[nrows, ncols] = size(input_map);

map = zeros(nrows, ncols);

map(~input_map) = 1;     % ðàñêðàñêà ñâîáîäíûõ êëåòîê
map(input_map)  = 2;     % ðàñêðàñêà ïðåïÿòñòâèé

start_node = sub2ind(size(map), start_coords(1), start_coords(2));
dest_node  = sub2ind(size(map), dest_coords(1),  dest_coords(2));

map(start_node) = 5;
map(dest_node)  = 6;

distanceFromStart = Inf(nrows, ncols);

parent = zeros(nrows, ncols);

distanceFromStart(start_node) = 0;

% ñ÷åò÷èê çàäåéñòâîâàííûõ â ïîèñêå êëåòîê
numExpanded = 0;

% ãëàâíûé öèêë
while true
    
    % îòðèñîâêà òåêóùåé êàðòû
    map(start_node) = 5;
    map(dest_node) = 6;
    
    if (drawMapEveryTime)
        image(1.5, 1.5, map);
        grid on;
        axis image;
        drawnow;
    end
    
    % íàõîæäåíèå êëåòêè ñ ìèíèìàëüíûì çíà÷åíèåì ðàññòîÿíèÿ
    [min_dist, current] = min(distanceFromStart(:));
    
    if ((current == dest_node) || isinf(min_dist))
        break
    end
    
    % îáíîâëåíèå êàðòû
    map(current) = 3;     % ðàñêðàñêà òåêóùåé êëåòêè êàê ïîñåùåííîé
    distanceFromStart(current) = Inf;     % óäàëåíèå ýòîé êëåòêè èç ñïèñêà ðàññìàòðèâàåìûõ
    
    % êîîðäèíàòû (ñòðîêà, ñòîëáåö) òåêóùåé êëåòêè
    [i, j] = ind2sub(size(distanceFromStart), current);
    
   % ********************************************************************* 
   % ÂÀØ ÊÎÄ ÄÎËÆÅÍ ÍÀÕÎÄÈÒÜÑß ÇÄÅÑÜ
   % íåîáõîäèìî ïîñåòèòü êàæäîãî ñîñåäà ðàññìàòðèâàåìîé êëåòêè è îáíîâèòü çíà÷åíèÿ ìàññèâîâ map, distances è parent
%    Îïðåäåëåíèå ñîñåäåé
    neighbors = [];
%     Èç-çà òîãî, ÷òî map(start_node) íà êàæäîé èòåðàöèè âûñòàâëÿåòñÿ
%     ðàâíûì 5, ïðèøëîñü ââîäèòü 3 óñëîâèå(
    top_nbr = current - 1;
    if mod(top_nbr, nrows) ~= 0
        if map(top_nbr) ~= 2 && map(top_nbr) ~= 3 && map(top_nbr) ~= 5
            neighbors = [neighbors, top_nbr];
        end
    end
    
    bot_nbr = current + 1;
    if mod(bot_nbr, nrows) ~= 1
        if map(bot_nbr) ~= 2 && map(bot_nbr) ~= 3 && map(bot_nbr) ~= 5
            neighbors = [neighbors, bot_nbr];
        end
    end
    
    left_nbr = current - nrows;
    if  left_nbr > 0
        if map(left_nbr) ~= 2 && map(left_nbr) ~= 3 && map(left_nbr) ~= 5
            neighbors = [neighbors, left_nbr];
        end
    end
    
    right_nbr = current + nrows;
    if  right_nbr < numel(map)
        if map(right_nbr) ~= 2 && map(right_nbr) ~= 3 && map(right_nbr) ~= 5
            neighbors = [neighbors, right_nbr];
        end
    end
    

    for k = 1:length(neighbors)
       nbr_id = neighbors(k);
       map(nbr_id) = 4;
       
       if (min_dist + 1) < distanceFromStart(nbr_id)
           distanceFromStart(nbr_id) = min_dist + 1;
           parent(nbr_id) = current;
       end

       map(nbr_id) = 1;
    end
    

    
   %*********************************************************************
end


%% ïîñòðîåíèå ïóòè ñ ïîìîùüþ ïîñëåäîâàòåëüíîãî ïðîõîæäåíèÿ ïî ðîäèòåëÿì
if (isinf(distanceFromStart(dest_node)))
    route = [];
else
    route = dest_node;
    
    while (parent(route(1)) ~= 0)
        route = [parent(route(1)), route];
    end
    
    % âèçóàëèçàöèÿ êàðòû è ïóòè
    for k = 2:length(route) - 1        
        map(route(k)) = 7;
        pause(0.1);
        image(1.5, 1.5, map);
        grid on;
        axis image;
    end
end

end