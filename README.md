# Comptia Security+ 701 Practice Exam Application

This project is designed to facilitate the learning process for those preparing for the CompTIA Security+ certification. It provides a convenient platform to format, track, and interact with the practice exam questions purchased from Professor Messer’s website.

## Prerequisites

Before you use this application, make sure you have purchased the necessary Test Exams from [Professor Messer’s website](https://www.professormesser.com/). This application is intended to complement your existing study materials by providing an interactive testing environment.

## Getting Started

Follow these steps to get the application up and running on your local machine for development and testing purposes.

### Step 1: Clone the Repository

```bash
git clone https://github.com/glopez195/PracticeSecurityPlus
cd PracticeSecurityPlus
```

### Step 2: Set Up a Python Virtual Environment

Creating a virtual environment is not required but highly recommended to avoid conflicts with other projects.

**For macOS and Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**For Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```


For additional support setting up the virtual environment visit https://python.land/virtual-environments/virtualenv
### Step 3: Install Dependencies

Ensure you are in the project directory where the `requirements.txt` is located.

```bash
pip install -r requirements.txt
```

### Step 4: Prepare the Exam PDF

Copy the PDF file containing the practice exam questions to the root directory of the project. Ensure that this is the only PDF in the root to avoid any confusion during file processing.

### Step 5: Process the PDF

Run the processing script to parse the PDF and prepare the data for the application.

```bash
python process_file.py
```

### Step 6: Launch the Application

Start the Flask application. By default, it will run on port 5000.

```bash
flask run
```

Navigate to `http://localhost:5000` in your web browser to access the application.

## Functionality

The application offers two modes of interaction with the practice exam questions:

1. **Exam Simulation Mode:** Answer all questions and submit your answers to see the overall results at the end. This mode simulates the actual testing environment.
2. **Immediate Feedback Mode:** After answering a question, you can immediately check your answer to receive feedback. This is useful for learning and understanding the material on a deeper level.

Both modes are designed to enhance your learning experience by providing detailed feedback and tracking your progress.

## Credits

This project utilizes practice exams created by Professor Messer. All content rights and intellectual property belong to him. Please ensure you have legally obtained his materials. Visit his [website](https://www.professormesser.com/) for more resources.

## License

This project is open-sourced under the MIT license.