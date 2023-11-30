import google.generativeai as palm
import os
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = os.environ.get('API_KEY')
if not API_KEY:
  raise ValueError('API_KEY environment variable not set')

palm.configure(api_key=API_KEY)

models = [
    m for m in palm.list_models()
    if 'generateText' in m.supported_generation_methods
]
model = models[0].name


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    topic = request.form.get('topic')
    student_coding_level = request.form.get('coding_level')
    questions = request.form.get('question')
    print(f"Received form data: topic={topic}, level={student_coding_level}, questions={questions}")
            # ... rest of your code ...

    prompt = f"""You are an expert in pedagogy (brilliant sense/ability to teach)
      and a brilliant Software Developer. Provide me the best code example you can give on {topic}.
        My coding level is {student_coding_level}. 
    """
    explanation1 = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0.1,
        # The maximum length of the response
        max_output_tokens=800,
    )
    code_example = explanation1.result

    prompt = f"""Explain the following code example in a clear and concise way,
      suitable for a student with a {student_coding_level} coding level:

    python
    """
    explanation2 = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0.1,
        # The maximum length of the response
        max_output_tokens=800,
    )
    explanation = explanation2.result
    print(type(explanation))

    if questions:
      questions_list = questions.split("?")
      answers = []

      # Remove any empty strings from the list of questions.
      questions_list = [question for question in questions_list if question]
      for question in questions_list:
        prompt = f"Explain {question} in a clear and simple way, using {explanation} as a starting point."
        answers.append(
            palm.generate_text(
                model=model,
                prompt=prompt,
                temperature=0.1,
                # The maximum length of the response
                max_output_tokens=800,
            ))
    else:
      answers = []

    return render_template('index.html',
                           code_example=code_example,
                           explanation=explanation,
                           answers=answers)
  else:
    return render_template('index.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
