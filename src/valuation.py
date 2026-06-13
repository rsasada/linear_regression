import json

def estimate_price(mileage, theta0, theta1):
    return theta0 + (theta1 * mileage)

def main():
    try:
        with open('model_param.json', 'r') as f:
            theta_values = json.load(f)
        theta0 = theta_values['b']
        theta1 = theta_values['a']
    except FileNotFoundError:
        theta0 = 0.0
        theta1 = 0.0
    except KeyError:
        print("model_param.json の形式が不正です。theta0=0, theta1=0 で予測します。")
        theta0 = 0.0
        theta1 = 0.0

    while True:
        try:
            mileage = float(input("Enter the mileage of the car: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    estimated_price = estimate_price(mileage, theta0, theta1)

    print(f"Estimated price for a car with {mileage} miles: ${estimated_price:.2f}")

if __name__ == "__main__":
    main()