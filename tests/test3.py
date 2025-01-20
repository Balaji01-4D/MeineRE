data = {
    "folder":{
        "today":{
            "text":"going to party tonight",
            "data":"2024-4-9"
        },
        "dost":{
            "text":"gonna meet a friend",
            "data":"2024-4-10"

        },
        "newdata":{
            "text":"this new data file should be submitted",
            "data":"2024-04-4"
        }
    },
    "folder1":{
        "boss":{
            "text":"boss appointed a new staff",
            "data":"2024-3-10"
        }
    }
}

for keys in data.items():
    print(keys)
    print(f"---{keys}")