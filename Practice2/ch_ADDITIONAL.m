f = 2.4e9;
c = 3e8;
P_t = 20;
P_r_min = -85;
N = 3;
d_max = 100;

T = [0, 21];

radii = zeros(size(T));

for i = 1:length(T)

    temp_correction = (T(i) - 0) * 0.05;
    d = linspace(1, d_max, 1000);
    PL = 26*log10(f/1e9) + 22.7 + 36.7*log10(d) + temp_correction;
    
    idx = find(P_t - PL >= P_r_min, 1, 'last');
    
    % Записываем результат
    radii(i) = d(idx);
end

% Выводим радиусы для каждой температуры
fprintf('Радиус действия при 0°C: %.2f метров\n', radii(1));
fprintf('Радиус действия при 21°C: %.2f метров\n', radii(2));

% Построение графика
figure;
plot(d, P_t - PL);
hold on;
yline(P_r_min, '--r', 'Чувствительность');
xlabel('Расстояние (м)');
ylabel('Мощность сигнала (дБм)');
legend('Сигнал', 'Чувствительность');
title('Зависимость мощности сигнала от расстояния');
grid on;
