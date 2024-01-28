import requests
import json
import csv


headers = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) //"
                  "Chrome/117.0.0.0 Safari/537.36"
}


def get_vacancies():
    vacancies_data = []
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": "Слесарь",
        "area": 2,
        "per_page": 30
    }
    response = requests.get(url=url, params=params, headers=headers)
    data = response.json()
    vacancies = data.get("items", [])
    for vacancy in vacancies:
        vacancy_title = vacancy.get("name")
        company_name = vacancy.get("employer", {}).get("name")
        vacancy_url = vacancy.get("alternate_url")
        required_experience = vacancy.get("experience", {}).get("name")
        area = vacancy.get("area", {}).get("name")
        if vacancy.get("salary") is not None:
            salary_from = vacancy.get("salary", {}).get("from")
            salary_to = vacancy.get("salary", {}).get("to")
            salary = f"От {salary_from} до {salary_to}"
        else:
            salary = "не указана"

        vacancies_data.append(
            {
                "Title": vacancy_title,
                "Company name": company_name,
                "URL": vacancy_url,
                "Required experience": required_experience,
                "Area": area,
                "Salary": salary
            }
        )
    return vacancies_data


def save_data_json(vacancies_data):
    open("data.json", "w").close()
    with open("data.json", "a") as file:
        json.dump(vacancies_data, file, indent=4, ensure_ascii=False)


def save_data_csv(vacancies_data):
    open("data.csv", "w").close()
    with open("data.csv", "a") as file:
        cols = ["Title", "Company name", "URL", "Required experience", "Area", "Salary"]
        writer = csv.DictWriter(file, fieldnames=cols)
        writer.writeheader()
        writer.writerows(vacancies_data)


if __name__ == "__main__":
    save_data_json(get_vacancies())
    save_data_csv(get_vacancies())
