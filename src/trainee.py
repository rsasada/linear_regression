import numpy as np
import json
import matplotlib.pyplot as plt


def load_data(filepath):
    data = np.loadtxt(filepath, delimiter=',', skiprows=1)
    return data

def standardize_data(data):

    standardized_data = data.copy()

    mileage_mean = np.mean(data[:, 0])
    mileage_std = np.std(data[:, 0])
    standardized_data[:, 0] = (data[:, 0] - mileage_mean) / mileage_std

    price_mean = np.mean(data[:, 1])
    price_std = np.std(data[:, 1])
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
    max_iterations = 10000

    for j in range(max_iterations):
        sum0 = 0
        sum1 = 0
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
            "b": theta[0],
            "a": theta[1]
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