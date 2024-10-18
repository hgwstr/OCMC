rng('shuffle');

seq1 = rand(1, 20);
seq2 = rand(1, 20);

max_lag = 25;

[acf_seq1, lags_seq1] = xcorr(seq1, max_lag, 'coeff');
[acf_seq2, lags_seq2] = xcorr(seq2, max_lag, 'coeff');

figure;
subplot(2, 1, 1);
stem(lags_seq1, acf_seq1, 'filled');
title('Нормированная автокорреляционная функция для первой последовательности');
xlabel('Сдвиг');
ylabel('Автокорреляция');

subplot(2, 1, 2);
stem(lags_seq2, acf_seq2, 'filled');
title('Нормированная автокорреляционная функция для второй последовательности');
xlabel('Сдвиг');
ylabel('Автокорреляция');

disp('Первая случайная последовательность:');
disp(reshape(seq1, [2, 10]));
disp('Вторая случайная последовательность:');
disp(reshape(seq2, [2, 10]));
