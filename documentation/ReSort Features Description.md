# ReSort: Your Smart Waste Sorting Assistant

## Introduction: 
Resort is a streamlit-based web application designed to help users identify and classify waste into three primary categories: Trash, Recycle, and Compost. Using both text and image classification powered by Google Gemini, combined with user-specific data visualization and personalized tips, ReSort aims to encourage sustainable habits and reduce landfill waste.

## Features 
### Text-Based Classification: 
The user describes the waste item they wish to dispose in a text box. After they click “Sort”, they will receive a sorting category (Trash, Recycle, or Compost) for the item and a brief explanation from the AI. After the response is given, the user has the option to click “Save”, which saves the item to their history. Saving is only allowed if the AI’s disposal method matches one of the three valid categories.

### Image-Based Classification:  
The user uploads an image of the waste item they wish to dispose. Then, they click “Analyze image”, which sorts the item into Trash, Recycle, or Compost, and also identifies the waste item. The AI then gives a response with the sorting category, item name, and a brief explanation on why the item is disposed in that manner. Next, the user can click “Save”, which saves the waste item to their history.

### Data Visualization (History):
From the sidebar on the left, the user can enter their waste sorting history. This page has two tabs: a “Statistics” tab and a “History” tab. This provides them with insights into their waste sorting habits with a pie chart and detailed table. The pie chart has three sections, each representing one of the three categories. They are also colored accordingly, with Trash being orange, Recycle being blue, and Compost being green. Below the pie chart, there is a total count of how many items of each category have been saved by the user. 

The user can switch from the “Statistics” tab to the “History” tab, where a detailed history table is displayed. The table has three columns: the item name, the disposal method, and the date sorted. This information helps the user so that if they had already sorted an item then saved it, they do not need to enter it again in the Sort page.

### Custom Analysis of History (Tips):
After the user has saved some items, be it through the text-based classification or the image classification, they can receive personalized tips through the Tips page. If the user has not sorted anything, no tips are given. The user can click the Tips page in the sidebar, then go to the “Generate tips” tab. There, the user will see a “Get personalized tips” button, which they can click to fetch tailored advice based on their unique sorting history.

## User Authentication and Security:
The user cannot access the website unless they register an account. To register, the user has to enter a username, email, and password. If the user uses a username or password that already exists, registering will fail. When the user successfully registers, their information is stored in the MySQL database. Their password is hashed for security purposes. Streamlit has a streamlit\_authenticator and session states that aid in this process. After registering, the user can use their information to login, granting them access to ReSort’s features.