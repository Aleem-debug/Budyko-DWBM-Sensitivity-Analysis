 % INPUT DATA
load P
load ET0
load Runoff_obs
load generations

PET = ET0;


% % Create a matrix to store values for each run
results = zeros(49152, 7); % Columns: [Smax, alfa1, alfa2, d, dg, rmse, nnse]
% 
for sim = 1:49152
    % Read 
    Smax  = generations(sim,1);
    alfa1  = generations(sim,2);
    alfa2  = generations(sim,3);
    d  = generations(sim, 4);
    dg  = generations(sim, 5);

    % Compute dependent variables
    w1 = -1 / (alfa1 - 1);
    w2 = -1 / (alfa2 - 1);

    % INITIAL CONDITIONS
    S0 = 202;
    G0 = 48;
	
    % FIND ALL THE VALUES AT INSTANT ACCORDING TO THE CONDITIONS
    X0(1) = Smax - S0 + PET(1);
    SS(1) = X0(1) / P(1);
    X(1) = ((1 + SS(1) - (1 + (SS(1)^w1))^(1/w1))) * P(1);
    W(1) = S0 + X(1);  
    Qd(1) = P(1) - X(1);
    SSS(1) = (PET(1) + Smax) / W(1); 
    Y(1) = ((1 + SSS(1) - (1 + (SSS(1)^w2))^(1/w2))) * W(1);
    SSSS(1) = (PET(1)) / W(1);
    ET(1) = ((1 + SSSS(1) - (1 + (SSSS(1)^w2))^(1/w2))) * W(1);
    R(1) = W(1) - Y(1);
    S(1) = Y(1) - ET(1);
    Qb(1) = G0 * d;
    Qg(1) = G0 * dg;
    G(1) = G0 - Qb(1) + R(1) - Qg(1);

 for i = 2:length(P) % FROM TIME 2)
        X0(i,1) = Smax - S(i-1,1) + PET(i,1);
        SS(i,1) = X0(i,1) / P(i,1);
        X(i,1) = ((1 + SS(i,1)) - (1 + (SS(i,1)^w1))^(1/w1)) * P(i,1);
        W(i,1) = S(i-1,1) + X(i,1);
        Qd(i,1) = P(i,1) - X(i,1);
        SSS(i,1) = (PET(i,1) + Smax) / W(i,1); 
        Y(i,1) = ((1 + SSS(i,1) - (1 + (SSS(i,1)^w2))^(1/w2))) * W(i,1);
        SSSS(i,1) = (PET(i,1)) / W(i,1);
        ET(i,1) = ((1 + SSSS(i,1) - (1 + (SSSS(i,1)^w2))^(1/w2))) * W(i,1);
        R(i,1) = W(i,1) - Y(i,1);
        S(i,1) = Y(i,1) - ET(i,1);
        Qb(i,1) = G(i-1,1) * d;
        Qg(i,1) = G(i-1,1) * dg;
        G(i,1) = G(i-1,1) - Qb(i,1) + R(i,1) - Qg(i,1);
    % end

    Runoff_sim = Qd + Qb;

 end

   % RMSE calculation
    rmse = sqrt(sum((Runoff_sim - Runoff_obs).^2) / numel(P));
     m    = mean(Runoff_obs);

    % Compute numerator and denominator correctly
    numerator = sum((Runoff_obs - Runoff_sim).^2);
    denominator = sum((Runoff_obs - m).^2);
    
    % Compute NSE
    if denominator == 0
        NSE = NaN; % Avoid division by zero
        warning('Denominator is zero; NSE is undefined.');
    else
        NSE = 1 - (numerator / denominator);
    end
    
    % Compute Normalized NSE (NNSE)
    if NSE < 2  % Avoid division by zero in NNSE formula
        nnse = 1 / (2 - NSE);
   
    end

    % % Store results in matrix
    results(sim, :) = [Smax , alfa1 , alfa2 , d , dg, rmse, nnse];

end

writematrix(results, 'simulation_results_4_Sobol_Saltelli.xlsx');