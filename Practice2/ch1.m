% Настройка начальных параметров
C = 3 * 10^8;  % Скорость света, м/с
THERMAL_NOISE_FLOOR_DBM_HZ = -174; % Термошум

% Параметры сети
power_bs_transmitter_dbm = 46;
sectors_per_bs = 3;
power_ue_transmitter_dbm = 24;
antenna_gain_bs_dbi = 21;
penetration_loss_db = 15;
interference_margin_db = 1;
frequency_ghz = 1.8;
bandwidth_ul_mhz = 10;
bandwidth_dl_mhz = 20;
noise_figure_bs_db = 2.4;
noise_figure_ue_db = 6;
sinr_dl_db = 2;
sinr_ul_db = 4;
mimo_antennas_bs = 2;
area_total_km2 = 100; % Площадь всей зоны в квадратных километрах
area_business_centers_km2 = 4; % Площадь бизнес-центров в квадратных километрах
feeder_loss_db = 2;

% Расчет термошума для UL и DL
frequency_hz = frequency_ghz * 10^9;
bandwidth_ul_hz = bandwidth_ul_mhz * 10^6;
bandwidth_dl_hz = bandwidth_dl_mhz * 10^6;
thermal_noise_dl = calculate_thermal_noise(bandwidth_dl_hz, THERMAL_NOISE_FLOOR_DBM_HZ);
thermal_noise_ul = calculate_thermal_noise(bandwidth_ul_hz, THERMAL_NOISE_FLOOR_DBM_HZ);

% Расчет чувствительности приёмников
sensitivity_bs_dbm = calculate_sensitivity(thermal_noise_dl, sinr_dl_db, noise_figure_bs_db);
sensitivity_ue_dbm = calculate_sensitivity(thermal_noise_ul, sinr_ul_db, noise_figure_ue_db);

% Расчет выигрыша MIMO
mimo_gain_db = calculate_mimo_gain(mimo_antennas_bs);

% Максимально допустимые потери сигнала для UL и DL
max_path_loss_dl = calculate_max_path_loss(power_bs_transmitter_dbm, feeder_loss_db, antenna_gain_bs_dbi, mimo_gain_db, penetration_loss_db, interference_margin_db, sensitivity_ue_dbm);
max_path_loss_ul = calculate_max_path_loss(power_ue_transmitter_dbm, feeder_loss_db, antenna_gain_bs_dbi, mimo_gain_db, penetration_loss_db, interference_margin_db, sensitivity_bs_dbm);

fprintf("Уровень максимально допустимых потерь сигнала MAPL_UL: %.2f дБ\n", max_path_loss_ul);
fprintf("Уровень максимально допустимых потерь сигнала MAPL_DL: %.2f дБ\n", max_path_loss_dl);

% Построение графиков для UMiNLOS и Cost231
plot_umi_nlos(frequency_ghz, max_path_loss_dl, max_path_loss_ul); % График UMiNLOS
plot_cost_231(frequency_ghz, max_path_loss_dl, max_path_loss_ul); % График Cost231
plot_combined_models(frequency_ghz, max_path_loss_dl, max_path_loss_ul); % Объединённый график

% Функции
function thermal_noise = calculate_thermal_noise(bandwidth_hz, thermal_noise_floor_dbm_hz)
    thermal_noise = thermal_noise_floor_dbm_hz + 10 * log10(bandwidth_hz);
end

function sensitivity = calculate_sensitivity(thermal_noise, sinr_db, noise_figure_db)
    sensitivity = thermal_noise + sinr_db + noise_figure_db;
end

function mimo_gain = calculate_mimo_gain(mimo_antennas)
    mimo_gain = 10 * log10(mimo_antennas);
end

function max_path_loss = calculate_max_path_loss(tx_power_dbm, feeder_loss_db, antenna_gain_dbi, mimo_gain_db, penetration_loss_db, interference_margin_db, sensitivity_dbm)
    max_path_loss = tx_power_dbm - feeder_loss_db + antenna_gain_dbi + mimo_gain_db - penetration_loss_db - interference_margin_db - sensitivity_dbm;
end

% Функция для построения графика UMi NLOS
function plot_umi_nlos(frequency_ghz, max_path_loss_dl, max_path_loss_ul)
    distances = linspace(1, 5000, 1000); % расстояния в метрах
    path_loss_umi = 26 * log10(frequency_ghz) + 22.7 + 36.7 * log10(distances);
    path_loss_fspl = calculate_fspl(distances);
    
    figure;
    plot(distances, path_loss_umi, 'b-', 'LineWidth', 2);
    hold on;
    plot(distances, path_loss_fspl, 'k--', 'LineWidth', 2);
    yline(max_path_loss_dl, 'r-', 'LineWidth', 2);
    yline(max_path_loss_ul, 'g--', 'LineWidth', 2);
    xlabel('Расстояние между приемником и передатчиком, м');
    ylabel('Потери сигнала, дБ');
    title('Модель UMiNLOS');
    legend('UMiNLOS', 'FSPL', 'MAPL_DL', 'MAPL_UL');
    grid on;
    hold off;
