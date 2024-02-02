# TECHIN-514-lab3

## Overview
The repo is about creating a Streamlit TODO task app that I can use to manage my todo tasks.


The TODO task App includes the features of:
1. `name`
2. `description`
3. `is_done` 
4. `created_at` (datetime)
5. `created_by` (person)
6. `category` (school, work, personal)
7.  Toggle the state field of tasks
8.  search bar
9.  filter dropdown for categorial fields
10. a button to delete tasks

## How to run
- Installation  
Open the terminal and run the following commands:
```bash
pip install -r requirements.txt
```

- Usage
Next, run the following commands:
```bash
streamlit run app.py
```

## Lessons learned
- I learned how to define data model with relevant formats via sqlite3.
- I learned how to how to use the Pydantic class with relevant formats to create forms.
- I learned some advanced functions of Pydantic form like filter dropdown menu.
- When I add a new column to the table, I need to delete the original todoapp.sqlite file first, otherwise the web page will report an error with "no xxx column".

## Future improvements
- To make the interface more joyful, I change the state display keywords from Planned, In-progress and Done to 📝 Planned, 🏃 In-progress and 🎊 Done.  
Hence, I can be remined of the current state with the emoji directly.

## Questions
- After click streamlit run app.py, what logic is based on the automatically generated web domain name? Can we customize the domain name?
- I wanted the first column (likely an index column automatically added by pandas) was not shown in the output table for a cleaner interface, but I failed to achieve this since it was easy to get various errors when I deleted that column. Hence, I want to know how to hide the first automatic column.
- When I updated the state from In-progress to Done, I have to refresh to see the change. I want to know how to the change immediately without refreshing.