import sqlite3
import psycopg2
import os
import streamlit as st
from datetime import datetime
import pandas as pd

# Connect to our database
DB_CONFIG = os.getenv("DB_TYPE")
if DB_CONFIG == 'PG':
    PG_USER = os.getenv("PG_USER")
    PG_PASSWORD = os.getenv("PG_PASSWORD")
    PG_HOST = os.getenv("PG_HOST")
    PG_PORT = os.getenv("PG_PORT")
    con = psycopg2.connect(f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/todoapp?connect_timeout=10&application_name=todoapp")
else:
    con = sqlite3.connect("todoapp.sqlite", isolation_level=None)
cur = con.cursor()

# Update the table creation query
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        name TEXT,
        created_by TEXT,
        description TEXT,
        category TEXT,
        state TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
)

def update_task_state(task_id, new_state):
    """
    Update the state of a task in the database.
    """
    placeholder = "%s" if DB_CONFIG == 'PG' else "?"
    cur.execute(
        f"UPDATE tasks SET state = {placeholder} WHERE id = {placeholder}",
        (new_state, task_id)
    )
    con.commit()

def delete_task(task_id):
    """
    Delete a task from the database.
    """
    placeholder = "%s" if DB_CONFIG == 'PG' else "?"
    cur.execute(f"DELETE FROM tasks WHERE id = {placeholder}", (task_id,))
    con.commit()

def main():
    st.title("Todo App")

    # Define state_mapping at the start so it's accessible throughout main()
    state_mapping = {"📝 Planned": "Planned", "🏃 In-Progress": "In-Progress", "🎊 Done": "Done"}

    # Filters for category and state
    category_filter = st.selectbox("Filter by category", ["All"] + ["School", "Work", "Life"], index=0)
    state_filter_with_emojis = ["All", "📝 Planned", "🏃 In-Progress", "🎊 Done"]
    state_filter = st.selectbox("Filter by state", state_filter_with_emojis, index=0)

    # Search bar
    search_term = st.text_input("Search tasks")

    # Display the form for adding a new task
    with st.form(key="task_form"):
        name = st.text_input("Name")
        created_by = st.text_input("Created By")
        description = st.text_area("Description")
        category_options = ["School", "Work", "Life"]
        selected_category = st.selectbox("Category", category_options)
        state_options_with_emojis = ["📝 Planned", "🏃 In-Progress", "🎊 Done"]
        selected_state = st.selectbox("State", state_options_with_emojis)
        created_at = datetime.now()  # Automatically capture the current timestamp
        submitted = st.form_submit_button("Submit")

    if submitted:
        cur.execute(
            """
            INSERT INTO tasks (name, description, created_by, category, state, created_at) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, description, created_by, selected_category, state_mapping[selected_state], created_at.strftime('%Y-%m-%d %H:%M:%S')),
        )
        con.commit()
        st.success("Task added successfully.")

    # Construct the query based on filters
    conditions = []
    parameters = []

    if search_term:
        conditions.append("name LIKE ?")
        parameters.append(f'%{search_term}%')
    
    if category_filter != "All":
        conditions.append("category = ?")
        parameters.append(category_filter)

    if state_filter != "All":
        conditions.append("state = ?")
        parameters.append(state_mapping[state_filter])

    query = "SELECT id, name, created_by, category, state, description, created_at FROM tasks"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    data = cur.execute(query, parameters).fetchall()

    if data:
        df = pd.DataFrame(data, columns=["ID", "Name", "Created By", "Category", "State", "Description", "Created At"])
        state_to_emoji = {"Planned": "📝 Planned", "In-Progress": "🏃 In-Progress", "Done": "🎊 Done"}
        df['State'] = df['State'].map(state_to_emoji)

        # Display the DataFrame
        st.dataframe(df, use_container_width=True)

        # Select a task to update its state
        task_id = st.selectbox("Select Task ID to Change State", df['ID'])
        new_state = st.selectbox("Select New State", state_options_with_emojis)
        if st.button("Update Task State"):
            update_task_state(task_id, state_mapping[new_state])
            st.success(f"Task {task_id} updated to {new_state}.")

        # Button for deleting tasks
        delete_task_id = st.selectbox("Select Task ID to Delete", df['ID'], key='delete_task')
        if st.button("Delete Task"):
            delete_task(delete_task_id)
            st.success(f"Task {delete_task_id} deleted successfully.")

if __name__ == "__main__":
    main()
