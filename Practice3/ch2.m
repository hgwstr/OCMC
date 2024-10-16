% Параметры
f1 = 8;
f2 = f1 + 4;
f3 = 2 * f1 + 1;

% Время
t = 0:0.01:1;

% Определение сигналов
s1 = cos(2 * pi * f1 * t);
s2 = cos(2 * pi * f2 * t);
s3 = cos(2 * pi * f3 * t);

% Сигналы a и b
a = 2 * s1 + 4 * s2 + s3;
b = s1 + s2;

% Корреляция
corr_ab = xcorr(a, b);

% Нормализация
norm_a = sqrt(sum(a.^2));
norm_b = sqrt(sum(b.^2));

if norm_a == 0 || norm_b == 0
    disp('Ошибка: Один из сигналов имеет нулевую энергию.');
else
    norm_corr_ab = sum(a .* b) / (norm_a * norm_b);
    disp('Нормализованная корреляция между a и b:');
    disp(norm_corr_ab);
end


disp('Корреляция между a и b:');
disp(corr_ab);

% Сдвиг массива b и вычисление корреляции
max_corr = -inf;
best_shift = 0;

for shift = 0:length(b)-1
    b_shifted = circshift(b, shift);
    current_corr = sum(a .* b_shifted) / (norm(a) * norm(b_shifted));
    %disp(['Сдвиг: ', num2str(shift), ' Корреляция: ', num2str(current_corr)]);
    if current_corr > max_corr
        max_corr = current_corr;
        best_shift = shift;
    end
end


% Построение графиков
figure;
subplot(2,1,1);
plot(t, a);
title('Сигнал a');

subplot(2,1,2);
plot(t, circshift(b, best_shift));
title(['Сигнал b, сдвинутый на ', num2str(best_shift)]);
