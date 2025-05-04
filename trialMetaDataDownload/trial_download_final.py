import requests
import csv

url = "https://euclinicaltrials.eu/ctis-public-api/search"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

all_trials = []
page = 1
page_size = 50  # You can increase this if the API allows more

while True:
    payload = {
        "pagination": {
            "page": page,
            "size": page_size
        },
        "sort": {
            "property": "decisionDate",
            "direction": "DESC"
        },
        "searchCriteria": {
            "containAll": None,
            "containAny": None,
            "containNot": None,
            "title": None,
            "number": None,
            "status": None,
            "medicalCondition": None,
            "sponsor": None,
            "endPoint": None,
            "productName": None,
            "productRole": None,
            "populationType": None,
            "orphanDesignation": None,
            "msc": None,
            "ageGroupCode": None,
            "therapeuticAreaCode": None,
            "trialPhaseCode": None,
            "sponsorTypeCode": None,
            "gender": None,
            "protocolCode": None,
            "rareDisease": None,
            "pip": None,
            "haveOrphanDesignation": None,
            "hasStudyResults": None,
            "hasClinicalStudyReport": None,
            "isLowIntervention": None,
            "hasSeriousBreach": None,
            "hasUnexpectedEvent": None,
            "hasUrgentSafetyMeasure": None,
            "isTransitioned": None,
            "eudraCtCode": None,
            "trialRegion": None,
            "vulnerablePopulation": None,
            "mscStatus": None
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    trials = data.get("data", [])
    if not trials:
        break

    for trial in trials:
        all_trials.append([trial.get("ctNumber"), trial.get("ctTitle")])

    # Check for more pages
    if data.get("pagination", {}).get("nextPage"):
        page += 1
    else:
        break

# Save to CSV
with open("clinical_trial_numbers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Trial Number", "Title"])
    writer.writerows(all_trials)

print(f"Saved {len(all_trials)} trial entries to 'clinical_trial_numbers.csv'")
