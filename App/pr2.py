import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import squarify



# Load the dataset
data_path = r'C:\Users\Vasilis\Desktop\Github\Sleep and Health Lifestyle\3. Cleaning\cleaned_sleep_health_dataset.csv'  # Ensure the file is in the same directory
data = pd.read_csv(data_path)

# Create an age decade column for further analysis
data['Age Decade'] = (data['Age'] // 10) * 10


# Set page layout to wide
st.set_page_config(layout="wide")

# Apply custom CSS to restrict content width
st.markdown(
    """
    <style>
    /* Constrain the main content width */
    div[data-testid="stAppViewContainer"] {
        max-width: 1280px;
        margin: 0 auto;
        padding-top: 20px;
    }

    /* Adjust sidebar width (optional) */
    div[data-testid="stSidebar"] {
        width: 300px;
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Sidebar - Filters
st.sidebar.header("Filters")
selected_gender = st.sidebar.multiselect(
    "Gender",
    options=data['Gender'].unique(),
    default=data['Gender'].unique()
)
selected_occupation = st.sidebar.multiselect(
    "Occupation",
    options=data['Occupation'].unique(),
    default=data['Occupation'].unique()
)
min_age, max_age = int(data['Age'].min()), int(data['Age'].max())
age_range = st.sidebar.slider(
    "Age Range",
    min_age,
    max_age,
    (min_age, max_age)
)

# Apply filters
filtered_data = data[
    (data['Gender'].isin(selected_gender)) & 
    (data['Occupation'].isin(selected_occupation)) & 
    (data['Age'] >= age_range[0]) & 
    (data['Age'] <= age_range[1])
]

# Title and description
st.title("Sleep Health Dashboard")
st.markdown("""
Explore the relationships between sleep health, physical activity, and health indicators across different professions, genders, and age groups.
""")

# Summary Container
st.markdown("### Sample Distribution Overview")
col1, col2, col3 = st.columns(3)

# Define a unified color palette
palette = sns.color_palette("coolwarm", n_colors=10)  # Παλέτα coolwarm με 10 αποχρώσεις

# 1. Gender Distribution
gender_distribution = filtered_data['Gender'].value_counts()
with col1:
    st.markdown("#### Gender Distribution")
    fig, ax = plt.subplots(figsize=(4, 4))
    gender_distribution.plot(
        kind='bar',
        color=[palette[0], palette[1]],  # Χρησιμοποίηση δύο χρωμάτων από την παλέτα
        alpha=0.8,
        ax=ax
    )
    ax.set_title("Gender Distribution")
    ax.set_ylabel("Count")
    ax.set_xlabel("Gender")
    st.pyplot(fig)

# 2. Sleep Hours Distribution (Pie Chart)
sleep_hours_bins = pd.cut(filtered_data['Sleep Duration'], bins=[0, 6, 8, 24], labels=["4-6 hours", "6-8 hours", ">8 hours"])
sleep_hours_distribution = sleep_hours_bins.value_counts()
with col2:
    st.markdown("#### Sleep Hours Distribution")
    fig, ax = plt.subplots(figsize=(4, 4))
    sleep_hours_distribution.plot(
        kind='pie',
        autopct='%1.1f%%',
        colors=palette[:3],  # Πρώτες 3 αποχρώσεις της παλέτας
        ax=ax,
        startangle=90,
        textprops={'fontsize': 10}  # Ensure consistent font size
    )
    ax.set_ylabel("")
    ax.set_title("Sleep Hours Distribution", fontsize=12)
    st.pyplot(fig)

# 3. Activity Level Distribution (Pie Chart)
activity_level_distribution = filtered_data['Activity Level'].value_counts()
with col3:
    st.markdown("#### Activity Level Distribution")
    fig, ax = plt.subplots(figsize=(4, 4))
    activity_level_distribution.plot(
        kind='pie',
        autopct='%1.1f%%',
        colors=palette[3:6],  # Επόμενες 3 αποχρώσεις της παλέτας
        ax=ax,
        startangle=90,
        textprops={'fontsize': 10}
    )
    ax.set_ylabel("")
    ax.set_title("Activity Level Distribution", fontsize=12)
    st.pyplot(fig)



# Unified color palette
palette = sns.color_palette("coolwarm", n_colors=10)  # Same palette for consistency

# Third Container: Treemap of Occupations and Sleep Quality Ratings
with st.container():
    col1, col2 = st.columns([2, 1])  # Make the treemap column wider than the bar chart

    # Treemap of Occupations
    with col1:
        st.markdown("### Treemap of Occupations")
        if 'Occupation' in filtered_data.columns:
            occupation_counts = filtered_data['Occupation'].value_counts()
            occupation_df = pd.DataFrame({
                'labels': occupation_counts.index + "\n" + occupation_counts.values.astype(str),
                'values': occupation_counts.values
            })
            fig = plt.figure(figsize=(12, 8))  # Increased size and width
            squarify.plot(
                sizes=occupation_df['values'],
                label=occupation_df['labels'],
                alpha=0.8,
                color=palette[:len(occupation_df)],  # Use the palette
                text_kwargs={'fontsize': 10}  # Set font size for better readability
            )
            plt.axis('off')
            st.pyplot(fig)

    # Sleep Quality Ratings
    with col2:
        st.markdown("### Sleep Quality Ratings Distribution")
        if 'Quality of Sleep' in filtered_data.columns:
            sleep_quality_counts = filtered_data['Quality of Sleep'].value_counts().sort_index()
            fig, ax = plt.subplots(figsize=(6, 6))  # Adjusted size to align better with treemap
            sns.barplot(
                x=sleep_quality_counts.index,
                y=sleep_quality_counts.values,
                palette=palette[:len(sleep_quality_counts)],  # Use the palette
                edgecolor='black',
                ax=ax
            )
            ax.set_title('Sleep Quality Ratings Distribution', fontsize=14)
            ax.set_xlabel('Sleep Quality Rating (1 = Poor, 10 = Excellent)', fontsize=12)
            ax.set_ylabel('Number of People', fontsize=12)
            st.pyplot(fig)




# Define physical activity categories
def categorize_activity(activity_level):
    if activity_level < 30:
        return "15-30"
    elif 30 <= activity_level <= 60:
        return "30-60"
    else:
        return "More than 60"

# Define age group categories
def categorize_age_group(age):
    if age < 30:
        return "Under 30"
    elif 30 <= age < 40:
        return "30s"
    elif 40 <= age < 50:
        return "40s"
    else:
        return "50+"

# Apply the categorization to the dataset
filtered_data['Activity Category'] = filtered_data['Physical Activity Level'].apply(categorize_activity)
filtered_data['Age Group'] = filtered_data['Age'].apply(categorize_age_group)

# Ensure Age Groups are ordered from smallest to largest
age_group_order = ["Under 30", "30s", "40s", "50+"]
filtered_data['Age Group'] = pd.Categorical(filtered_data['Age Group'], categories=age_group_order, ordered=True)

# Create the grouped bar chart
activity_by_age_group = (
    filtered_data.groupby(['Age Group', 'Activity Category'])
    .size()
    .reset_index(name='Count')
)

# Unified color palette
palette = sns.color_palette("coolwarm", n_colors=10)  # Same palette as the other charts

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="Age Group",
    y="Count",
    hue="Activity Category",
    data=activity_by_age_group,
    palette=palette[:3],  # First 3 colors of the palette for the Activity Categories
    edgecolor='black'
)

# Add titles and labels
ax.set_title('Physical Activity Duration by Age Group', fontsize=16)
ax.set_xlabel('Age Group', fontsize=12)
ax.set_ylabel('Number of People', fontsize=12)
ax.legend(title='Activity Category (Minutes)', fontsize=10, title_fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Show the chart in Streamlit
st.pyplot(fig)



# Unified color palette
palette = sns.color_palette("coolwarm", n_colors=10)

# 5. Sleep Duration and Quality Across the Population
st.markdown("### Sleep Duration and Quality Across the Population")

# Prepare data for plotting
average_sleep_duration = filtered_data.groupby('Age')['Sleep Duration'].mean()
average_sleep_quality = filtered_data.groupby('Age')['Quality of Sleep'].mean()

fig, ax = plt.subplots(figsize=(12, 6))

# Area plot for sleep duration
ax.fill_between(
    average_sleep_duration.index,
    average_sleep_duration.values,
    color=palette[1],  # Consistent color from the palette
    alpha=0.5,
    label='Average Sleep Duration (Hours)'
)

# Line plot for sleep quality
ax.plot(
    average_sleep_quality.index,
    average_sleep_quality.values,
    color=palette[7],  # Consistent color from the palette
    linewidth=2,
    marker='o',
    label='Average Sleep Quality (Score)'
)

# Add titles and labels
ax.set_title('Sleep Duration and Quality Across the Population', fontsize=16)
ax.set_xlabel('Age', fontsize=12)
ax.set_ylabel('Values', fontsize=12)
ax.legend(title='Metrics', fontsize=10, title_fontsize=12)
ax.grid(alpha=0.5, linestyle='--')

# Show the chart in Streamlit
st.pyplot(fig)

# Ensure unified color palette
palette = sns.color_palette("coolwarm", n_colors=10)  # Παλέτα με τουλάχιστον 10 χρώματα

# First container: Average Sleep Duration by Occupation and Activity Level Distribution by Occupation
with st.container():
    col1, col2 = st.columns(2)

    # 1. Average Sleep Duration by Occupation
    with col1:
        st.markdown("### Average Sleep Duration by Occupation")
        avg_sleep_by_occupation = filtered_data.groupby('Occupation')['Sleep Duration'].mean()
        
        # Ensure there are enough colors
        color = palette[2] if len(palette) > 2 else 'blue'

        fig, ax = plt.subplots(figsize=(5, 4))
        avg_sleep_by_occupation.sort_values(ascending=False).plot(
            kind='bar',
            color=color,  # Unified color
            ax=ax
        )
        ax.set_title("Average Sleep Duration by Occupation")
        ax.set_ylabel("Sleep Duration (hours)")
        ax.set_xlabel("Occupation")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

    # 2. Activity Level Distribution by Occupation
    with col2:
        st.markdown("### Activity Level Distribution by Occupation")
        activity_level_by_occupation = filtered_data.groupby('Occupation')['Activity Level'].value_counts(normalize=True).unstack()
        
        # Adjust palette dynamically based on the number of levels
        activity_palette = sns.color_palette("coolwarm", n_colors=activity_level_by_occupation.shape[1])

        fig, ax = plt.subplots(figsize=(5, 4))
        activity_level_by_occupation.plot(
            kind='bar',
            stacked=True,
            color=activity_palette,  # Use dynamic palette
            ax=ax
        )
        ax.set_title("Activity Level Distribution by Occupation")
        ax.set_ylabel("Proportion")
        ax.set_xlabel("Occupation")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

# Second container: Sleep Disorders Percentage by Occupation and Average Stress Level by Occupation
with st.container():
    col1, col2 = st.columns(2)

    # 3. Sleep Disorders Percentage by Occupation
    with col1:
        st.markdown("### Sleep Disorders Percentage by Occupation")
        sleep_disorders_grouped = filtered_data[filtered_data['Sleep Disorder'] != 'None'] \
            .groupby('Occupation')['Sleep Disorder'].count()
        total_by_occupation = filtered_data['Occupation'].value_counts()
        sleep_disorders_percentage = (sleep_disorders_grouped / total_by_occupation) * 100
        
        # Ensure there are enough colors
        color = palette[4] if len(palette) > 4 else 'teal'

        fig, ax = plt.subplots(figsize=(5, 4))
        sleep_disorders_percentage.sort_values(ascending=False).plot(
            kind='bar',
            color=color,  # Unified color
            ax=ax
        )
        ax.set_title("Sleep Disorders Percentage by Occupation")
        ax.set_ylabel("Percentage (%)")
        ax.set_xlabel("Occupation")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)

    # 4. Average Stress Level by Occupation
    with col2:
        st.markdown("### Average Stress Level by Occupation")
        stress_by_occupation = filtered_data.groupby('Occupation')['Stress Level'].mean()
        
        # Ensure there are enough colors
        color = palette[6] if len(palette) > 6 else 'salmon'

        fig, ax = plt.subplots(figsize=(5, 4))
        stress_by_occupation.sort_values(ascending=False).plot(
            kind='bar',
            color=color,  # Unified color
            ax=ax
        )
        ax.set_title("Average Stress Level by Occupation")
        ax.set_ylabel("Average Stress Level")
        ax.set_xlabel("Occupation")
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
