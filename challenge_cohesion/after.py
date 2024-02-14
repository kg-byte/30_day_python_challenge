import pandas as pd


def c_to_k(c: float) -> float:
    return c + 273.15


def humidaty_scale_0_1(h: float) -> float:
    return h/100


def calibrate_co2(co2: float)-> float:
    return co2 + 23


def process_row(row: pd.DataFrame)-> pd.DataFrame:
    sensor: str= row['Sensor']
    value: float = row['Value']
    processing_fn = {
    "Temperature": c_to_k,
    "Humidity": humidaty_scale_0_1,
    "CO2": calibrate_co2
    }
    row['Value'] = processing_fn[sensor](value)
    return row


def process_data(data: pd.DataFrame, option: str) -> pd.DataFrame:
    if option in ("Temperature", "Humidity", "CO2"):
        data = data.loc[data["Sensor"] == option]

    processed_data: list[pd.DataFrame]= []
    for _, row in data.iterrows():
        processed_row = process_row(row)
        processed_data.append(processed_row)

    return pd.DataFrame(data=processed_data)

def main() -> None:
    raw_data = pd.read_csv("challenge_cohesion/sensor_data.csv")
    processed_data = process_data(data=raw_data, option="CO2")
    print(processed_data)


if __name__ == "__main__":
    main()