end

% Функция для построения графика Cost231
function plot_cost_231(frequency_ghz, max_path_loss_dl, max_path_loss_ul)
    distances = linspace(1, 5000, 1000); % расстояния в метрах
    base_station_height_m = 50; % Высота базовой станции (метры)
    mobile_height_m = 1.5;      % Высота мобильного устройства (метры)
    
    a = (1.1 * log10(frequency_ghz * 1000) - 0.7) * mobile_height_m - ...
        (1.56 * log10(frequency_ghz * 1000) - 0.8);
    
    path_loss_cost = 46.3 + 33.9 * log10(frequency_ghz * 1000) - ...
        13.82 * log10(base_station_height_m) + a + ...
        (44.9 - 6.55 * log10(base_station_height_m)) * log10(distances / 1000);
    
    path_loss_fspl = calculate_fspl(distances);

    figure;
    plot(distances, path_loss_cost, 'b-', 'LineWidth', 2);
    hold on;
    plot(distances, path_loss_fspl, 'k--', 'LineWidth', 2);
    hold on;
    yline(max_path_loss_dl, 'r-', 'LineWidth', 2);
    yline(max_path_loss_ul, 'g--', 'LineWidth', 2);
    xlabel('Расстояние между приемником и передатчиком, м');
    ylabel('Потери сигнала, дБ');
    title('Модель Cost231');
    legend('Cost231', 'FSPL', 'MAPL_DL', 'MAPL_UL');
    grid on;
    hold off;
end

% Объединённый график для всех моделей (UMiNLOS, Cost231, Walfish-Ikegami LOS и NLOS)
function plot_combined_models(frequency_ghz, max_path_loss_dl, max_path_loss_ul)
    % Расстояния
    distances = linspace(1, 5000, 1000); % расстояния в метрах
    distances_km = distances / 1000; % расстояния в километрах
    
    % UMiNLOS модель
    path_loss_umi = 26 * log10(frequency_ghz) + 22.7 + 36.7 * log10(distances);
    
    % Cost231 модель
    base_station_height_m = 50;
    mobile_height_m = 1.5;
    a = (1.1 * log10(frequency_ghz * 1000) - 0.7) * mobile_height_m - ...
        (1.56 * log10(frequency_ghz * 1000) - 0.8);
    path_loss_cost = 46.3 + 33.9 * log10(frequency_ghz * 1000) - ...
        13.82 * log10(base_station_height_m) + a + ...
        (44.9 - 6.55 * log10(base_station_height_m)) * log10(distances / 1000);
    
    % Walfish-Ikegami LOS модель
    path_loss_walfish_los = 42.6 + 26 * log10(distances_km) + 20 * log10(frequency_ghz * 1000);
    
    % Walfish-Ikegami NLOS модель
    h = 30;  % Средняя высота зданий, м
    w = 20;  % Среднее расстояние между зданиями, м
    rooftop_loss = 0;  % Примерное значение
    path_loss_walfish_nlos = 13.96 + 5.8 * log10(distances_km) + rooftop_loss + ...
        20 * log10(frequency_ghz * 1000) + h - w;

    % Построение графика
    figure;
    plot(distances, path_loss_umi, 'b-', 'LineWidth', 2);
    hold on;
    plot(distances, path_loss_cost, 'g-', 'LineWidth', 2);
    plot(distances, path_loss_walfish_los, 'r-', 'LineWidth', 2);
    plot(distances, path_loss_walfish_nlos, 'm-', 'LineWidth', 2);
    yline(max_path_loss_dl, 'r--', 'LineWidth', 2);
    yline(max_path_loss_ul, 'g--', 'LineWidth', 2);
    xlabel('Расстояние между приемником и передатчиком, м');
    ylabel('Потери сигнала, дБ');
    title('Объединенный график моделей UMiNLOS, Cost231, Walfish LOS и NLOS');
    legend('UMiNLOS', 'Cost231', 'Walfish LOS', 'Walfish NLOS', 'MAPL_DL', 'MAPL_UL');
    grid on;
    hold off;
end

% Функция расчета свободных потерь пространства (FSPL)
function path_loss_fspl = calculate_fspl(distances)
    path_loss_fspl = 20 * log10(distances) + 20 * log10(1.8 * 10^9) - 147.55; % частота 1.8 ГГц
end
