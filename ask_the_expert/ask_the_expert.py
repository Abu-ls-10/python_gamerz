from tkinter import Tk, simpledialog, messagebox
import os

FILE_NAME = "capital_data.txt"

def read_from_file():
    if not os.path.exists(FILE_NAME):
        return {}

    data = {}
    with open(FILE_NAME, "r") as file:
        for line in file:
            line = line.strip()
            if not line or "/" not in line:
                continue
            country, city = line.split("/", 1)
            data[country.lower()] = city
    return data


def write_to_file(country_name, city_name):
    # Avoid duplicate writes
    with open(FILE_NAME, "a") as file:
        file.write(f"{country_name}/{city_name}\n")


print("Ask the Expert - Capital Cities of the World")

root = Tk()
root.withdraw()

the_world = read_from_file()

while True:
    query_country = simpledialog.askstring(
        "Country",
        "Type a country name (Cancel to quit):"
    )

    if query_country is None:
        break  # user pressed cancel → exit cleanly

    query_country = query_country.strip()

    if not query_country:
        continue

    key = query_country.lower()

    if key in the_world:
        result = the_world[key]
        messagebox.showinfo(
            "Answer",
            f"The capital city of {query_country.title()} is {result}!"
        )
    else:
        new_city = simpledialog.askstring(
            "Teach me",
            f"I don't know! What is the capital city of {query_country}?"
        )

        if new_city:
            new_city = new_city.strip()
            the_world[key] = new_city
            write_to_file(query_country.title(), new_city)

            messagebox.showinfo(
                "Learned!",
                f"Got it! {query_country.title()} → {new_city}"
            )

root.destroy()