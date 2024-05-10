import PyPDF2
import json
import re
import os

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = [page.extract_text() for page in pdf_reader.pages]
    return "\n".join(text)

def find_questions(text, letter):
    pattern = f"Answers{letter}(([6-9]\.)|(\d\d)\.)((.|\s)*?)(?=More information:)"    
    matches = re.findall(pattern, text, re.DOTALL)    
    return matches

def find_options(text):    
    pattern = r"❍[A-Z]\.\s.*"
    matches = re.findall(pattern, text)
    return matches

def find_prompt(text):
    pattern = r"^([\s\S]*?)\s*❍"
    match = re.findall(pattern, text)    
    return match

def find_explanation(text):
    pattern = r"(The Answer([\s\S.]*))"
    matches = re.findall(pattern, text)    
    return matches

def find_answer(text):
    pattern = r"([A-Z])\."
    matches = re.findall(pattern, text.split("The incorrect")[0])
    return matches

def parse_questions(matches):
    questions = []
    for match in matches:
        text = match[3]
        options = [option[1:] for option in find_options(text)]
        prompt = find_prompt(text)[0][1:]   
        explanation = find_explanation(text)[0][0]          
        answer = find_answer(explanation)           
        question = {
            "question": prompt,
            "options": options,
            "correct_answer": answer,
            "explanation": explanation
        }
        #print(json.dumps(question, indent=4))
        questions.append(question)
    return questions


def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def find_exams(exam_names, pdf_path):
    exams = {}
    text = extract_text_from_pdf(pdf_path)
    for letter in exam_names:
        matches = find_questions(text, letter)
        print(f"Found {len(matches)} questions in {pdf_path}")
        exams[f"Practice Exam {letter}"] = parse_questions(matches)
    return exams

def main():   
    pdf_path = find_pdf()
    exams = find_exams(["A", "B", "C"], pdf_path)
    save_to_json(exams, 'exams.json')
    print("Extraction complete and saved to exam_b_questions.json")

def find_pdf():
    """ Find and return the first PDF file in the given directory. """
    for filename in os.listdir("./uploads"):
        if filename.lower().endswith('.pdf'):
            return os.path.join("./uploads/", filename)
    return None  # Return None if no PDF file is found


if __name__ == "__main__":
    main()