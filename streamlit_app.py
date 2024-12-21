import streamlit as st
import mysql.connector

# Function to retrieve books based on search criteria
def get_books(search_title=None, search_author=None, search_category=None):

    # Connect to MySQL database
    connection = mysql.connector.connect(
            host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",  
            port=4000,
            user="3tN77YkdrSS9WKK.root", 
            password="Eufk68BdWytW0E6w",
            database="BookSpace"
        )
    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Base query
    query = "SELECT book_id, book_title, book_authors, categories, year FROM book_details WHERE 1=1"

    # Add conditions to the query based on search input
    if search_title:
        query += f" AND book_title LIKE '%{search_title}%'"
    if search_author:
        query += f" AND book_authors LIKE '%{search_author}%'"
    if search_category:
        query += f" AND categories LIKE '%{search_category}%'"

    # Execute the query
    cursor.execute(query)

    # Fetch all the results from the query
    books = cursor.fetchall()

    return books


# Streamlit app layout
st.title("BookSpace")
st.header("Browse Books in Our Collection")

# Add search inputs for title, author, and genre
search_title = st.text_input("Search by Book Title")
search_author = st.text_input("Search by Author")
search_category = st.selectbox("Search by Genre", ["","Fiction", "Historical fiction", "Business & Economics", "Creation (Literary, artistic, etc.)",
                                                "Biography & Autobiography", "Literary Collections", "Sports & Recreation", "Imaginary histories", "English poetry", "World War",
                                                "Language Arts & Disciplines", "Political Science", "Dystopias", "Dyslexia", "Literary Criticism", "N/A"])

# Get books data based on search input
books_data = get_books(search_title, search_author, search_category)

# Display books in a table if data is available
if books_data:
    st.write("### List of Books:")
    st.write("This list displays all the books matching your search criteria.")

    # Create a table to display books in a structured format
    book_columns={
    0 : "ID",
    1 : "Title",
    2 : "Author",
    3 : "Category",
    4 : "Year Published"
}

    st.table(books_data)
else:
    st.write("No books found based on your search criteria.")