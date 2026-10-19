# AI-Powered Product Recommendation System

## Project Overview
This project recommends products based on user preferences using Python and Streamlit. Users can select a product category, specify a maximum budget, and enter their intended use to receive personalized recommendations.

## Features
- Dataset containing 15 products across five categories
- Category-based product filtering
- Budget-based filtering
- Keyword matching for recommendations
- Top three recommended products with relevance scores and explanations
- Testing with three sample user profiles

## Technologies Used
- Python
- Streamlit
- Pandas
- Regular Expressions (`re`)

## Installation and Execution

1. Install Python.
2. Download or clone this repository.
3. Install dependencies:

   `python -m pip install -r requirements.txt`

4. Run the application:

   `python -m streamlit run app.py`

5. Open the local URL displayed in the terminal.

## Recommendation Method
The application uses content-based recommendation with category matching, budget filtering, and keyword similarity.

## Testing
The system includes three sample profiles: Music Listener, Student, and Fitness User.

## Author
Shrenik Patil
