
import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="AI Product Recommendation System",
    page_icon="🛍️",
    layout="wide"
)

# 1. Product dataset: 15 products
products = [
    ["Wireless Headphones", "Electronics", 1499,
     "Music, audio, calls and travel"],
    ["Bluetooth Speaker", "Electronics", 1999,
     "Music, audio, parties and outdoor use"],
    ["Wireless Mouse", "Electronics", 799,
     "Computer work, study and office"],
    ["Study Desk Lamp", "Home & Living", 899,
     "Reading, studying and working"],
    ["Water Bottle", "Home & Living", 399,
     "School, college, gym and travel"],
    ["Storage Organizer", "Home & Living", 699,
     "Books, stationery and home storage"],
    ["Running Shoes", "Sports", 2499,
     "Running, jogging and fitness training"],
    ["Yoga Mat", "Sports", 999,
     "Yoga, stretching and workouts"],
    ["Cricket Bat", "Sports", 1799,
     "Cricket practice and outdoor games"],
    ["Notebook Set", "Education", 299,
     "Study notes, assignments and exams"],
    ["Scientific Calculator", "Education", 699,
     "Mathematics, science and calculations"],
    ["Laptop Stand", "Education", 1199,
     "Laptop, study and online learning"],
    ["Face Moisturizer", "Personal Care", 349,
     "Skincare and skin hydration"],
    ["Shampoo", "Personal Care", 249,
     "Hair washing and grooming"],
    ["Fitness Hand Gripper", "Personal Care", 499,
     "Exercise, grip strength and fitness"]
]

df = pd.DataFrame(
    products,
    columns=["Name", "Category", "Price", "Description"]
)


# 2. Content-based recommendation algorithm
def recommend_products(category, budget, intended_use):
    results = df[
        (df["Category"] == category) &
        (df["Price"] <= budget)
    ].copy()

    user_words = set(
        re.findall(r"[a-zA-Z0-9]+", intended_use.lower())
    )

    scores = []
    reasons = []

    for _, product in results.iterrows():
        product_text = (
            product["Name"] + " " + product["Description"]
        ).lower()

        product_words = set(
            re.findall(r"[a-zA-Z0-9]+", product_text)
        )

        matches = user_words.intersection(product_words)
        score = 80 + min(len(matches) * 5, 20)

        reason = (
            f"Matches category {category} and is within "
            f"your budget of Rs. {budget}."
        )

        if matches:
            reason += (
                " Matching keywords: "
                + ", ".join(sorted(matches))
            )
        else:
            reason += " No direct keyword match was found."

        scores.append(score)
        reasons.append(reason)

    results["Score"] = scores
    results["Reason"] = reasons

    return results.sort_values(
        by=["Score", "Price"],
        ascending=[False, True]
    ).head(3)


# 3. Streamlit interface
st.title("AI-Powered Product Recommendation System")
st.write(
    "Find suitable products based on your preferences."
)

st.sidebar.header("Enter Your Preferences")

category = st.sidebar.selectbox(
    "Select Category",
    sorted(df["Category"].unique())
)

budget = st.sidebar.number_input(
    "Maximum Budget (Rs.)",
    min_value=1,
    max_value=100000,
    value=2000
)

intended_use = st.sidebar.text_input(
    "Intended Use",
    placeholder="e.g. music, study, fitness"
)

if st.sidebar.button("Recommend Products"):
    if not intended_use.strip():
        st.warning("Please enter your intended use.")
    else:
        recommendations = recommend_products(
            category, budget, intended_use
        )

        st.subheader("Top Recommended Products")

        if recommendations.empty:
            st.warning(
                "No products match your selected category "
                "and budget. Please increase your budget "
                "or select another category."
            )
        else:
            for rank, (_, product) in enumerate(
                recommendations.iterrows(), start=1
            ):
                st.markdown(
                    f"### {rank}. {product['Name']}"
                )
                st.write(
                    f"**Category:** {product['Category']}"
                )
                st.write(
                    f"**Price:** Rs. {product['Price']}"
                )
                st.write(
                    f"**Description:** {product['Description']}"
                )
                st.write(
                    f"**Relevance Score:** {product['Score']}/100"
                )
                st.write(
                    f"**Reason:** {product['Reason']}"
                )
                st.divider()


# 4. Display the complete dataset
st.subheader("Available Product Dataset")
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# 5. Test three different user profiles
st.subheader("Testing with Three User Profiles")

test_profiles = [
    ("Music Listener", "Electronics", 2000, "music audio"),
    ("Student", "Education", 1500, "study exams notes"),
    ("Fitness User", "Sports", 2600, "fitness exercise workout")
]

if st.button("Run Three Tests"):
    passed_count = 0

    for name, cat, limit, purpose in test_profiles:
        result = recommend_products(cat, limit, purpose)

        passed = (
            not result.empty
            and (result["Category"] == cat).all()
            and (result["Price"] <= limit).all()
        )

        st.markdown(f"### {name}")
        st.write(
            f"**Category:** {cat} | "
            f"**Budget:** Rs. {limit} | "
            f"**Intended use:** {purpose}"
        )

        if not result.empty:
            st.dataframe(
                result[["Name", "Category", "Price",
                        "Score", "Reason"]],
                use_container_width=True,
                hide_index=True
            )

        # Correct indentation for PASS/FAIL messages
        if passed:
            st.success(
                "PASS: Category and budget match."
            )
            passed_count += 1
        else:
            st.warning(
                "FAIL: No matching products found."
            )

    st.subheader("Test Summary")
    st.write(
        f"Passed {passed_count} out of "
        f"{len(test_profiles)} tests."
    )

    if passed_count == len(test_profiles):
        st.success("All three user profile tests passed.")
    else:
        st.warning("Review the failed test profiles.")


st.caption(
    "Method: Content-based recommendation using category "
    "matching, budget filtering and keyword similarity."
)
