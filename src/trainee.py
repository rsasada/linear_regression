import numpy as np
import json
import matplotlib.pyplot as plt


def load_data(filepath):
    try:
        data = np.loadtxt(filepath, delimiter=',', skiprows=1)
    except FileNotFoundError:
        print(f"Error: '{filepath}' not found")
        exit(1)
    except ValueError as e:
        print(f"Error: '{filepath}' is not in the correct format. ({e})")
        exit(1)
    if data.ndim != 2 or data.shape[1] < 2:
        print(f"Error: '{filepath}' requires at least 2 columns.")
        exit(1)
    if np.any(data[:, 0] < 0):
        print(f"Error: '{filepath}' contains negative mileage values.")
        exit(1)
    return data

def standardize_data(data):

    standardized_data = data.copy()

    mileage_mean = np.mean(data[:, 0])
    mileage_std = np.std(data[:, 0])
    if mileage_std == 0:
        print("Error: The variance of mileage is zero (all data have the same value). Standardization cannot be performed.")
        exit(1)
    standardized_data[:, 0] = (data[:, 0] - mileage_mean) / mileage_std

    price_mean = np.mean(data[:, 1])
    price_std = np.std(data[:, 1])
    if price_std == 0:
        print("Error: The variance of price is zero (all data have the same value). Standardization cannot be performed.")
        exit(1)
    standardized_data[:, 1] = (data[:, 1] - price_mean) / price_std

    params = (
        (mileage_mean, mileage_std),
        (price_mean, price_std)
    )

    return standardized_data, params

def inverse_tandardizer(theta, params):
    
    mileage_mean = params[0][0]
    mileage_std = params[0][1]

    price_mean = params[1][0]
    price_std = params[1][1]

    theta[1] = theta[1] * ( price_std / mileage_std)
    theta[0] = (theta[0] * price_std + price_mean) - (theta[1] * mileage_mean)

    return theta

def train_data(data):
    theta = np.zeros(2, dtype=float)

    learning_rate = 0.1
    tolerance = 1e-6
    max_iterations = 1000

    for j in range(max_iterations):
        sum0 = 0.0
        sum1 = 0.0
        for i in range(len(data)):
            sum0 += ((theta[1] * data[i][0]) + theta[0]) - data[i][1]
            sum1 += ((theta[1] * data[i][0]) + theta[0] - data[i][1]) * data[i][0]
        
        tmp0 = learning_rate * (sum0 / len(data))
        tmp1 = learning_rate * (sum1 / len(data))

        theta[0] -= tmp0
        theta[1] -= tmp1

        if abs(tmp0) < tolerance and abs(tmp1) < tolerance:
            print(f"Converged at iteration {j + 1}")
            break
    
    return theta


if __name__ == "__main__":

    data = load_data('data.csv')
    normalized_data, params  = standardize_data(data)
  
    theta = train_data(normalized_data)
    theta = inverse_tandardizer(theta, params)

    original_theta_to_save = {
            "theta0": float(theta[0]),
            "theta1": float(theta[1])
        }
    try:
        with open('model_param.json', 'w') as f:
            json.dump(original_theta_to_save, f, indent=4)
    except Exception as e:
        print(f"\n--- JSONファイルの保存に失敗しました: {e} ---")

    plt.figure(figsize=(10, 6))
    plt.title('Price vs Mileage')
    plt.xlabel('Mileage (km)')
    plt.ylabel('Price (price)')

    original_mileage = data[:, 0]
    original_price = data[:, 1]
    plt.scatter(original_mileage, original_price, color='blue', label='data')

    b_original = theta[0]
    a_original = theta[1]
    
    x_line = np.array([np.min(original_mileage), np.max(original_mileage)])
    
    y_line = (a_original * x_line) + b_original
    
    plt.plot(x_line, y_line, color='red', label='Prediction Line (Linear Regression)')

    plt.legend()
    plt.grid(True)
    plt.show()
    plt.close()