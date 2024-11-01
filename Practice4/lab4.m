function main
    sequence_length = 31;

    % Первая последовательность Голда (x = 8, y = 15)
    x1 = [0 1 0 0 0]; % 01000
    y1 = [0 1 1 1 1]; % 01111
    gold_sequence1 = generateGoldSequence(x1, y1, sequence_length);

    % Вторая последовательность Голда (x = 9, y = 10)
    x2 = [0 1 0 0 1]; % 01001
    y2 = [0 1 0 1 0]; % 01010
    gold_sequence2 = generateGoldSequence(x2, y2, sequence_length);

    % Вывод первой и второй последовательности
    disp('Первая последовательность Голда (x=8, y=15):');
    fprintf('%d', gold_sequence1);
    fprintf('\n');

    disp('Вторая последовательность Голда (x=9, y=10):');
    fprintf('%d', gold_sequence2);
    fprintf('\n');

    % Автокорреляция с проверкой на m-последовательность
    disp('Автокорреляция первой последовательности с проверкой на m-последовательность:');
    calculateAutocorrelationAndCheckMSequence(gold_sequence1, sequence_length);

    % Взаимная корреляция между первой и второй последовательностями
    cross_correlation = correlation(gold_sequence1, gold_sequence2, sequence_length);
    fprintf(['\nВзаимная корреляция между первой и второй последовательностями: ', num2str(cross_correlation), '/', num2str(sequence_length)]);
    fprintf('\n');

    % Графическая визуализация
    visualizeAutocorrelation(gold_sequence1);
    visualizeCrossCorrelation(gold_sequence1, gold_sequence2);
end

% Функция для генерации последовательности Голда
function gold_sequence = generateGoldSequence(x, y, length)
    gold_sequence = zeros(1, length);
    for i = 1:length
        new_bit_x = xor(x(5), x(3)); % XOR элементов 5 и 3
        new_bit_y = xor(y(5), y(3)); % XOR элементов 5 и 3
        gold_sequence(i) = xor(x(5), y(5)); % Голд последовательность как XOR выходов двух регистров

        % Обновляем регистры
        x = [new_bit_x, x(1:4)];
        y = [new_bit_y, y(1:4)];
    end
end

% Проверка сбалансированности
function balanced = checkBalance(sequence)
    count_ones = sum(sequence == 1);
    count_zeros = length(sequence) - count_ones;
    balance = abs(count_ones - count_zeros);
    if balance <= 1
        balanced = true;
    else
        balanced = false;
    end

    if balance
       fprintf('\nm-последовательность');
    else
       fprintf('\nне m-последовательность');
    end
end

% Проверка на m-последовательность
function is_m = isMSequence(sequence)
    if length(sequence) ~= 31
        is_m = false;
    else
        is_m = checkBalance(sequence);
    end
end

% Функция для автокорреляции с проверкой на m-последовательность
function calculateAutocorrelationAndCheckMSequence(sequence, sequence_length)
    for shift = 0:sequence_length - 1
        shifted_sequence = circshift(sequence, [0 shift]);
        corr = calculateCorrelation(sequence, shifted_sequence);
        is_m_sequence = isMSequence(shifted_sequence);

        fprintf('%4d | %s | %4d/%d | %s\n', shift, sprintf('%d ', shifted_sequence), corr, is_m_sequence);
    end
end

% Расчет корреляции между двумя последовательностями
function corr = correlation(seq1, seq2, length)
    corr = sum(seq1(1:length) .* seq2(1:length));
end

% Расчет корреляции между двумя последовательностями
function corr = calculateCorrelation(seq1, seq2)
    corr = sum(seq1 == seq2) - sum(seq1 ~= seq2);
end

% Визуализация автокорреляции
function visualizeAutocorrelation(sequence)
    sequence_length = length(sequence);
    autocorr_values = zeros(1, sequence_length);

    for shift = 0:sequence_length
        shifted_sequence = circshift(sequence, [0 shift]);
        autocorr_values(shift + 1) = calculateCorrelation(sequence, shifted_sequence);
    end

    figure;
    stem(0:sequence_length, autocorr_values, 'filled', 'red');
    title('Autocorrelation of Gold Sequence');
    xlabel('Shift');
    ylabel('Correlation');
    grid on;
end

% Визуализация взаимной корреляции
function visualizeCrossCorrelation(seq1, seq2)
    sequence_length = length(seq1);
    crosscorr_values = zeros(1, sequence_length);

    for shift = 0:sequence_length
        shifted_seq2 = circshift(seq2, [0 shift]);
        crosscorr_values(shift + 1) = correlation(seq1, shifted_seq2, sequence_length);
    end

    figure;
    stem(0:sequence_length, crosscorr_values, 'filled', 'green');
    title('Cross-Correlation of Two Gold Sequences');
    xlabel('Shift');
    ylabel('Correlation');
    grid on;
end
